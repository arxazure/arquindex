"""Arquindex Capture: validated document segmentation and local client backup utilities.
This module is a standalone prototype; no production endpoints are exposed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import sqlite3
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import fitz

PATIENT = re.compile(r"(?im)^\s*(?:nome\s+do\s+paciente|paciente)\s*[:\-]\s*([^\n\r]{5,100})")
EMPLOYEE = re.compile(r"(?im)^\s*(?:nome\s+do\s+funcion[aá]rio|colaborador)\s*[:\-]\s*([^\n\r]{5,100})")
REGISTRATION = re.compile(r"(?im)^\s*matr[ií]cula\s*[:\-]\s*([A-Z0-9./-]{2,30})")
MAX_BYTES = 4 * 1024 * 1024 * 1024

def clean_name(s: str) -> str:
    s = re.sub(r"[^\w\- ]+", "", s, flags=re.UNICODE).strip()
    return re.sub(r"\s+", "_", s)[:100] or "NAO_IDENTIFICADO"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def split_pdf(source: Path, destination: Path, model: str, min_text_chars: int = 25) -> dict:
    """Conservative segmentation: split ONLY on changed, explicitly labelled identities.
    Every unrecognised/ambiguous page stays with previous document, and is flagged.
    A fully blank/ambiguous leading page causes manual review, not automated release.
    """
    if model not in ("prontuario", "dossie"):
        raise ValueError("Modelo inválido")
    pattern = PATIENT if model == "prontuario" else EMPLOYEE
    src = fitz.open(str(source))
    if src.needs_pass or src.page_count == 0:
        raise ValueError("PDF criptografado ou vazio")
    destination.mkdir(parents=True, exist_ok=True)
    groups, review, active_identity, active_mat, begin = [], [], None, None, 0
    for idx, page in enumerate(src):
        text = page.get_text("text")
        if len(text.strip()) < min_text_chars:
            review.append({"pagina": idx+1, "motivo": "OCR ausente ou insuficiente"})
        names = {re.sub(r"\s+", " ", x.strip()).casefold(): x.strip() for x in pattern.findall(text)}
        mats = REGISTRATION.findall(text) if model == "dossie" else []
        if len(names) > 1 or len(set(mats)) > 1:
            review.append({"pagina": idx+1, "motivo": "Identidades conflitantes"})
            continue
        identity = next(iter(names.values()), None)
        mat = mats[0] if mats else None
        if identity and active_identity and identity.casefold() != active_identity.casefold():
            groups.append((begin, idx, active_identity, active_mat))
            begin = idx
            active_identity, active_mat = identity, mat
        elif identity and not active_identity:
            if idx:
                review.append({"pagina": idx+1, "motivo": "Primeira identidade só identificada após início"})
            active_identity, active_mat = identity, mat
        elif identity and model == "dossie" and mat and active_mat and mat != active_mat:
            groups.append((begin, idx, active_identity, active_mat))
            begin = idx
            active_identity, active_mat = identity, mat
        elif mat and not active_mat:
            active_mat = mat
    if active_identity is None:
        src.close()
        return {"status": "revisao_obrigatoria", "motivo": "Nenhum cabeçalho identificado", "arquivos": [], "alertas": review}
    groups.append((begin, src.page_count, active_identity, active_mat))
    outputs = []
    for n,(start,end,name,mat) in enumerate(groups,1):
        if start == end:
            continue
        name_out = f"{n:04d}_{clean_name(name)}"
        if mat:
            name_out += f"_{clean_name(mat)}"
        target = destination / (name_out + ".pdf")
        if target.exists():
            src.close()
            raise FileExistsError(f"Arquivo já existe: {target.name}")
        pdf = fitz.open()
        pdf.insert_pdf(src, from_page=start, to_page=end-1)
        pdf.save(str(target), garbage=3, deflate=True)
        pdf.close()
        outputs.append({"arquivo": target.name, "paginas": [start+1,end], "nome": name, "matricula": mat, "sha256": sha256_file(target)})
    src.close()
    return {"status": "revisao_obrigatoria" if review else "aguardando_aprovacao", "arquivos": outputs, "alertas": review, "observacao": "Não é PDF/A validado nem assinado; submeter ao pipeline de conformidade."}

def backup_client(client: str, root: Path, db: Path, destination: Path) -> dict:
    """Local archive for a client tree and metadata snapshot. No platform VM/s3 backup.
    Operate only on an admin-configured, pre-authorized source directory.
    """
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", client):
        raise ValueError("Identificador de cliente inválido")
    root, destination = root.resolve(strict=True), destination.resolve(strict=True)
    if not root.is_dir() or not destination.is_dir():
        raise ValueError("Pastas de origem e destino devem existir")
    if destination == root or root in destination.parents:
        raise ValueError("Destino não pode ficar dentro da origem")
    if db.exists() and db.resolve().is_symlink():
        raise ValueError("Não aceitar banco em link simbólico")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    final = destination / f"arquindex_{client}_{timestamp}.zip"
    if final.exists():
        raise FileExistsError(final)
    manifest = {"client":client,"created_utc":timestamp,"files":[]}
    with tempfile.TemporaryDirectory() as work:
        temp_path = Path(work) / "backup.zip"
        snap = Path(work) / "index.sqlite"
        if db.exists():
            with sqlite3.connect(str(db)) as s, sqlite3.connect(str(snap)) as d:
                s.backup(d)
        with zipfile.ZipFile(temp_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
            for p in sorted(root.rglob("*")):
                if p.is_symlink():
                    raise ValueError(f"Link simbólico não permitido: {p}")
                if not p.is_file():
                    continue
                rel = p.relative_to(root).as_posix()
                if p.stat().st_size > MAX_BYTES:
                    raise ValueError(f"Arquivo grande demais para este executor: {rel}")
                z.write(p, "documentos/"+rel)
                manifest["files"].append({"path":"documentos/"+rel,"bytes":p.stat().st_size,"sha256":sha256_file(p)})
            if snap.exists():
                z.write(snap,"dados/index.sqlite")
                manifest["files"].append({"path":"dados/index.sqlite","bytes":snap.stat().st_size,"sha256":sha256_file(snap)})
            z.writestr("manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2))
        os.replace(temp_path, final)
    return {"arquivo":str(final),"sha256":sha256_file(final),"quantidade":len(manifest["files"]),"nota":"Backup local sem criptografia: manter destino em volume cifrado, com permissão restrita e cópia externa."}

def main():
    p=argparse.ArgumentParser(description="Arquindex - ferramentas isoladas de preparação")
    sub=p.add_subparsers(dest="command",required=True)
    s=sub.add_parser("split")
    s.add_argument("--input",type=Path,required=True)
    s.add_argument("--out",type=Path,required=True)
    s.add_argument("--model",required=True,choices=["prontuario","dossie"])
    b=sub.add_parser("backup")
    b.add_argument("--client",required=True)
    b.add_argument("--root",type=Path,required=True)
    b.add_argument("--db",type=Path,required=True)
    b.add_argument("--destination",type=Path,required=True)
    args=p.parse_args()
    result=split_pdf(args.input,args.out,args.model) if args.command=="split" else backup_client(args.client,args.root,args.db,args.destination)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
