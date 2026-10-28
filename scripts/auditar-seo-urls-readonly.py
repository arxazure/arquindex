#!/usr/bin/env python3
"""Auditoria somente leitura de metadados SEO em URLs explicitamente fornecidas."""
import argparse
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.h1 = []
        self.in_h1 = False
        self._h1_text = ""
        self.canonicals = []
        self.descriptions = []
        self.robots = []
        self.viewport = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "title": self.in_title = True
        if tag == "h1": self.in_h1 = True; self._h1_text = ""
        if tag == "link":
            if "canonical" in d.get("rel", "").lower().split(): self.canonicals.append(d.get("href", ""))
        if tag == "meta":
            name = d.get("name", "").lower()
            if name == "description": self.descriptions.append(d.get("content", ""))
            if name == "robots": self.robots.append(d.get("content", ""))
            if name == "viewport": self.viewport.append(d.get("content", ""))
        if tag == "a" and d.get("href"): self.links.append(d["href"])
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "h1":
            self.in_h1 = False
            self.h1.append(self._h1_text.strip())
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_h1: self._h1_text += data

def audit(url, timeout=15):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or not parsed.hostname.endswith(".arquindex.com.br"):
        raise ValueError("Somente subdomínios HTTPS de arquindex.com.br")
    req = urllib.request.Request(url, headers={"User-Agent": "Arquindex-SEO-ReadOnly/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as response:
        final_url = response.url
        if not urllib.parse.urlsplit(final_url).hostname.endswith(".arquindex.com.br"):
            raise ValueError("Redirecionamento externo não autorizado")
        status = response.status
        html = response.read(2_000_000).decode("utf-8", "replace")
    p = HeadParser()
    p.feed(html)
    canonical = urllib.parse.urljoin(final_url, p.canonicals[0]) if len(p.canonicals) == 1 else None
    return {
        "requested": url, "final_url": final_url, "http_status": status,
        "title": p.title.strip(), "h1": p.h1,
        "canonical": p.canonicals, "canonical_resolved": canonical,
        "canonical_matches_final": canonical == final_url if canonical else False,
        "meta_description": p.descriptions, "robots": p.robots, "viewport": p.viewport,
        "internal_link_count": sum(urllib.parse.urlsplit(urllib.parse.urljoin(final_url, link)).hostname.endswith(".arquindex.com.br") for link in p.links if urllib.parse.urlsplit(urllib.parse.urljoin(final_url, link)).hostname),
        "checks": {"single_title": bool(p.title.strip()), "single_h1": len(p.h1) == 1,
                   "single_canonical": len(p.canonicals) == 1,
                   "single_description": len(p.descriptions) == 1}
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+", help="Até seis URLs explícitas")
    ap.add_argument("--output", default="-")
    args = ap.parse_args()
    if len(args.urls) > 6: ap.error("Máximo de seis URLs por rodada")
    results = []
    for url in args.urls:
        try: results.append(audit(url))
        except (ValueError, urllib.error.URLError, TimeoutError) as exc:
            results.append({"requested": url, "error": str(exc)})
    payload = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output == "-": print(payload)
    else:
        with open(args.output, "w", encoding="utf-8") as f: f.write(payload + "\n")
    return int(any("error" in item for item in results))

if __name__ == "__main__":
    raise SystemExit(main())
