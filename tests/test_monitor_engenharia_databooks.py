import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
spec=importlib.util.spec_from_file_location('monitor',Path(__file__).resolve().parents[1]/'scripts/monitor_engenharia_databooks.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
URL='https://databook-petrobras-elaboracao.arquindex.com.br/'
HTML='<title>Databook</title><h1>Guia</h1><link rel="canonical" href="'+URL+'"><a href="/escopo">Escopo</a>'

def response(url):
    return (200,url,{},'User-agent: *\nAllow: /' if url.endswith('robots.txt') else HTML)

class MonitorTest(unittest.TestCase):
    def test_scope(self):
        self.assertTrue(m.allowed(URL))
        for u in ['https://arquindex.com.br.evil.example/','https://evil.example/','http://arquindex.com.br/','https://user@arquindex.com.br/','https://arquindex.com.br:444/']:
            self.assertFalse(m.allowed(u))
    @patch.object(m,'fetch',side_effect=response)
    def test_valid_page_does_not_claim_indexing(self,_):
        row=m.check({'id':'x','url':URL})
        self.assertEqual(row['issues'],[])
        self.assertEqual(row['indexacao'],'nao_verificada')
        self.assertEqual(row['links'],[URL+'escopo'])
    @patch.object(m,'fetch',side_effect=HTTPError(URL,503,'Unavailable',{},None))
    def test_503_alert(self,_):
        row=m.check({'id':'x','url':URL})
        self.assertEqual(row['http'],503)
        self.assertEqual(row['issues'],['http_nao_200'])
    def test_duplicate_canonical_and_h1(self):
        def duplicate(url):
            a,b,c,d=response(url)
            return a,b,c,d if url.endswith('robots.txt') else d+'<h1>Duplicado</h1><link rel="canonical" href="'+URL+'">'
        with patch.object(m,'fetch',side_effect=duplicate): row=m.check({'id':'x','url':URL})
        self.assertIn('h1_ausente_ou_multiplo',row['issues'])
        self.assertIn('canonical_ausente_ou_multiplo',row['issues'])
    def test_header_noindex_and_robots_disallow(self):
        def blocked(url):
            return 200,url,{'x-robots-tag':'noindex'},'User-agent: *\nDisallow: /' if url.endswith('robots.txt') else HTML
        with patch.object(m,'fetch',side_effect=blocked): row=m.check({'id':'x','url':URL})
        self.assertIn('noindex',row['issues'])
        self.assertIn('robots_bloqueia_googlebot',row['issues'])
    def test_external_redirect_is_rejected(self):
        with self.assertRaises(ValueError): m.SafeRedirect().redirect_request(None,None,302,'',{},'https://evil.example/')

if __name__=='__main__':unittest.main()
