import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('audit',Path(__file__).parents[1]/'scripts/audit_56_public.py')
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
class PublicGateTests(unittest.TestCase):
    def good(self):
        return [{'host':f's{i}.arquindex.com.br','dns':['192.0.2.1'],'tls':{'valid':True},'page':{'status':200,'url':f'https://s{i}.arquindex.com.br/'},'html':{'canonical':[f'https://s{i}.arquindex.com.br/']},'issues':[]} for i in range(56)]
    def test_complete_public_evidence(self):
        self.assertTrue(audit.public_gate(self.good(),True))
    def test_ftp_or_http_success_cannot_replace_dns_tls_and_own_content(self):
        for change in [{'dns':[]},{'tls':{'valid':False}},{'html':{'canonical':['https://www.arquindex.com.br/']}},{'page':{'status':200,'url':'https://www.arquindex.com.br/'}}]:
            rows=self.good(); rows[2].update(change)
            self.assertFalse(audit.public_gate(rows,True))
    def test_postflight_rejects_sitemap_failure(self):
        rows=self.good(); rows[50]['issues']=['XML sitemap inválido']
        self.assertFalse(audit.public_gate(rows))
    def test_missing_host_rejected(self):
        self.assertFalse(audit.public_gate(self.good()[:-1],True))
    def test_duplicate_h1_detectable(self):
        self.assertEqual(len(audit.parsed('<h1>A</h1><h1>B</h1>')['h1']),2)
if __name__=='__main__': unittest.main()
