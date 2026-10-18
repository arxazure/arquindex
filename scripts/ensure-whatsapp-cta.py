#!/usr/bin/env python3
"""Idempotent WhatsApp CTA injection for Arquindex static HTML deployments.
Usage: python scripts/ensure-whatsapp-cta.py PATH [PATH ...]
Dry run: python scripts/ensure-whatsapp-cta.py --check PATH
Only modifies *.html; skips files already containing the marker.
"""
import argparse, pathlib, re, sys
PHONE="5531973632725"
MARK="arquindex-whatsapp-atendimento-v1"
CSS=f"""<style id="{MARK}-style">
.arq-whatsapp-float{{position:fixed;right:18px;bottom:18px;z-index:9999;display:flex;align-items:center;gap:9px;padding:13px 17px;border-radius:999px;background:#087c4a;color:#fff!important;font:700 15px/1.3 Arial,sans-serif;text-decoration:none;box-shadow:0 4px 16px #0004}}
.arq-whatsapp-float:focus-visible{{outline:3px solid #ffcf52;outline-offset:3px}}
@media(max-width:600px){{.arq-whatsapp-float{{right:12px;bottom:12px;padding:12px 14px}}}}
</style>"""
LINK=f"""<a class="arq-whatsapp-float" data-arq-whatsapp="{MARK}" href="https://wa.me/{PHONE}?text=Ol%C3%A1%21%20Vim%20pelo%20site%20da%20Arquindex%20e%20gostaria%20de%20atendimento." target="_blank" rel="noopener noreferrer" aria-label="Atendimento Arquindex pelo WhatsApp">☎ Atendimento WhatsApp</a>"""
def run(root,check):
    changed=skipped=errors=0
    files=[root] if root.is_file() else root.rglob("*.html")
    for file in files:
        if file.suffix.lower()!=".html":continue
        try:
            raw=file.read_text(encoding="utf-8")
            if MARK in raw:skipped+=1;continue
            if not re.search(r"</body\s*>",raw,re.I):errors+=1;print("SEM_BODY",file);continue
            updated=re.sub(r"</head\s*>",lambda m:CSS+"\n"+m.group(),raw,count=1,flags=re.I)
            updated=re.sub(r"</body\s*>",lambda m:LINK+"\n"+m.group(),updated,count=1,flags=re.I)
            if not check:file.write_text(updated,encoding="utf-8")
            changed+=1;print("PENDENTE" if check else "ATUALIZADO",file)
        except (OSError,UnicodeError) as exc:errors+=1;print("ERRO",file,exc)
    return changed,skipped,errors
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--check",action="store_true");p.add_argument("paths",nargs="+");a=p.parse_args()
    totals=[0,0,0]
    for path in a.paths:
        if not pathlib.Path(path).exists():print("NAO_EXISTE",path);totals[2]+=1;continue
        r=run(pathlib.Path(path),a.check);totals=[x+y for x,y in zip(totals,r)]
    print("Resumo: modificáveis/modificados=%s já existentes=%s erros=%s"%tuple(totals))
    sys.exit(bool(totals[2]))
