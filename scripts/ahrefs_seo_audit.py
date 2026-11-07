#!/usr/bin/env python3
"""Read-only inventory of on-disk HTML for Ahrefs SEO triage.

Does NOT publish, rewrite pages, submit IndexNow, or infer live crawl status.
Usage: python3 scripts/ahrefs_seo_audit.py --root . --out seo-report/ahrefs-audit.json
"""
import argparse
import json
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

SITE = "https://www.arquindex.com.br"
SKIP = {".git", "node_modules", ".venv", "vendor", "dist", "build", "artifacts", "seo-report"}
MAX_BYTES = 2_000_000

class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_depth = False
        self.title = ""
        self.description = []
        self.og = {}
        self.canonical = []
        self.h1 = 0
        self.links = []
        self.jsonld = []
        self._json = False
        self._json_body = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.title_depth = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "meta":
            if (a.get("name") or "").lower() == "description":
                self.description.append((a.get("content") or "").strip())
            prop = (a.get("property") or "").lower()
            if prop.startswith("og:"):
                self.og[prop] = (a.get("content") or "").strip()
        elif tag == "link" and "canonical" in (a.get("rel") or "").lower().split():
            self.canonical.append(a.get("href") or "")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._json = True
            self._json_body = ""

    def handle_data(self, data):
        if self.title_depth:
            self.title += data
        if self._json:
            self._json_body += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.title_depth = False
        if tag == "script" and self._json:
            self.jsonld.append(self._json_body)
            self._json = False

def normalized_url(url):
    p = urlsplit(url)
    if p.scheme not in ("http", "https") or p.hostname not in ("arquindex.com.br", "www.arquindex.com.br"):
        return None
    path = unquote(p.path or "/")
    path = re.sub(r"/+", "/", path)
    if path.endswith("/index.html"):
        path = path[:-len("/index.html")] + "/"
    return "https://www.arquindex.com.br" + path.rstrip("/") + ("/" if path.endswith("/") or path == "/" else "")

def page_url(path, root):
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return SITE + "/"
    if relative.endswith("/index.html"):
        return SITE + "/" + relative[:-len("index.html")]
    return SITE + "/" + relative

def schema_has_faq(items):
    for raw in items:
        try:
            parsed = json.loads(raw)
            if "FAQPage" in json.dumps(parsed, ensure_ascii=False):
                return True
        except (ValueError, TypeError):
            continue
    return False

def audit(root, max_files):
    pages = []
    for file in root.rglob("*.html"):
        if any(p in SKIP or p.startswith(".") for p in file.relative_to(root).parts[:-1]):
            continue
        if len(pages) >= max_files:
            break
        if file.stat().st_size > MAX_BYTES:
            continue
        parser = Markup()
        try:
            parser.feed(file.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError) as error:
            pages.append({"file": str(file.relative_to(root)), "issues": ["read_error:" + str(error)]})
            continue
        url = page_url(file, root)
        issues = []
        if not parser.description or not any(parser.description):
            issues.append("meta_description_missing")
        if len(parser.title.strip()) > 60:
            issues.append("title_over_60_characters_review")
        if not parser.title.strip():
            issues.append("title_missing")
        required_og = ("og:title", "og:description", "og:url", "og:image")
        if any(not parser.og.get(k) for k in required_og):
            issues.append("open_graph_incomplete")
        if parser.h1 > 1:
            issues.append("multiple_h1")
        if parser.h1 == 0:
            issues.append("h1_missing")
        if "faq" in file.stem.lower() and not schema_has_faq(parser.jsonld):
            issues.append("faq_schema_review_not_automatic")
        if len(parser.canonical) != 1:
            issues.append("canonical_count_review")
        pages.append({"file": str(file.relative_to(root)), "url": url,
                      "title": parser.title.strip(), "h1_count": parser.h1,
                      "links": parser.links, "issues": issues})
    incoming = defaultdict(set)
    known = {normalized_url(p["url"]) for p in pages if p.get("url")}
    for page in pages:
        if not page.get("url"):
            continue
        for href in page["links"]:
            target = normalized_url(urljoin(page["url"], href))
            if target in known and target != normalized_url(page["url"]):
                incoming[target].add(page["url"])
    for page in pages:
        if not page.get("url"):
            continue
        page["incoming_internal_links"] = len(incoming[normalized_url(page["url"])])
        if page["incoming_internal_links"] == 0 and page["url"] != SITE + "/":
            page["issues"].append("orphan_within_scanned_files_review")
        page.pop("links", None)
    return {"scope": "local_html_only", "site": SITE, "pages_scanned": len(pages),
            "limitations": [
                "Repository pages do not necessarily correspond to published HomeHost pages.",
                "Orphan means no incoming link among HTML files scanned, not an Ahrefs live-crawl finding.",
                "Performance, backlinks, IndexNow acceptance, and word-count changes require external data.",
                "Do not add FAQPage automatically: verify the visible FAQ content and current Google eligibility.",
                "No files modified or deployed."
            ], "pages": pages}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, default=Path("seo-report/ahrefs-audit.json"))
    ap.add_argument("--max-files", type=int, default=10000)
    args = ap.parse_args()
    if not args.root.is_dir() or args.max_files < 1:
        ap.error("root must be a directory and max-files must be positive")
    report = audit(args.root.resolve(), args.max_files)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = defaultdict(int)
    for page in report["pages"]:
        for issue in page["issues"]:
            counts[issue] += 1
    print(json.dumps({"pages": report["pages_scanned"], "findings": dict(counts), "report": str(args.out)}))

if __name__ == "__main__":
    main()
