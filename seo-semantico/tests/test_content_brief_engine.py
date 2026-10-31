import tempfile
import unittest
from pathlib import Path
from content_brief_engine import entities, build_brief, render, run, public_https

class BriefEngineTests(unittest.TestCase):
 def test_safe_urls(self):
  self.assertTrue(public_https("https://example.org/guide"))
  self.assertFalse(public_https("http://example.org/"))
  self.assertFalse(public_https("https://user:pass@example.org/"))
 def test_offline_generates_files(self):
  config={"briefs":{"lgpd":{"title":"Adequação LGPD empresarial","competitor_urls":[]}}}
  with tempfile.TemporaryDirectory() as folder:
   result=run(config,folder,skip_fetch=True)
   self.assertEqual(result["lgpd"]["references_analyzed"],0)
   self.assertTrue((Path(folder)/"briefs"/"lgpd"/"rascunho.md").exists())
   self.assertIn("RASCUNHO PARA REVISÃO",(Path(folder)/"briefs"/"lgpd"/"rascunho.md").read_text())
 def test_topic_brief(self):
  analysis=entities([],["OCR pesquisável"])
  brief=build_brief("digitalizacao",{"title":"Digitalização B2B"},[],analysis)
  self.assertIn("OCR pesquisável",brief["recommended_subtopics"])
  self.assertEqual(brief["status"],"draft_review_required")
if __name__=="__main__":unittest.main()
