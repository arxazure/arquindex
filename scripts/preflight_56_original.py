#!/usr/bin/env python3
"""Preflight original 56-site inventory without DNS or production changes."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]/"seo-regional"/"56-sites"
class Tags(HTMLParser):
    def __init__(self): super().__init__();self.titles=0;self.h1=0;self.canon=[];self.description=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":self.titles+=1
        if tag=="h1":self.h1+=1
        if tag=="link" and a.get("rel")=="canonical":self.canon.append(a.get("href"))
        if tag=="meta" and a.get("name")=="description":self.description+=1
def main():
    manifest=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
    issues=[]; seen=set()
    for item in manifest:
        host=item["host"];path=ROOT/host/"index.html"
        if host in seen:issues.append(f"{host}: duplicado")
        seen.add(host)
        if not re.fullmatch(r"[a-z0-9-]+\.arquindex\.com\.br",host):issues.append(f"{host}: host inválido")
        if not path.is_file():issues.append(f"{host}: arquivo ausente");continue
        content=path.read_text(encoding="utf-8");tags=Tags();tags.feed(content)
        if tags.titles!=1 or tags.h1!=1 or tags.description!=1:issues.append(f"{host}: title/h1/description inválidos")
        if tags.canon!=["https://"+host+"/"]:issues.append(f"{host}: canonical divergente {tags.canon}")
        if len(re.findall(r"\b[\wÀ-ÿ]+\b",re.sub(r"<[^>]+>"," ",content)))<300:issues.append(f"{host}: conteúdo curto")
    if len(manifest)!=56 or len(seen)!=56:issues.append(f"manifesto contém {len(manifest)} entradas e {len(seen)} hosts distintos, esperado 56")
    print(json.dumps({"checked":len(manifest),"issues":issues,"pass":not issues},ensure_ascii=False,indent=2))
    return 1 if issues else 0
if __name__=="__main__":sys.exit(main())
