#!/usr/bin/env python3
"""Testes locais sem rede para integracao RH/DP. Executar: python -m unittest discover -s seo/review/2026-10-27 -p 'test_*.py'"""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("publicar_rhdp", HERE / "publicar-rhdp-homehost.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
FRAGMENT = (HERE / "rhdp-dossies-bloco-editorial.html").read_text(encoding="utf-8").strip()
SOURCE = """<!doctype html><html lang="pt-BR"><head>
<link rel="canonical" href="https://www.arquindex.com.br/gestao_de_colaboradores_documentos.html">
<title>Gestão de documentos de colaboradores</title></head>
<body><h1>Gestão documental para colaboradores</h1><main>Conteúdo original</main></body></html>"""

class TestRhDp(unittest.TestCase):
    def test_preserva_conteudo_e_estrutura(self):
        updated = mod.integrate(SOURCE, FRAGMENT)
        mod.validate(updated)
        self.assertIn("<main>Conteúdo original</main>", updated)
        self.assertEqual(updated.count('id="arquindex-dossies-rhdp"'), 1)
        self.assertEqual(updated.count(mod.MARK_START), 1)
        self.assertEqual(updated.count(mod.MARK_END), 1)

    def test_idempotencia(self):
        once = mod.integrate(SOURCE, FRAGMENT)
        twice = mod.integrate(once, FRAGMENT)
        self.assertEqual(once, twice)

    def test_rejeita_h1_duplicado(self):
        with self.assertRaises(RuntimeError):
            mod.validate(SOURCE.replace("</body>", "<h1>Outro</h1></body>"))

    def test_rejeita_canonical_incorreto(self):
        with self.assertRaises(RuntimeError):
            mod.validate(SOURCE.replace("gestao_de_colaboradores_documentos.html", "outra.html"))

    def test_rejeita_marcadores_ambiguos(self):
        with self.assertRaises(RuntimeError):
            mod.integrate(SOURCE + mod.MARK_START, FRAGMENT)

if __name__ == "__main__":
    unittest.main()
