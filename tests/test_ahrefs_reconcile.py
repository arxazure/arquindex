"""Offline checks for exact-match Ahrefs issue reconciliation."""
import tempfile
import unittest
from pathlib import Path

from scripts.ahrefs_reconcile import classify_issue, load_csv, normalize, reconcile, URL_HEADERS, ISSUE_HEADERS


class AhrefsReconcileTests(unittest.TestCase):
    def test_keep_path_query_and_trailing_slash(self):
        self.assertNotEqual(normalize("https://www.arquindex.com.br/faq/"),
                            normalize("https://www.arquindex.com.br/faq"))
        self.assertEqual(normalize("HTTPS://WWW.ARQUINDEX.COM.BR/faq/?x=1#top"),
                         "https://www.arquindex.com.br/faq/?x=1")

    def test_not_force_www_for_other_hosts(self):
        self.assertNotEqual(normalize("https://ecm.arquindex.com.br/a"),
                            normalize("https://www.arquindex.com.br/a"))

    def test_external_issue_remains_manual(self):
        self.assertIsNone(classify_issue("Slow page"))
        self.assertIsNone(classify_issue("Changed pages not submitted to IndexNow"))

    def test_match_requires_live_verification(self):
        result = reconcile(
            [("https://www.arquindex.com.br/faq/", "Meta description tag missing or empty")],
            [("https://www.arquindex.com.br/faq/", "meta_description_missing")])
        self.assertEqual(result["rows"][0]["status"], "MATCH_REQUIRES_LIVE_VERIFICATION")

    def test_different_host_unmatched(self):
        result = reconcile(
            [("https://ecm.arquindex.com.br/faq/", "Meta description tag missing")],
            [("https://www.arquindex.com.br/faq/", "meta_description_missing")])
        self.assertEqual(result["rows"][0]["status"], "NO_EXACT_LOCAL_MATCH")

    def test_missing_column_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "in.csv"
            path.write_text("Affected URL,Other Column\nhttps://example.com,foo\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_csv(path, (URL_HEADERS, ISSUE_HEADERS))


if __name__ == "__main__":
    unittest.main()
