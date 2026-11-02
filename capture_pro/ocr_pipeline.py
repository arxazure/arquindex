"""Arquivo de entrada imutável -> cópia OCR pesquisável -> PDF/A validado -> revisão.
Não realiza assinatura nem aprova automaticamente.
Dependências externas no PATH: ocrmypdf e verapdf (validador PDF/A).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024*1024),b""):
            h.update(part)
    return h.hexdigest()

def pipeline(src: Path, dest: Path, language: str="por", timeout: int=3600) -> dict:
    src=src.resolve(strict=True)
    if not src.is_file() or src.suffix.lower()!=".pdf":
        raise ValueError("Entrada deve ser PDF existente")
    if not (2<=len(language)<=24) or not all(x.isalpha() for x in language.split("+")):
        raise ValueError("Idioma inválido")
    if not shutil.which("ocrmypdf") or not shutil.which("verapdf"):
        raise RuntimeError("OCRmyPDF e veraPDF devem estar instalados no worker")
    dest=dest.absolute()
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() or src==dest:
        raise FileExistsError("Destino deve ser novo e diferente da origem")
    with tempfile.TemporaryDirectory(dir=str(dest.parent)) as tmp:
        temp=Path(tmp)/"pesquisavel.pdf"
        cmd=["ocrmypdf","--output-type","pdfa-2","--language",language,"--rotate-pages","--deskew","--skip-text","--jobs","2",str(src),str(temp)]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
        if p.returncode!=0:
            return {"status":"erro_ocr","codigo":p.returncode,"detalhe":p.stderr[-1500:]}
        # veraPDF CLI defaults to machine-readable XML with --format xml.
        v=subprocess.run(["verapdf","--format","xml",str(temp)],capture_output=True,text=True,timeout=300,check=False)
        # Fail closed: require explicit isCompliant=true, not just an exit code.
        import xml.etree.ElementTree as ET
        compliant=False
        if v.returncode==0:
            try:
                root=ET.fromstring(v.stdout)
                compliant=any(el.attrib.get("isCompliant","").lower()=="true" for el in root.iter())
            except ET.ParseError:
                compliant=False
        if not compliant:
            return {"status":"revisao_pdfa","detalhe":"Arquivo não validado como PDF/A pelo veraPDF","stderr":v.stderr[-500:]}
        os.replace(temp,dest)
    return {"status":"aguardando_revisao","original_sha256":digest(src),"pdfa_sha256":digest(dest),"arquivo":str(dest),"assinatura":"nao_assinado"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--lang",default="por")
    args=p.parse_args()
    print(json.dumps(pipeline(args.input,args.output,args.lang),ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
