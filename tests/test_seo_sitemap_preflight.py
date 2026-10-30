import tempfile
import unittest
from pathlib import Path
from scripts.seo_sitemap_preflight import inspect

class SitemapPreflightTests(unittest.TestCase):
    def check(self, xml):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'sitemap.xml'
            path.write_text(xml, encoding='utf-8')
            return inspect(path)

    def test_valid_local_urls(self):
        r = self.check('<urlset><url><loc>https://www.arquindex.com.br/guarda</loc></url></urlset>')
        self.assertEqual(r['issues'], [])
        self.assertEqual(r['urls'], 1)

    def test_outside_domain(self):
        r = self.check('<urlset><url><loc>https://arquindex.com.br.example.net/page</loc></url></urlset>')
        self.assertIn('outside_arq_domain', r['issues'])

    def test_duplicate(self):
        r = self.check('<urlset><url><loc>https://arquindex.com.br/a</loc></url><url><loc>https://arquindex.com.br/a</loc></url></urlset>')
        self.assertIn('duplicate_loc', r['issues'])

    def test_non_https(self):
        r = self.check('<urlset><url><loc>http://www.arquindex.com.br/a</loc></url></urlset>')
        self.assertIn('invalid_absolute_https_loc', r['issues'])

    def test_invalid_xml(self):
        r = self.check('<urlset><url>')
        self.assertTrue(any(x.startswith('invalid_xml_or_file:') for x in r['issues']))

if __name__ == '__main__':
    unittest.main()
