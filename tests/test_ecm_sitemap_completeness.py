import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('ecm', Path(__file__).resolve().parents[1]/'scripts/seo_ecm_sitemap_proposal.py')
ecm=importlib.util.module_from_spec(spec);spec.loader.exec_module(ecm)
class CoverageTests(unittest.TestCase):
 def test_partial_never_ready(self):
  self.assertFalse(ecm.complete_review([{'accepted':True}]+[{'accepted':False}]*6))
  self.assertFalse(ecm.complete_review([]))
 def test_verification_tokens_excluded_not_deleted(self):
  urls,rejected=ecm.extract_candidates(b'<urlset><url><loc>/bh.html</loc></url><url><loc>/googleabc123.html</loc></url></urlset>')
  self.assertEqual(urls,[ecm.ORIGIN+'/bh.html'])
  self.assertEqual(rejected[0]['reason'],'verification_token')
 def test_partial_run_removes_stale_candidate(self):
  xml=b'<urlset><url><loc>/bh.html</loc></url><url><loc>/custo.html</loc></url></urlset>'
  def fetch(url):return (200,{},b'User-agent: *\nAllow: /' if url.endswith('robots.txt') else xml)
  def validate(url):return dict(url=url,accepted=url.endswith('custo.html'),reason='canonical_other_target')
  import os
  cwd=os.getcwd()
  with tempfile.TemporaryDirectory() as tmp:
   try:
    os.chdir(tmp);d=Path('seo-report/ecm-sitemap-proposal');d.mkdir(parents=True);(d/'sitemap.xml').write_text('old')
    with patch.object(ecm,'fetch',side_effect=fetch),patch.object(ecm,'validate',side_effect=validate):ecm.run()
    self.assertFalse((d/'sitemap.xml').exists())
   finally:os.chdir(cwd)
 def test_none_is_noindex(self):
  with patch.object(ecm,'fetch',return_value=(200,{'Content-Type':'text/html'},b'<meta name="robots" content="none"><link rel="canonical" href="https://ecm.arquindex.com.br/bh.html">')):
   self.assertEqual(ecm.validate(ecm.ORIGIN+'/bh.html')['reason'],'noindex')
if __name__=='__main__':unittest.main()
