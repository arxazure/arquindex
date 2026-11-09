#!/usr/bin/env python3
"""Validate the five-page contextual linking plan and the regional sitemap offline."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

BASE = "https://www.arquindex.com.br"
FOLDER = "seo-regional/gestao-documental-ecm-databooks"
SLUGS = ("", "betim", "contagem", "nova-lima")
BLOG = "blog/montagem-de-databooks-de-engenharia"
PAGES = {BASE + "/" + FOLDER + "/" + (slug + "/" if slug else ""):
         Path(FOLDER) / slug / "index.html" for slug in SLUGS}
PAGES[BASE + "/" + BLOG + "/"] = Path(BLOG) / "index.html"
SITEMAP = Path(FOLDER) / "sitemap.xml"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.h1_count = 0
        self.canonicals = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.add(a["href"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "link" and "canonical" in (a.get("rel") or "").split():
            self.canonicals.append(a.get("href"))


def validate(root):
    errors = []
    pages = {}
    for url, relative in PAGES.items():
        file = root / relative
        if not file.is_file():
            errors.append(f"missing_file: {relative}")
            continue
        parser = Links()
        parser.feed(file.read_text(encoding="utf-8"))
        if parser.h1_count != 1:
            errors.append(f"invalid_h1: {relative}")
        if parser.canonicals != [url]:
            errors.append(f"canonical_mismatch: {relative}")
        pages[url] = {urljoin(url, href) for href in parser.links
                      if urlsplit(urljoin(url, href)).hostname == "www.arquindex.com.br"}
    for source, targets in pages.items():
        for dest in PAGES:
            if dest == source:
                continue
            if dest not in targets:
                errors.append(f"missing_contextual_link: {source} -> {dest}")
    try:
        tree = ET.parse(root / SITEMAP)
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        listed = [node.text for node in tree.findall(".//" + ns + "loc")]
        if len(set(listed)) != len(listed):
            errors.append("duplicate_sitemap_loc")
        for page in PAGES:
            if listed.count(page) != 1:
                errors.append(f"sitemap_page_not_exactly_once: {page}")
    except (OSError, ET.ParseError) as error:
        errors.append(f"sitemap_invalid: {error}")
    return errors


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    errors = validate(root)
    for error in errors:
        print("ERROR", error)
    if errors:
        print(f"FAILED {len(errors)}")
        return 1
    print(f"OK {len(PAGES)} pages interconnected, regional sitemap unique")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
