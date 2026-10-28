import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gerar-blocos-eeat-staging.py"
HTML = '<!doctype html><html lang="pt-BR"><head><title>Teste</title><link rel="canonical" href="https://www.arquindex.com.br/teste"></head><body><main><h1>Serviço</h1><p>Conteúdo original.</p></main></body></html>'

class EeatStagingTests(unittest.TestCase):
    def run_generator(self, html, service="digitalizacao"):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp)/"original.html", Path(tmp)/"saida.html"
            src.write_text(html, encoding="utf-8")
            p = subprocess.run([sys.executable, str(SCRIPT), "--service", service, "--input", str(src), "--output", str(dst)], text=True, capture_output=True)
            return p, src.read_text(encoding="utf-8"), dst.read_text(encoding="utf-8") if dst.exists() else None

    def test_five_services(self):
        for service in ["digitalizacao", "guarda", "alfresco", "lgpd", "ocr"]:
            with self.subTest(service=service):
                result, original, output = self.run_generator(HTML, service)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(original, HTML)
                self.assertEqual(output.count('id="aq-eeat-aeo"'), 1)
                self.assertEqual(output.count("<h1>"), 1)
                self.assertEqual(output.count('rel="canonical"'), 1)
                self.assertIn("Conteúdo original.", output)

    def test_no_duplicate_block(self):
        html = HTML.replace("</main>", '<section id="aq-eeat-aeo"></section></main>')
        result, _, output = self.run_generator(html)
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(output)

    def test_no_second_h1(self):
        result, _, output = self.run_generator(HTML.replace("</main>", "<h1>Duplicado</h1></main>"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(output)

    def test_no_second_canonical(self):
        html = HTML.replace("</head>", '<link rel="canonical" href="https://www.arquindex.com.br/duplicado"></head>')
        result, _, output = self.run_generator(html)
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(output)

    def test_requires_main(self):
        result, _, output = self.run_generator(HTML.replace("<main>", "<div>").replace("</main>", "</div>"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(output)

if __name__ == "__main__":
    unittest.main()
