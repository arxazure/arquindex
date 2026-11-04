import unittest
from daily_health import summarize, markdown


class DailyHealthTests(unittest.TestCase):
    def test_prioritizes_availability_and_noindex(self):
        data = {"results": [
            {"url": "https://www.arquindex.com.br/", "status": 200, "issues": []},
            {"url": "https://www.arquindex.com.br/guia/", "status": 200, "issues": ["noindex", "missing_description"]},
            {"url": "https://www.arquindex.com.br/erro/", "status": 404, "error": "HTTP 404"},
        ]}
        summary = summarize(data)
        self.assertEqual(summary["audited"], 3)
        self.assertEqual(summary["http_200"], 2)
        self.assertEqual(summary["unavailable"], 1)
        self.assertEqual(summary["by_priority"]["critical"], 2)
        self.assertEqual(summary["by_priority"]["ok"], 1)
        self.assertEqual(summary["issues"]["noindex"], 1)

    def test_report_does_not_claim_ranking_or_publication(self):
        summary = summarize({"results": [{"url": "https://arquindex.com.br/", "status": 200}]})
        report = markdown(summary)
        self.assertIn("não mede indexação", report)
        self.assertIn("não publica alterações", report)

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            summarize({})


if __name__ == "__main__":
    unittest.main()
