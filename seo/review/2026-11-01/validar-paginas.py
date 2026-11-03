#!/usr/bin/env python3
"""Offline SEO gate for Arquindex review landing pages. No deployment."""
from html.parser import HTMLParser
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
PAGES = {
    "digitalizacao-dossies-funcionarios": BASE / "digitalizacao-dossies-funcionarios/index.html",
    "ocr-indexacao-documentos-rh": BASE / "ocr-indexacao-documentos-rh/index.html",
}
HOST = "https://www.arquindex.com.br/"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.meta = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "meta":
            self.meta.append(values)
        if tag == "link":
            self.links.append(values)

def inspect(slug, path):
    html = path.read_text(encoding="utf-8")
    scan = Scan()
    scan.feed(html)
    errors = []
    if scan.tags.count("h1") != 1:
        errors.append("H1_COUNT")
    if scan.tags.count("main") != 1:
        errors.append("MAIN_COUNT")
    canonicals = [x.get("href") for x in scan.links if x.get("rel") == "canonical"]
    if canonicals != [HOST + slug + "/"]:
        errors.append("CANONICAL")
    robots = [x.get("content", "") for x in scan.meta if x.get("name") == "robots"]
    if robots != ["noindex,follow"]:
        errors.append("REVIEW_NOINDEX")
    desc = [x.get("content", "") for x in scan.meta if x.get("name") == "description"]
    if len(desc) != 1 or not (70 <= len(desc[0]) <= 170):
        errors.append("DESCRIPTION")
    if html.count("wa.me/5531973632725") != 1:
        errors.append("CTA")
    return errors

def main():
    failed = False
    for slug, path in PAGES.items():
        errors = inspect(slug, path)
        print(slug, "OK" if not errors else ",".join(errors))
        failed |= bool(errors)
    return int(failed)

if __name__ == "__main__":
    sys.exit(main())
