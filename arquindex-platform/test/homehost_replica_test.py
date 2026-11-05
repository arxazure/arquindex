"""Run with python3 -m unittest discover -s arquindex-platform/test -p '*_test.py'.

Requires PHP CLI. The real entrypoint runs under php -n with cURL stubbed at
the network boundary, so tests never contact the production origin.
"""
import json
from pathlib import Path
import subprocess
import unittest
from urllib.parse import urlsplit

ENTRYPOINT = Path(__file__).resolve().parents[1] / "homehost-replica/index.php"
ORIGIN = "https://arquindex-gestao-documental.arquindex.chatgpt.site"
BASE = "/gestao-documental"
KEY = "a948be82c7824bc989f2c5dd0f071bea"
HARNESS = r"""
$input = json_decode(stream_get_contents(STDIN), true);
$_SERVER = [
    'REQUEST_URI' => $input['uri'],
    'QUERY_STRING' => $input['query'] ?? '',
    'REQUEST_METHOD' => $input['method'] ?? 'GET',
];
$capturedUrl = null;
foreach (['CURLOPT_RETURNTRANSFER', 'CURLOPT_FOLLOWLOCATION', 'CURLOPT_MAXREDIRS',
    'CURLOPT_CONNECTTIMEOUT', 'CURLOPT_TIMEOUT', 'CURLOPT_USERAGENT',
    'CURLOPT_ENCODING', 'CURLINFO_RESPONSE_CODE', 'CURLINFO_CONTENT_TYPE'] as $i => $name) {
    define($name, $i + 1);
}
function curl_init($url) { $GLOBALS['capturedUrl'] = $url; return true; }
function curl_setopt_array($handle, $options) { return true; }
function curl_exec($handle) { return $GLOBALS['input']['upstream_body'] ?? '<a href="/orcamento">Orçamento</a>'; }
function curl_getinfo($handle, $option) {
    return $option === CURLINFO_RESPONSE_CODE ? 200 : ($GLOBALS['input']['content_type'] ?? 'text/html; charset=utf-8');
}
function curl_error($handle) { return ''; }
function curl_close($handle) {}
ob_start();
register_shutdown_function(function () {
    $body = ob_get_clean();
    echo json_encode([
        'status' => http_response_code() ?: 200,
        'url' => $GLOBALS['capturedUrl'],
        'body' => $body,
    ], JSON_UNESCAPED_SLASHES);
});
require $argv[1];
"""


