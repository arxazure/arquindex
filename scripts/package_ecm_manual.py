#!/usr/bin/env python3
"""Package the reviewed ECM website for manual installation; never uploads."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from datetime import datetime, timezone
from validate_ecm_dedicated_site import main as validate

ROOT = Path("deploy/subdominios/ecm-arquindex")
FILES = ["index.html", "bh.html", "empresas.html", "o-que-e.html",
         "vantagens-ecm.html", "vantagens.html", "robots.txt", "sitemap.xml"]

def run(dest: Path):
    validate()
    dest.mkdir(parents=True, exist_ok=True)
    entries = []
    with zipfile.ZipFile(dest / "ecm-arquindex-manual.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            path = ROOT / name
            data = path.read_bytes()
            entries.append({"file": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
            archive.writestr(name, data)
        instructions = ("PACOTE PARA PUBLICACAO MANUAL - ECM ARQUINDEX\n"
                        "Nao instalar antes de confirmar document root exato na HomeHost.\n"
                        "Realizar backup com teste de restauracao e comparar arquivos remotos.\n"
                        "Este pacote nao inclui custo.html nem tokens de verificacao; preserve-os.\n"
                        "Validar URLs publicas, canonicals e sitemap apos implantacao.\n"
                        "Nao extrair na raiz do dominio principal nem no host alfresco-ecm.\n")
        archive.writestr("LEIA-ME-PUBLICACAO.txt", instructions)
    manifest = {"target_host": "ecm.arquindex.com.br",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "mode": "manual_install_only", "published": False,
                "requires_verified_document_root": True,
                "preserve_remote_files": ["custo.html", "google*.html", "sitechecker*.html"],
                "files": entries}
    (dest / "manifest-sha256.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("ECM_MANUAL_PACKAGE_READY",len(entries), str(dest / "ecm-arquindex-manual.zip"))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="ecm-release")
    run(Path(p.parse_args().out))
