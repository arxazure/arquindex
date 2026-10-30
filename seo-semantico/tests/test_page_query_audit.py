import unittest
from page_query_audit import analyze
class PageQueryTests(unittest.TestCase):
 def test_overlap_not_automatic_duplicate(self):
  rows=[dict(query="assessoria lgpd",page="https://a.arquindex.com.br/",clicks="0",impressions="2",position="10"),
        dict(query="assessoria lgpd",page="https://b.arquindex.com.br/",clicks="0",impressions="1",position="20")]
  report=analyze(rows)
  self.assertEqual(len(report["query_page_overlaps"]),1)
  self.assertEqual(report["query_page_overlaps"][0]["page_count"],2)
 def test_bad_rows_ignored(self):
  self.assertEqual(analyze([dict(query="alfresco",page="https://x/",clicks="bad")])["rows_read"],0)
if __name__=="__main__":unittest.main()