class HomehostReplicaTest(unittest.TestCase):
    def request(self, uri, **options):
        result = subprocess.run(
            ["php", "-n", "-r", HARNESS, str(ENTRYPOINT)],
            input=json.dumps({"uri": uri, **options}), text=True,
            capture_output=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_malicious_suffixes_rejected_before_curl(self):
        for suffix in [
            "@evil.com/", ".evil.com/", "-extra/", "0", "%2fblog", "%40evil.com/",
            "/@evil.com/", "/blog/user@evil.com", "/\\evil.com/", "\\evil.com/",
            "//evil.com/", "///evil.com/", "/%40evil.com/", "/%5cevil.com/",
            "/%5Cevil.com/", "/%2fevil.com/", "/%2Fevil.com/", "/%2f%2fevil.com/",
            "/%00", "/%0d%0aHost%3Aevil.com", "/%7f", "/bad%", "/bad%2", "/bad%ZZ",
            "/bad\x00path", "/bad\r\npath", "/bad path",
        ]:
            with self.subTest(suffix=suffix):
                result = self.request(BASE + suffix)
                self.assertEqual(result, {"status": 400, "url": None, "body": ""})

    def test_invalid_request_targets_rejected_before_curl(self):
        for uri in ["", "//evil.com/gestao-documental/",
                    "https://evil.com/gestao-documental/", "//[invalid", "*"]:
            with self.subTest(uri=uri):
                result = self.request(uri)
                self.assertEqual(result["status"], 400)
                self.assertIsNone(result["url"])

    def test_legitimate_routes_and_response_rewrite(self):
        for suffix in ["", "/", "/blog", "/blog/lgpd-governanca",
                       "/_next/static/app.js", "/robots.txt", "/sitemap.xml",
                       "/feed.xml", "/api/orcamento",
                       "/arquivos/gest%C3%A3o%20documental.pdf",
                       "/arquivos/100%25.pdf", "/0"]:
            with self.subTest(suffix=suffix):
                result = self.request(BASE + suffix)
                self.assertEqual(result["status"], 200)
                self.assertEqual(result["url"], ORIGIN + (suffix or "/"))
                upstream = urlsplit(result["url"])
                self.assertEqual(upstream.netloc, urlsplit(ORIGIN).netloc)
                self.assertIsNone(upstream.username)
                self.assertIn("Orçamento", result["body"])
                self.assertIn(BASE + "/orcamento", result["body"])

    def test_query_remains_query_data_on_fixed_origin(self):
        query = "q=a%20b&email=user%40evil.com&next=https%3A%2F%2Fevil.com%2F"
        result = self.request(BASE + "/blog?" + query, query=query)
        self.assertEqual(result["url"], ORIGIN + "/blog?" + query)
        self.assertEqual(urlsplit(result["url"]).netloc, urlsplit(ORIGIN).netloc)

    def test_all_500_city_canonicals_and_links(self):
        inventory = json.loads((ENTRYPOINT.parents[1] / "test/fixtures/regional-city-paths.json").read_text())
        self.assertEqual(len(inventory["paths"]), 500)
        for path in inventory["paths"]:
            with self.subTest(path=path):
                body = '<link rel="canonical" href="' + ORIGIN + path + '"><h1>Cidade</h1><a href="' + path + '">Cidade</a>'
                result = self.request(BASE + path, upstream_body=body)
                self.assertEqual(result["status"], 200)
                self.assertEqual(result["body"], '<link rel="canonical" href="https://www.arquindex.com.br' + BASE + path + '"><h1>Cidade</h1><a href="' + BASE + path + '">Cidade</a>')

    def test_city_sitemap_preserves_xml_and_all_locations(self):
        paths = json.loads((ENTRYPOINT.parents[1] / "test/fixtures/regional-city-paths.json").read_text())["paths"]
        xml = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + ORIGIN + p + '</loc></url>' for p in paths) + '</urlset>'
        result = self.request(BASE + '/sitemap-cidades.xml', upstream_body=xml, content_type='application/xml')
        self.assertEqual(result["body"], xml.replace(ORIGIN, 'https://www.arquindex.com.br' + BASE))

    def test_malformed_brasilia_redirects_before_upstream(self):
        path = BASE + '/brasil/centro-oeste/df/gestao-documental/brasilia'
        for method in ('GET', 'HEAD'):
            result = self.request(path, method=method, query='utm_source=test')
            self.assertEqual(result["status"], 301)
            self.assertIsNone(result["url"])
            self.assertEqual(result["body"], '')

    def test_head_body_is_empty(self):
        result = self.request(BASE + "/blog", method="HEAD")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["url"], ORIGIN + "/blog")
        self.assertEqual(result["body"], "")

    def test_unrelated_path_stays_404(self):
        result = self.request("/outro/blog")
        self.assertEqual(result["status"], 404)
        self.assertIsNone(result["url"])

    def test_local_health_check(self):
        result = self.request(BASE + "/_health")
        self.assertEqual(result["status"], 200)
        self.assertIsNone(result["url"])
        self.assertTrue(json.loads(result["body"])["ok"])

    def test_local_indexnow_verification(self):
        result = self.request(BASE + "/" + KEY + ".txt")
        self.assertEqual(result["status"], 200)
        self.assertIsNone(result["url"])
        self.assertEqual(result["body"], KEY)


if __name__ == "__main__":
    unittest.main()
