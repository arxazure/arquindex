"""Regression tests for the repository-only Ahrefs audit (no network calls)."""
import tempfile
import unittest
from pathlib import Path

from scripts.ahrefs_seo_audit import audit, normalized_url, page_url


class SeoAuditTests(unittest.TestCase):
    def test_index_variants_resolve_to_same_page(self):
        self.assertEqual(
            normalized_url("https://www.arquindex.com.br/guias/index.html"),
            "https://www.arquindex.com.br/guias/",
        )
        self.assertEqual(
            normalized_url("https://arquindex.com.br/guias/?utm_source=test#section"),
            "https://www.arquindex.com.br/guias/",
        )

    def test_reject_external_links(self):
        self.assertIsNone(normalized_url("https://example.com/guias/"))
        self.assertIsNone(normalized_url("javascript:alert(1)"))

    def test_nested_index_path(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(page_url(root / "guias" / "index.html", root),
                             "https://www.arquindex.com.br/guias/")

    def test_incoming_links_and_html_diagnostics(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "guias").mkdir()
            (root / "index.html").write_text(
                '<html><head><title>Arquindex</title><meta name="description" '
                'content="Institucional"></head><body><h1>Início</h1>'
                '<a href="/guias/">Guias</a></body></html>', encoding="utf-8")
            (root / "guias" / "index.html").write_text(
                '<html><head><title>Guias</title></head>'
                '<body><h1>Primeiro</h1><h1>Segundo</h1></body></html>',
                encoding="utf-8")
            result = audit(root, 100)
            self.assertEqual(result["pages_scanned"], 2)
            pages = {p["url"]: p for p in result["pages"]}
            child = pages["https://www.arquindex.com.br/guias/"]
            self.assertEqual(child["incoming_internal_links"], 1)
            self.assertNotIn("orphan_within_scanned_files_review", child["issues"])
            self.assertIn("meta_description_missing", child["issues"])
            self.assertIn("multiple_h1", child["issues"])
            self.assertEqual(child["og_missing_tags"], ["og:title", "og:description", "og:url", "og:image"])

    def test_true_orphan_within_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "index.html").write_text("<h1>Home</h1>", encoding="utf-8")
            (root / "unused.html").write_text("<h1>Unused</h1>", encoding="utf-8")
            result = audit(root, 100)
            unused = next(p for p in result["pages"] if p.get("url", "").endswith("/unused.html"))
            self.assertIn("orphan_within_scanned_files_review", unused["issues"])


    def test_file_cap_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.html").write_text("<html><h1>A</h1></html>", encoding="utf-8")
            (root / "b.html").write_text("<html><h1>B</h1></html>", encoding="utf-8")
            result = audit(root, 1)
            self.assertTrue(result["scan_limit_reached"])
            self.assertEqual(result["pages_scanned"], 1)
            self.assertEqual(result["pages"][0]["file"], "a.html")


if __name__ == "__main__":
    unittest.main()
