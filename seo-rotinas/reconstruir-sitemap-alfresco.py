#!/usr/bin/env python3
"""Arquindex Alfresco sitemap recovery preflight. Read-only: NEVER uploads.

Builds a candidate XML from repository manifest and three editorial URLs.
Only includes URLs returning HTTP 200, self-canonical, and no noindex.
Run from repository root: python3 seo-rotinas/reconstruir-sitemap-alfresco.py
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = "https://www.arquindex.com.br/"
MANIFEST = Path("seo/alfresco-cloud-manifest.json")
EXTRA = [
    ROOT + "blog/alfresco-cloud-ocr-inteligencia-documental/",
    ROOT + "blog/tco-alfresco-cloud-versus-saas/",
    ROOT + "blog/ocr-inteligente-vs-busca-ecm/",
]
OUT = Path("publish-report/sitemap-alfresco-cloud-20261021.candidate.xml")
REPORT = Path("publish-report/sitemap-alfresco-recovery-preflight.json")
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

class SEOHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []
    def handle_starttag(self, tag, attrs):
        if tag not in ("link", "meta"):
            return
        attrs = dict(attrs)
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name", "").lower() in ("robots", "googlebot"):
            self.robots.append(attrs.get("content", "").lower())

def verify(url):
    if not url.startswith(ROOT):
        return {"url": url, "accepted": False, "reason": "outside_canonical_host"}
    request = urllib.request.Request(url, headers={"User-Agent": "ArquindexSitemapPreflight/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=18) as response:
            final_url = response.geturl()
            status = response.status
            content_type = response.headers.get("Content-Type", "")
            header_robots = response.headers.get("X-Robots-Tag", "").lower()
            body = response.read(1_500_000)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"url": url, "accepted": False, "reason": type(exc).__name__}
    parser = SEOHTML()
    if "text/html" not in content_type.lower():
        return {"url": url, "accepted": False, "reason": "not_html"}
    parser.feed(body.decode("utf-8", errors="replace"))
    reasons = []
    if status != 200: reasons.append("http_not_200")
    if final_url != url: reasons.append("redirect_or_url_mismatch")
    if "noindex" in header_robots or any("noindex" in x for x in parser.robots):
        reasons.append("noindex")
    if len(parser.canonicals) != 1 or parser.canonicals[0] != url:
        reasons.append("canonical_not_self_or_missing")
    return {"url": url, "accepted": not reasons, "reason": ",".join(reasons) or "ok", "final_url": final_url}

def main():
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    urls = sorted(set([e["url"] for e in entries] + EXTRA))
    if len(urls) != len(entries) + len(EXTRA):
        raise RuntimeError("duplicate candidate URLs; review manifest")
    results = [verify(url) for url in urls]
    accepted = [r["url"] for r in results if r["accepted"]]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    root = ET.Element("{" + NS + "}urlset")
    for url in accepted:
        item = ET.SubElement(root, "{" + NS + "}url")
        ET.SubElement(item, "{" + NS + "}loc").text = url
    ET.ElementTree(root).write(OUT, encoding="utf-8", xml_declaration=True)
    REPORT.write_text(json.dumps({"candidate_count": len(urls), "accepted_count": len(accepted), "results": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("CANDIDATES", len(urls), "ACCEPTED", len(accepted), "REJECTED", len(urls) - len(accepted))
    print("LOCAL_ONLY", OUT, REPORT)
    if len(accepted) < 10:
        print("BLOCKED: fewer than 10 validated URLs; do not publish", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
