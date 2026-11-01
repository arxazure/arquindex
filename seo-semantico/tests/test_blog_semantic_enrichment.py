import unittest
from blog_semantic_enrichment import choose_terms,proposals
class BlogSemanticTests(unittest.TestCase):
 def test_contextual_not_keyword_stuffing(self):
  a={"title":"OCR em digitalização documental","body":"O processo de digitalização empresarial envolve documentos.","url":"https://arquindex.com.br/blog/a"}
  r={"seed_topics":["OCR pesquisável","receita de bolo","digitalização certificada"]}
  selected=choose_terms(a,r)
  self.assertIn("digitalização certificada",selected)
  self.assertNotIn("receita de bolo",selected)
 def test_preserves_original(self):
  a={"title":"LGPD nas empresas","description":"Resumo original","body":"LGPD e tratamento de dados","url":"https://arquindex.com.br/blog/lgpd"}
  result=proposals(a,{"seed_topics":["LGPD corporativa"]})
  self.assertEqual(result["current_description"],"Resumo original")
  self.assertTrue(result["approval_required"])
if __name__=="__main__":unittest.main()
