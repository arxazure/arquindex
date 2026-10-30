import json
import unittest
from generate_schema import build
class SchemaTests(unittest.TestCase):
 def test_service(self):
  value=build({"type":"Service","url":"https://www.arquindex.com.br/exemplo/","title":"Teste","description":"Serviço demonstrativo"})
  self.assertEqual(value["@type"],"Service")
  self.assertEqual(value["provider"]["name"],"Arquindex Gestão Documental LTDA")
 def test_refuse_http(self):
  with self.assertRaises(ValueError):
   build({"type":"Service","url":"http://example.com","title":"Teste","description":"Teste"})
 def test_refuse_missing_title(self):
  with self.assertRaises(ValueError):
   build({"type":"Article","url":"https://www.arquindex.com.br/a","description":"Teste"})
if __name__=="__main__":unittest.main()
