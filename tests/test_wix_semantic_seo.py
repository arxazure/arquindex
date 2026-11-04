"""Offline tests: no API calls or real credentials."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('wix_seo', Path(__file__).resolve().parents[1] / 'scripts/wix_semantic_seo.py')
seo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo)

class SemanticTests(unittest.TestCase):
    def test_missing_and_whitespace_credentials_make_no_requests(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(seo, 'OUTPUT_DIR', Path(directory)), patch.dict(seo.os.environ, {'GOOGLE_API_KEY': '  '}, clear=True), patch.object(seo.session, 'get') as get, patch.object(seo.session, 'post') as post, patch.object(seo, 'research') as generate:
            self.assertEqual(seo.main(), 2)
            get.assert_not_called()
            post.assert_not_called()
            generate.assert_not_called()
            status = json.loads((Path(directory) / 'status.json').read_text())
            self.assertEqual(status['code'], 'SEO_NOT_CONFIGURED')
            self.assertIn('GOOGLE_API_KEY', status['missing'])

    def test_failure_preserves_research_and_redacts_exception(self):
        env = {key: 'offline-placeholder' for key in ['GOOGLE_API_KEY', 'GOOGLE_CX_ID', 'OPENAI_API_KEY']}
        with tempfile.TemporaryDirectory() as directory, patch.object(seo, 'OUTPUT_DIR', Path(directory)), patch.dict(seo.os.environ, env, clear=True), patch.object(seo, 'search', return_value=[{'url': 'https://example.org'}]) as search, patch.object(seo, 'research', side_effect=RuntimeError('secret-marker')):
            self.assertEqual(seo.main(), 1)
            self.assertEqual(len(list(Path(directory).glob('*.research.json'))), 1)
            self.assertNotIn('secret-marker', (Path(directory) / 'status.json').read_text())
            self.assertEqual(seo.main(), 1)
            self.assertEqual(search.call_count, 1)

    def test_wix_failure_keeps_local_draft_and_prevents_duplicate(self):
        env = {key: 'offline-placeholder' for key in ['GOOGLE_API_KEY', 'GOOGLE_CX_ID', 'OPENAI_API_KEY', 'WIX_API_KEY', 'WIX_SITE_ID']}
        env['WIX_CREATE_DRAFT'] = 'true'
        with tempfile.TemporaryDirectory() as directory, patch.object(seo, 'OUTPUT_DIR', Path(directory)), patch.dict(seo.os.environ, env, clear=True), patch.object(seo, 'search', return_value=[{'url': 'https://example.org'}]), patch.object(seo, 'research', return_value={'title': 'Offline draft'}), patch.object(seo, 'create_wix_draft', side_effect=RuntimeError('secret-marker')) as draft:
            self.assertEqual(seo.main(), 1)
            day = seo.datetime.now(seo.timezone.utc).strftime('%Y-%m-%d')
            report = (Path(directory) / f'{day}.json').read_bytes()
            self.assertEqual(seo.main(), 3)
            self.assertEqual((Path(directory) / f'{day}.json').read_bytes(), report)
            self.assertEqual(draft.call_count, 1)

    def test_local_generation_does_not_require_wix_keys(self):
        env = {key: 'offline-placeholder' for key in ['GOOGLE_API_KEY', 'GOOGLE_CX_ID', 'OPENAI_API_KEY']}
        with tempfile.TemporaryDirectory() as directory, patch.object(seo, 'OUTPUT_DIR', Path(directory)), patch.dict(seo.os.environ, env, clear=True), patch.object(seo, 'search', return_value=[{'url': 'https://example.org'}]), patch.object(seo, 'research', return_value={'title': 'Offline draft'}), patch.object(seo, 'create_wix_draft') as draft:
            self.assertEqual(seo.main(), 0)
            draft.assert_not_called()
            status = json.loads((Path(directory) / 'status.json').read_text())
            self.assertEqual(status['publication'], 'not_attempted')
            self.assertEqual(status['indexation'], 'not_verified')
