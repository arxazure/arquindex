import unittest
import tempfile
from pathlib import Path
from scripts.seo_canonical_review import analyze, classify, read_export

class CanonicalReviewTests(unittest.TestCase):
    def test_target_fourxx_explicit(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","https://www.arquindex.com.br/b","404"),"canonical_4xx_confirm_in_live")
    def test_generic_httpcode_not_target(self):
        result=analyze([{"URL":"https://www.arquindex.com.br/a","Canonical":"https://www.arquindex.com.br/b","HTTP Code":"404"}])
        self.assertEqual(result["findings"][0]["target_http_status_from_export"],"")
        self.assertEqual(result["findings"][0]["source_http_status_from_export"],"")
        self.assertEqual(result["findings"][0]["category"],"verify_live_status")
    def test_explicit_ahrefs_target_alias_and_source_status(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ahrefs.csv"
            path.write_text(
                "\ufeffURL,Canonical URL,Source HTTP status code,Canonical URL status code\n"
                "https://www.arquindex.com.br/a,https://www.arquindex.com.br/b,404,410\n",
                encoding="utf-8",
            )
            finding = read_export(path)["findings"][0]
        self.assertEqual(finding["source_http_status_from_export"], "404")
        self.assertEqual(finding["target_http_status_from_export"], "410")
        self.assertEqual(finding["category"], "canonical_4xx_confirm_in_live")
    def test_other_host_requires_review(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","https://foo.arquindex.com.br/b","404"),"cross_host_manual_review")
    def test_no_url_or_canonical(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","",""),"missing_evidence")
    def test_http_canonical(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","http://www.arquindex.com.br/a",""),"http_canonical_review")
    def test_reject_unsafe_urls(self):
        self.assertEqual(classify("https://user@www.arquindex.com.br/a","https://www.arquindex.com.br/b","404"),"invalid_page_url")
        self.assertEqual(classify("https://www.arquindex.com.br/a","https://www.arquindex.com.br:8443/b","404"),"invalid_canonical")
        self.assertEqual(classify("https://example.com/a","https://example.com/b","404"),"source_host_manual_review")
if __name__=="__main__":
    unittest.main()
