import tempfile
import unittest
from pathlib import Path
from scripts.seo_authority_preflight import audit

class AuthorityPreflightTests(unittest.TestCase):
    def check(self, html):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "sample.html"
            path.write_text(html, encoding="utf-8")
            return audit(path)["issues"]

    def test_external_imitation_not_counted(self):
        issues = self.check('<title>SEO</title><h1>SEO</h1><a href="https://notarquindex.com.br/x">Link</a>')
        self.assertIn("cross_property_links_review", issues)

    def test_real_subdomain_counted(self):
        issues = self.check('<title>SEO</title><h1>SEO</h1><a href="https://ecm.arquindex.com.br/custo.html">ECM</a>')
        self.assertNotIn("cross_property_links_review", issues)

    def test_noindex_is_flagged(self):
        issues = self.check('<title>SEO</title><h1>SEO</h1><meta name="robots" content="noindex,follow">')
        self.assertIn("noindex_review", issues)

    def test_canonical_requires_https(self):
        issues = self.check('<title>SEO</title><h1>SEO</h1><link rel="canonical" href="http://arquindex.com.br/test">')
        self.assertIn("canonical_not_absolute_https", issues)

if __name__ == "__main__":
    unittest.main()
