import unittest
from audit import parse_html

class AuditTests(unittest.TestCase):
 def test_nested_h1_and_internal_anchor(self):
  html = '<html><head><title>Digitalização</title><meta name="description" content="Teste"><link rel="canonical" href="/servico/"></head><body><h1>Gestão <em>documental</em></h1><a href="/contato">Orçamento</a><p>' + ('digitalização ' * 160) + '</p></body></html>'
  result = parse_html(html, "https://www.arquindex.com.br/servico/")
  self.assertEqual(result["h1"], ["Gestão documental"])
  self.assertEqual(result["internal_links"], 1)
  self.assertEqual(result["canonical"], "https://www.arquindex.com.br/servico/")
  self.assertNotIn("thin_content_review", result["issues"])
 def test_missing_metadata(self):
  result = parse_html("<html><body>Teste</body></html>", "https://www.arquindex.com.br/")
  self.assertIn("missing_title", result["issues"])
  self.assertIn("missing_canonical", result["issues"])
 def test_external_canonical(self):
  result = parse_html('<link rel="canonical" href="https://other.example/a">', "https://www.arquindex.com.br/")
  self.assertIn("external_canonical_review", result["issues"])
if __name__ == "__main__": unittest.main()
