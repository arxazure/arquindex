"""Smoke tests: only synthetic PDFs, no client data."""
import tempfile
import unittest
from pathlib import Path
import fitz
from capture_pro.processing import split_pdf, clean_name

class SplitTests(unittest.TestCase):
    def test_prontuario_multipage(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            p=root/"entrada.pdf"
            doc=fitz.open()
            for text in ["Paciente: Ana Silva\nConsulta realizada","Exame clinico pagina 2","Paciente: Joao Souza\nConsulta realizada"]:
                page=doc.new_page()
                page.insert_text((72,72),text)
            doc.save(str(p));doc.close()
            result=split_pdf(p,root/"out","prontuario",min_text_chars=10)
            self.assertEqual(len(result["arquivos"]),2)
            self.assertEqual(result["arquivos"][0]["paginas"],[1,2])
            self.assertEqual(result["arquivos"][1]["paginas"],[3,3])
    def test_safe_names(self):
        self.assertEqual(clean_name("Ana / Silva"),"Ana_Silva")

if __name__=="__main__":
    unittest.main()
