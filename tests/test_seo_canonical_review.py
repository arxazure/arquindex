import unittest
from scripts.seo_canonical_review import analyze, classify

class CanonicalReviewTests(unittest.TestCase):
    def test_target_fourxx_explicit(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","https://www.arquindex.com.br/b","404"),"canonical_4xx_confirm_in_live")
    def test_generic_httpcode_not_target(self):
        result=analyze([{"URL":"https://www.arquindex.com.br/a","Canonical":"https://www.arquindex.com.br/b","HTTP Code":"404"}])
        self.assertEqual(result["findings"][0]["target_http_status_from_export"],"")
        self.assertEqual(result["findings"][0]["category"],"verify_live_status")
    def test_other_host_requires_review(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","https://foo.arquindex.com.br/b","404"),"cross_host_manual_review")
    def test_no_url_or_canonical(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","",""),"missing_evidence")
    def test_http_canonical(self):
        self.assertEqual(classify("https://www.arquindex.com.br/a","http://www.arquindex.com.br/a",""),"http_canonical_review")
if __name__=="__main__":
    unittest.main()
