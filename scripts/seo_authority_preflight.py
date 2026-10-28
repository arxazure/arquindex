#!/usr/bin/env python3
"""Read-only SEO/GEO/AEO preflight for versioned HTML. Never submits URLs."""
import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SKIP = {".git", "node_modules", ".next", "dist", "build", "vendor"}
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.h1 = 0
        self.titles = []
        self.description = []
        self.canonicals = []
        self.robots = []
        self.jsonld = []
        self.authors = []
        self.links = []
        self.in_heading = False
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.in_title = True
        if tag == "h1": self.h1 += 1
        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description": self.description.append(a.get("content", ""))
            if name in ("robots", "googlebot", "bingbot"): self.robots.append(a.get("content", ""))
            if name == "author": self.authors.append(a.get("content", ""))
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.jsonld.append(True)
        if tag == "a" and a.get("href"): self.links.append(a["href"])
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.titles.append(data)

def audit(path):
    page = Page()
    try: page.feed(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc: return {"path": str(path), "errors": ["parse_error: "+str(exc)]}
    issues = []
    if not "".join(page.titles).strip(): issues.append("missing_title")
    if not page.description or not page.description[0].strip(): issues.append("missing_meta_description")
    if page.h1 != 1: issues.append("h1_count_"+str(page.h1))
    if len(page.canonicals) != 1: issues.append("canonical_count_"+str(len(page.canonicals)))
    else:
        p = urlparse(page.canonicals[0])
        if p.scheme != "https" or not p.hostname: issues.append("canonical_not_absolute_https")
    if any(re.search(r"\bnoindex\b", x, re.I) for x in page.robots): issues.append("noindex_review")
    if not page.jsonld: issues.append("structured_data_review")
    if not page.authors: issues.append("author_attribution_review")
    # For editorial inspection only; do not assert schema or visible biography from meta author.
    if not any(x.startswith("https://") and "arquindex.com.br" in urlparse(x).hostname.lower()
               for x in page.links if urlparse(x).hostname):
        issues.append("cross_property_links_review")
    return {"path": str(path), "issues": issues, "canonical": page.canonicals[:2],
            "links": len(page.links)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="seo-report/authority-preflight.json")
    ap.add_argument("--max-files", type=int, default=15000)
    a = ap.parse_args()
    root = Path(a.root)
    files = sorted(p for p in root.rglob("*.html") if not any(v in SKIP for v in p.parts))
    if len(files) > a.max_files: raise SystemExit("Refusing incomplete audit: file limit reached")
    results = [audit(p) for p in files]
    counts = Counter(issue for row in results for issue in row.get("issues", row.get("errors", [])))
    report = {"scope": "versioned_html_only", "files_scanned": len(results),
              "issue_counts": dict(sorted(counts.items())), "pages": results,
              "notes": ["Read-only; not a live HTTP, DNS, GSC or IndexNow test.",
                        "Manual editorial review is mandatory before changes or publishing.",
                        "Meta author and JSON-LD presence do not prove E-E-A-T."]}
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"files_scanned": len(results), "issue_counts": report["issue_counts"], "report": str(out)}, ensure_ascii=False))
if __name__ == "__main__": main()
