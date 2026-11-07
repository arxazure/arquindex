#!/usr/bin/env python3
"""Validate Arquindex GED/ECM study and Alfresco interlinking locally."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = "/estudos/ged-ecm-transformacao-digital/"
STUDIES = "/estudos/"
ALFRESCO = "/estudos/alfresco-community/"
PAGES = [
    "estudos/index.html",
    "estudos/alfresco-community/index.html",
    "estudos/ged-ecm-transformacao-digital/index.html",
    "alfresco-automacao-documental/index.html",
    "blog/alfresco-reducao-custos-processos-documentais/index.html",
    "blog/alfresco-rpa-conectores-ia-automacao/index.html",
    "blog/alfresco-recebimento-aprovacao-revisao-compartilhamento/index.html",
    "alfresco-cloud-ocr-ia/index.html",
    "blog/alfresco-community-gestao-documental-sem-amps/index.html",
    "manuais/alfresco-community-aspectos-temporalidade/index.html",
    "blog/alfresco-cloud-e-ocr-tco/index.html",
]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(v for k,v in attrs if k == "href" and v)
errors = []
for path in PAGES:
    file = ROOT / path
    if not file.exists():
        errors.append(f"MISSING {path}")
        continue
    p = Links()
    p.feed(file.read_text(encoding="utf-8"))
    if BRIDGE not in p.hrefs:
        errors.append(f"NO BRIDGE LINK {path}")
    if path not in ("estudos/index.html", "estudos/alfresco-community/index.html"):
        for target in (STUDIES, ALFRESCO):
            if target not in p.hrefs:
                errors.append(f"NO LINK {target} IN {path}")
    for href in p.hrefs:
        if href.startswith("/") and not href.startswith("//"):
            local = ROOT / urlsplit(href).path.lstrip("/")
            if local.is_dir() and (local / "index.html").exists():
                continue
            if local.is_file():
                continue
            # Existing production routes can be outside the repository build root.
            print(f"REQUIRES_DEPLOY_CHECK {path}: {href}")
    print(f"CHECKED {path}")
sitemap = ROOT / "sitemap-estudos-ged-ecm.xml"
if not sitemap.exists():
    errors.append("MISSING sitemap-estudos-ged-ecm.xml")
else:
    data = sitemap.read_text(encoding="utf-8")
    for target in (BRIDGE, STUDIES, ALFRESCO):
        if f"https://www.arquindex.com.br{target}" not in data:
            errors.append(f"SITEMAP MISSING {target}")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("PASS: bridge and sitemap references are present in all listed files.")
