import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('validator',Path('scripts/validate-pr-digital.py'))
validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
class ValidatorRegression(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);shutil.copytree('pr-digital',self.root/'pr-digital')
 def tearDown(self):self.tmp.cleanup()
 def mutate(self,path,old,new):
  p=self.root/path;p.write_text(p.read_text().replace(old,new))
 def test_valid_package(self):self.assertEqual(validator.validate(self.root),[])
 def test_anchor_cannot_substitute_canonical(self):
  self.mutate('pr-digital/index.html','rel="canonical"','rel="alternate"');self.assertTrue(any('canonical' in x for x in validator.validate(self.root)))
 def test_invalid_jsonld(self):
  self.mutate('pr-digital/ia-local-governanca-documental/index.html','"@context":','"@context" INVALID:');self.assertTrue(any('JSON-LD' in x for x in validator.validate(self.root)))
 def test_missing_link(self):
  self.mutate('pr-digital/index.html','/pr-digital/calculadora-tco/','/pr-digital/missing/');self.assertTrue(any('missing internal' in x for x in validator.validate(self.root)))
 def test_duplicate_sitemap(self):
  self.mutate('pr-digital/sitemap.xml','<loc>https://www.arquindex.com.br/pr-digital/calculadora-tco/</loc>','<loc>https://www.arquindex.com.br/pr-digital/</loc>');self.assertTrue(any('Sitemap' in x for x in validator.validate(self.root)))
if __name__=='__main__':unittest.main()
