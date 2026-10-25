import json
import socket
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import indexnow_preflight as preflight


class PreflightTests(unittest.TestCase):
    def test_dns_failure_does_not_attempt_http(self):
        with patch.object(preflight.socket, 'getaddrinfo', side_effect=socket.gaierror(-2, 'missing')), \
             patch.object(preflight.daily, 'request') as request:
            result = preflight.check_host('missing.arquindex.com.br')
        self.assertEqual(result['errors'][0]['code'], 'dns')
        self.assertEqual(result['sitemap'], 'unchecked')
        request.assert_not_called()

    def test_http_404_has_stage_and_sitemap_is_still_checked(self):
        http = urllib.error.HTTPError('https://a.arquindex.com.br/indexnow-key.txt', 404, '', {}, None)
        failure = RuntimeError('HTTP 404')
        failure.__cause__ = http
        with patch.object(preflight.socket, 'getaddrinfo', return_value=[(0, 0, 0, '', ('192.0.2.1', 443))]), \
             patch.object(preflight.daily, 'key_for', side_effect=failure), \
             patch.object(preflight.daily, 'discover', return_value=['https://a.arquindex.com.br/']) as discover:
            result = preflight.check_host('a.arquindex.com.br')
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['errors'][0]['stage'], 'key')
        self.assertEqual(result['errors'][0]['code'], 'http_404')
        self.assertEqual(result['sitemap'], 'ok')
        discover.assert_called_once()

    def test_ready_host_makes_only_get_requests(self):
        calls = []
        def get(url, payload=None):
            self.assertIsNone(payload, 'preflight must never POST')
            self.assertNotEqual(url, preflight.daily.ENDPOINT)
            calls.append(url)
            if url.endswith('/indexnow-key.txt'):
                return 200, b'abcdefgh12345678', {}
            return 200, b'<urlset><url><loc>https://a.arquindex.com.br/</loc></url></urlset>', {}
        with patch.object(preflight.socket, 'getaddrinfo', return_value=[(0, 0, 0, '', ('192.0.2.1', 443))]), \
             patch.object(preflight.daily, 'request', side_effect=get):
            result = preflight.check_host('a.arquindex.com.br')
        self.assertEqual(result['status'], 'ready_for_page_checks')
        self.assertEqual(len(calls), 2)
        self.assertNotIn('abcdefgh12345678', json.dumps(result))

    def test_report_preserves_receipts_and_records_blocked_hosts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            state = root / 'accepted.json'
            state.write_bytes(b'{"existing":"receipt"}')
            result = {'host': 'a.arquindex.com.br', 'status': 'blocked', 'dns': [],
                      'key': 'unchecked', 'sitemap': 'unchecked', 'pages_in_sitemap': 0,
                      'errors': [{'stage': 'dns', 'code': 'dns', 'error': 'missing'}]}
            with patch.object(preflight, 'OUT', root / 'report'), \
                 patch.object(preflight.daily, 'STATE', state), \
                 patch.object(preflight.daily, 'hosts_from_repository', return_value=[result['host']]), \
                 patch.object(preflight, 'check_host', return_value=result), \
                 patch.dict(preflight.os.environ, {'GITHUB_STEP_SUMMARY': str(root / 'summary')}):
                preflight.main()
            report = json.loads((root / 'report/report.json').read_text())
            self.assertEqual(state.read_bytes(), b'{"existing":"receipt"}')
            self.assertFalse(report['submitted'])
            self.assertEqual(report['blocked_hosts'], 1)
            self.assertEqual(report['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
