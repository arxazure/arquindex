#!/usr/bin/env python3
"""Validate reviewed ECM HTML and sitemap; no network or deployment."""
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

ROOT = Path("deploy/subdominios/ecm-arquindex")
HOST = "https://ecm.arquindex.com.br/"
PAGES = ["index.html", "bh.html", "empresas.html", "o-que-e.html",
         "vantagens-ecm.html", "vantagens.html"]

class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.robots = []
        self.title = []
        self.h1 = 0
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "link" and "canonical" in d.get("rel", "").lower().split():
            self.canonical.append(d.get("href", ""))
        if tag == "meta" and d.get("name", "").lower() == "robots":
            self.robots.append(d.get("content", ""))
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
    def handle_data(self, text):
        if self.in_title:
            self.title.append(text)
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def main():
    for name in PAGES:
        parser = Head()
        parser.feed((ROOT / name).read_text(encoding="utf-8"))
        expected = HOST if name == "index.html" else HOST + name
        assert parser.canonical == [expected], (name, parser.canonical)
        assert len(parser.title) > 0 and parser.h1 == 1, name
        assert parser.robots == ["index,follow"], name
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [x.text for x in tree.findall(".//s:loc", ns)]
    expected_urls = {HOST, *(HOST + n for n in PAGES if n != "index.html"), HOST + "custo.html"}
    assert set(locs) == expected_urls, (locs, expected_urls)
    assert len(locs) == len(set(locs)), "duplicate loc"
    for loc in locs:
        parts = urlsplit(loc)
        assert parts.scheme == "https" and parts.netloc == "ecm.arquindex.com.br", loc
        assert not any(token in loc for token in ["sitechecker", "google", "verification"]), loc
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    assert "Sitemap: " + HOST + "sitemap.xml" in robots
    print(f"PASS: {len(PAGES)} HTML pages, {len(locs)} absolute sitemap URLs, robots")
if __name__ == "__main__":
    main()
