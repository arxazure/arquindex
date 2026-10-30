import unittest
from gsc_opportunities import classify,prioritize

class OpportunitiesTests(unittest.TestCase):
 def test_classification(self):
  self.assertEqual(classify("serviço de digitalização de documentos"),"digitalizacao")
  self.assertEqual(classify("consultoria LGPD"),"lgpd")
  self.assertIsNone(classify("receita culinária"))
 def test_minimum(self):
  rows=[{"query":"digitalização de documentos","impressions":"102","clicks":"1","position":"27.25"},
        {"query":"DPO terceirizado","impressions":"2","clicks":"0","position":"10"}]
  result=prioritize(rows)
  self.assertEqual(len(result),1)
  self.assertEqual(result[0]["tier"],"needs_foundation")
 def test_skip_bad_numbers(self):
  self.assertEqual(prioritize([{"query":"Alfresco ECM","impressions":"bad","position":"11"}]),[])
if __name__=="__main__":unittest.main()
