#!/usr/bin/env python3
"""Offline preflight for the Arquindex Alfresco regional campaign."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
CITIES = ("sao-paulo", "rio-de-janeiro", "brasilia", "curitiba", "recife", "belo-horizonte", "contagem", "betim", "nova-lima", "santa-luzia")
ARTICLES = ("alfresco-cloud-e-ocr-tco", "ocr-inteligente-vs-busca-ecm", "nuvem-dedicada-governanca-alfresco")
class HTMLCheck(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.meta = []
        self.links = []
        self.jsonld = []
        self.capture_script = False
        self.script = []
    def handle_starttag(self, tag, attrs):
        p = dict(attrs)
        self.tags.append(tag)
        if tag == "meta": self.meta.append(p)
        if tag == "link": self.links.append(p)
        if tag == "script" and p.get("type") == "application/ld+json":
            self.capture_script = True
            self.script = []
    def handle_data(self, data):
        if self.capture_script: self.script.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.capture_script:
            self.jsonld.append("".join(self.script))
            self.capture_script = False

issues = []
for kind, slugs in (("seo", CITIES), ("blog", ARTICLES)):
    for slug in slugs:
        folder = f"alfresco-cloud-ocr-ia-{slug}" if kind == "seo" else slug
        path = ROOT / kind / folder / "index.html"
        if not path.is_file():
            issues.append(f"Missing: {path.relative_to(ROOT)}")
            continue
        html = path.read_text(encoding="utf-8")
        parser = HTMLCheck()
        parser.feed(html)
        canonical = f"https://www.arquindex.com.br/{kind}/{folder}/"
        canonicals = [x.get("href") for x in parser.links if x.get("rel") == "canonical"]
        if canonicals != [canonical]: issues.append(f"{folder}: canonical mismatch")
        if parser.tags.count("h1") != 1: issues.append(f"{folder}: expected one H1")
        if not any(x.get("name") == "description" and x.get("content") for x in parser.meta):
            issues.append(f"{folder}: missing meta description")
        if not parser.jsonld: issues.append(f"{folder}: missing JSON-LD")
        for raw in parser.jsonld:
            try: json.loads(raw)
            except json.JSONDecodeError: issues.append(f"{folder}: invalid JSON-LD")
        if "http-equiv=\"refresh\"" in html.lower(): issues.append(f"{folder}: unexpected refresh redirect")
        print("CHECK", kind, folder, "canonical", canonical)
if issues:
    print("\n".join(issues), file=sys.stderr)
    sys.exit(1)
print("PASS: 13 pages structurally valid. Public URL/hosting verification remains required.")
