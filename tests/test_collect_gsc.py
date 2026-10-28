"""Offline regression tests; placeholders are not credentials or API evidence."""
import importlib.util
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('gsc', Path(__file__).resolve().parents[1] / 'painel-seo/collect_gsc.py')
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

class GSCTests(unittest.TestCase):
    def test_property_boundaries_and_permission(self):
        for site in ['sc-domain:arquindex.com.br', 'https://www.arquindex.com.br/', 'sc-domain:bh.arquindex.com.br']:
            self.assertTrue(gsc.authorized_property({'siteUrl': site, 'permissionLevel': 'siteOwner'}))
        for site in ['sc-domain:fakearquindex.com.br', 'https://arquindex.com.br.evil.example/', 'https://evil.example/arquindex.com.br/', 'https://arquindex.com.br@evil.example/']:
            self.assertFalse(gsc.authorized_property({'siteUrl': site, 'permissionLevel': 'siteOwner'}))
        self.assertFalse(gsc.authorized_property({'siteUrl': 'sc-domain:arquindex.com.br', 'permissionLevel': 'siteUnverifiedUser'}))

    def test_missing_secrets_never_calls_oauth(self):
        with patch.dict(gsc.os.environ, {}, clear=True), patch.object(gsc, 'oauth_token') as oauth:
            with self.assertRaisesRegex(RuntimeError, 'GSC_NOT_CONFIGURED'):
                gsc.main()
            oauth.assert_not_called()

    def run_fixture(self, directory, response):
        with patch.dict(gsc.os.environ, {name: 'offline-test-placeholder' for name in ('GSC_CLIENT_ID', 'GSC_CLIENT_SECRET', 'GSC_REFRESH_TOKEN')}, clear=True), patch.object(gsc, '__file__', str(Path(directory) / 'collect_gsc.py')), patch.object(gsc, 'oauth_token', return_value='offline-test-placeholder'), patch.object(gsc, 'request_json', side_effect=[{'siteEntry': [{'siteUrl': 'sc-domain:arquindex.com.br', 'permissionLevel': 'siteOwner'}]}, response]):
            gsc.main()

    def test_api_failure_preserves_previous_data_and_redacts_error(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'gsc-real.json'
            output.write_text('previous-verified-data')
            with self.assertRaisesRegex(RuntimeError, 'GSC_PROPERTY_READ_FAILED') as error:
                self.run_fixture(directory, urllib.error.HTTPError('https://example.invalid/', 403, 'private-error-content', {}, None))
            self.assertNotIn('private-error-content', str(error.exception))
            self.assertEqual(output.read_text(), 'previous-verified-data')

    def test_success_replaces_data_after_complete_response(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            self.run_fixture(directory, {'rows': [{'keys': ['offline-query', 'https://www.arquindex.com.br/'], 'clicks': 1, 'impressions': 2}]})
            output = json.loads((Path(directory) / 'gsc-real.json').read_text())
            self.assertEqual(len(output['rows']), 1)
            self.assertEqual(output['properties'][0]['rows'], 1)
            self.assertFalse((Path(directory) / 'gsc-real.json.tmp').exists())

if __name__ == '__main__':
    unittest.main()
