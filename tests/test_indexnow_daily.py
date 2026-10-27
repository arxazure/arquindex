import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('daily', Path(__file__).resolve().parents[1] / 'scripts/indexnow_daily.py')
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)


class IndexNowTests(unittest.TestCase):
    def test_exact_host_boundary(self):
        self.assertTrue(daily.valid_url('https://a.arquindex.com.br/test', 'a.arquindex.com.br'))
        for url in ['https://a.arquindex.com.br.evil.com/', 'https://a.arquindex.com.br@evil.com/',
                    'https://b.arquindex.com.br/', 'http://a.arquindex.com.br/',
                    'https://a.arquindex.com.br/#x']:
            self.assertFalse(daily.valid_url(url, 'a.arquindex.com.br'))

    def run_host(self, code, old=None):
        host, url = 'a.arquindex.com.br', 'https://a.arquindex.com.br/'
        submissions = []
        def fake_request(target, payload=None):
            if payload:
                submissions.append(payload)
                return code, b'', {}
            return 200, b'changed content', {}
        with patch.object(daily, 'key_for', return_value=('12345678', 'https://' + host + '/indexnow-key.txt')), \
             patch.object(daily, 'discover', return_value=[url]), \
             patch.object(daily, 'robots_for', return_value=type('Robots', (), {'can_fetch': lambda *args: True})()), \
             patch.object(daily, 'request', side_effect=fake_request):
            report, state = daily.process_host(host, old or {})
        return report, state, submissions

    def test_received_200_persists_hash_and_deduplicates(self):
        report, state, sent = self.run_host(200)
        self.assertEqual(report['received_200'], 1)
        self.assertEqual(sent[0]['host'], 'a.arquindex.com.br')
        self.assertEqual(len(state), 1)
        report, state, sent = self.run_host(200, state)
        self.assertEqual(report['unchanged'], 1)
        self.assertEqual(sent, [])

    def test_202_keeps_url_pending_for_next_run(self):
        report, state, _ = self.run_host(202)
        self.assertEqual(report['pending_202'], 1)
        self.assertEqual(state, {})

    def test_failed_submission_does_not_mark_received(self):
        report, state, _ = self.run_host(403)
        self.assertTrue(report['errors'])
        self.assertEqual(state, {})

    def test_missing_key_blocks_only_that_host(self):
        with patch.object(daily, 'key_for', side_effect=ValueError('missing key')), \
             patch.object(daily, 'discover', return_value=['https://a.arquindex.com.br/']), \
             patch.object(daily, 'request') as request:
            report, state = daily.process_host('a.arquindex.com.br', {})
        self.assertTrue(report['errors'])
        request.assert_not_called()

    def test_cross_host_sitemap_is_rejected(self):
        with patch.object(daily, 'request', return_value=(200,
                b'<urlset><url><loc>https://evil.com/</loc></url></urlset>', {})):
            with self.assertRaises(ValueError):
                daily.discover('a.arquindex.com.br')

    def test_apex_www_alias_is_not_an_error_or_submission(self):
        with patch.object(daily, 'request', return_value=(200,
                b'<urlset><url><loc>https://www.arquindex.com.br/</loc></url></urlset>', {})):
            report, state = daily.process_host('arquindex.com.br', {})
        self.assertEqual(report['status'], 'delegated_to_www')
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['batches'], [])

    def test_noindex_canonical_and_header_guards(self):
        url = 'https://a.arquindex.com.br/'
        good = b'<html><link rel="canonical" href="https://a.arquindex.com.br/"></html>'
        self.assertIsNone(daily.exclusion_reason(url, good, {}))
        self.assertEqual(daily.exclusion_reason(url, good, {'X-Robots-Tag': 'noindex'}), 'x_robots_noindex')
        self.assertEqual(daily.exclusion_reason(url, good.replace(b'</html>', b'<meta name="robots" content="noindex"></html>'), {}), 'meta_noindex')
        self.assertEqual(daily.exclusion_reason(url, good.replace(b'a.arquindex', b'b.arquindex'), {}), 'canonical_points_elsewhere')
        self.assertEqual(daily.exclusion_reason(url, b'<html></html>', {}), 'canonical_missing_or_multiple')

    def test_dns_error_is_classified(self):
        import socket
        import urllib.error
        self.assertEqual(daily.error_code(urllib.error.URLError(socket.gaierror(-2, 'not found'))), 'dns')


if __name__ == '__main__':
    unittest.main()
