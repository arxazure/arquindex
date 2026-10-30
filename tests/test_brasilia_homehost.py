import hashlib
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('staging', ROOT/'scripts/prepare-brasilia-homehost.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
POLICY = json.loads(module.POLICY.read_text())
class SafeStaging(unittest.TestCase):
    def fixture(self, page):
        return ('<!doctype html><html><head><title>Antigo</title><meta name="description" content="Original"><link rel="canonical" href="'+POLICY[page]['canonical']+'"><script>window.analytics=1</script></head><body><main><h1>Serviço original</h1><a href="/antigo.html">Histórico</a></main><footer>Contato</footer></body></html>').encode()
    def test_minimal_change_preserves_existing_assets_urls_and_source(self):
        for page in POLICY:
            raw = self.fixture(page); original = raw[:]
            result = module.prepare(raw,POLICY[page],hashlib.sha256(raw).hexdigest()).decode()
            self.assertEqual(raw,original)
            for retained in ['<h1>Serviço original</h1>','<a href="/antigo.html">','<script>window.analytics=1</script>','<footer>Contato</footer>']:self.assertIn(retained,result)
            self.assertEqual(result.count('id="arquindex-brasilia-20261029"'),1)
            with self.assertRaises(ValueError):module.prepare(result.encode(),POLICY[page],hashlib.sha256(result.encode()).hexdigest())
    def test_rejects_changed_source_wrong_canonical_missing_anchor_and_bad_encoding(self):
        page='digitalizacao.html';raw=self.fixture(page)
        with self.assertRaises(ValueError):module.prepare(raw,POLICY[page],'0'*64)
        for bad in [raw.replace(b'digitalizacao.html',b'outra.html'),raw.replace(b'</main>',b''),raw.replace(b'</main>',b'</main></main>'),raw.replace(b'<h1>',b'<h1>Segundo</h1><h1>'),raw+b'\xff']:
            with self.assertRaises((ValueError,UnicodeError)):module.prepare(bad,POLICY[page],hashlib.sha256(bad).hexdigest())
    def test_legacy_unique_anchor_allowed_but_head_anchor_rejected(self):
        page='montagem_databook_organizar.html';raw=self.fixture(page)
        self.assertIn(b'arquindex-brasilia-20261029',module.prepare(raw,POLICY[page],hashlib.sha256(raw).hexdigest(),'<footer>'))
        with self.assertRaises(ValueError):module.prepare(raw,POLICY[page],hashlib.sha256(raw).hexdigest(),'</head>')
if __name__=='__main__':unittest.main()
