import unittest
from scripts.seo_priority_queue import prioritize

class PriorityQueueTests(unittest.TestCase):
    def test_canonical_ranks_above_author_review(self):
        html = {"pages": [
            {"path": "article.html", "issues": ["author_attribution_review"]},
            {"path": "service.html", "issues": ["canonical_count_0"]},
        ]}
        result = prioritize(html, {"inventories": []})
        self.assertEqual(result["queue"][0]["source"], "service.html")
        self.assertEqual(result["count"], 2)

    def test_no_issues_has_empty_queue(self):
        result = prioritize({"pages": [{"path": "ok.html", "issues": []}]},
                            {"inventories": [{"file": "sitemap.xml", "issues": []}]})
        self.assertEqual(result["count"], 0)

    def test_sitemap_error_prioritized(self):
        result = prioritize({"pages": [{"path": "x.html", "issues": ["missing_title"]}]},
                            {"inventories": [{"file": "sitemap.xml", "issues": ["invalid_xml_or_file: bad"]}]})
        self.assertEqual(result["queue"][0]["kind"], "sitemap")

if __name__ == "__main__":
    unittest.main()
