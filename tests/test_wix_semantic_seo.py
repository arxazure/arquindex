"""Offline regression tests for the Semantic SEO job (no credentials/network)."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import wix_semantic_seo as seo


class SemanticSeoTests(unittest.TestCase):
    def test_missing_secrets_produces_diagnostic_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(seo, "OUTPUT_DIR", Path(tmp)), patch.dict(
                seo.os.environ,
                {"GOOGLE_API_KEY": "", "GOOGLE_CX_ID": "", "OPENAI_API_KEY": "",
                 "WIX_CREATE_DRAFT": "false"},
            ), patch.object(seo, "search") as search:
                with self.assertRaisesRegex(RuntimeError, "Missing GitHub Actions secrets"):
                    seo.main()
                search.assert_not_called()
                report = json.loads((Path(tmp) / "diagnostic.json").read_text())
                self.assertEqual(report["status"], "configuration_error")
                self.assertIn("OPENAI_API_KEY", report["missing_secret_names"])

    def test_wix_credentials_required_only_when_draft_enabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(seo, "OUTPUT_DIR", Path(tmp)), patch.dict(
                seo.os.environ,
                {"GOOGLE_API_KEY": "test", "GOOGLE_CX_ID": "test",
                 "OPENAI_API_KEY": "test", "WIX_API_KEY": "", "WIX_SITE_ID": "",
                 "WIX_CREATE_DRAFT": "true"},
            ), patch.object(seo, "search") as search:
                with self.assertRaisesRegex(RuntimeError, "WIX_API_KEY"):
                    seo.main()
                search.assert_not_called()

    def test_markdown_conversion_produces_heading_and_paragraph(self):
        nodes = seo.wix_nodes("# Heading\n\nBody text")
        self.assertEqual([node["type"] for node in nodes],
                         ["HEADING", "PARAGRAPH"])


if __name__ == "__main__":
    unittest.main()
