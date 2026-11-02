#!/usr/bin/env python3
"""Arquindex SEO read-only preflight. No publishing, pinging or sitemap submissions."""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = "https://arquindex.com.br"
SITEMAP = "https://www.arquindex.com.br/sitemap-alfresco-cloud-20261021.xml"
CRITICAL = (
    ROOT + "/empresa.html",
    ROOT + "/blog/alfresco-cloud-ocr-inteligencia-documental/",
)
KNOWN_GOOD = (ROOT + "/", ROOT + "/solucoes/digitalizacao-documentos")
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.noindex = False
        self.links = []
        self.jsonld = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        if tag == "meta" and a.get("name", "").lower() == "robots":
            self.noindex |= "noindex" in a.get("content", "").lower()
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])


def fetch(url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": "ArquindexSEOAudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"status": response.status, "final_url": response.url, "body": response.read(3000000), "error": None}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "final_url": exc.url, "body": exc.read(100000), "error": str(exc)}
    except Exception as exc:
        return {"status": None, "final_url": url, "body": b"", "error": str(exc)}


def check_page(url, timeout):
    result = fetch(url, timeout)
    p = PageParser()
    if result["status"] == 200 and b"<html" in result["body"][:4000].lower():
        p.feed(result["body"].decode("utf-8", "replace"))
    return {"url": url, "status": result["status"], "final_url": result["final_url"],
            "canonical": p.canonicals, "noindex": p.noindex,
            "link_count": len(p.links), "error": result["error"]}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--timeout", type=int, default=12)
    a.add_argument("--output", default="seo-preflight-report.json")
    args = a.parse_args()
    sitemap_result = fetch(SITEMAP, args.timeout)
    report = {"sitemap": {"url": SITEMAP, "status": sitemap_result["status"],
                         "error": sitemap_result["error"]}, "pages": [], "blockers": []}
    urls = []
    if sitemap_result["status"] == 200:
        try:
            doc = ET.fromstring(sitemap_result["body"])
            if doc.tag != NS + "urlset":
                raise ValueError("Not a sitemap urlset")
            urls = [x.text.strip() for x in doc.findall("./" + NS + "url/" + NS + "loc") if x.text]
            report["sitemap"]["count"] = len(urls)
            report["sitemap"]["urls"] = urls
            if len(urls) != len(set(urls)):
                report["blockers"].append("duplicate_sitemap_urls")
            if len(urls) != 16:
                report["blockers"].append("sitemap_url_count_changed_review_required")
        except (ET.ParseError, ValueError) as exc:
            report["blockers"].append("invalid_sitemap_xml: " + str(exc))
    else:
        report["blockers"].append("sitemap_unavailable")
    for url in dict.fromkeys([*CRITICAL, *KNOWN_GOOD, *urls]):
        if not url.startswith(("https://arquindex.com.br/", "https://www.arquindex.com.br/")):
            report["blockers"].append("unexpected_host: " + url)
            continue
        p = check_page(url, args.timeout)
        report["pages"].append(p)
        if p["status"] != 200:
            report["blockers"].append("page_not_http_200: " + url)
        elif p["noindex"]:
            report["blockers"].append("page_noindex: " + url)
        elif p["canonical"] and not any(x.rstrip("/") == p["final_url"].rstrip("/") for x in p["canonical"]):
            report["blockers"].append("canonical_mismatch: " + url)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps({"sitemap_count": len(urls), "checked": len(report["pages"]),
                      "blockers": len(report["blockers"]), "output": args.output}, ensure_ascii=False))
    return 2 if report["blockers"] else 0


if __name__ == "__main__":
    sys.exit(main())
