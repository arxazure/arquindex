#!/usr/bin/env python3
"""Read-only HTTPS preflight for an explicitly reviewed list of Arquindex URLs.
No deploy, indexing API, authentication or state mutation. Never follow redirects.
"""
import argparse
import json
import re
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_URLS = [
    "https://www.arquindex.com.br/",
    "https://www.arquindex.com.br/gestao-documental/",
    "https://www.arquindex.com.br/robots.txt",
    "https://www.arquindex.com.br/sitemap.xml",
    "https://ecm.arquindex.com.br/custo.html",
]
MAX_BODY = 2 * 1024 * 1024
class Meta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []
        self.title = ""
        self._title = False
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "title":
            self._title = True
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name", "").lower() in {"robots", "googlebot", "bingbot"}:
            self.robots.append(attrs.get("content", ""))
    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
    def handle_data(self, data):
        if self._title:
            self.title += data

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def check(url):
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    # Hard boundary: only an explicitly approved Arquindex domain over HTTPS.
    if parsed.scheme != "https" or parsed.port not in (None, 443) or parsed.username or parsed.password or parsed.fragment or (
        host != "arquindex.com.br" and not host.endswith(".arquindex.com.br")
    ):
        return {"url": url, "state": "rejected", "reason": "outside_explicit_https_scope"}
    row = {"url": url, "state": "unknown", "http_status": None, "location": None,
           "canonical": [], "robots": [], "title": None, "observed_at": datetime.now(timezone.utc).isoformat()}
    req = urllib.request.Request(url, headers={"User-Agent": "Arquindex-SEO-Live-Preflight/1.0"})
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        try:
            response = opener.open(req, timeout=12)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            row["http_status"] = response.status
            row["location"] = response.headers.get("Location")
            xrobots = response.headers.get("X-Robots-Tag")
            if xrobots:
                row["robots"].append("header: " + xrobots)
            if response.status == 200 and "html" in response.headers.get("Content-Type", "").lower():
                body = response.read(MAX_BODY + 1)
                if len(body) > MAX_BODY:
                    row["state"] = "oversize"
                    return row
                meta = Meta()
                meta.feed(body.decode("utf-8", errors="replace"))
                row["canonical"] = meta.canonicals
                row["robots"] += meta.robots
                row["title"] = meta.title.strip()[:240]
            row["state"] = "observed"
    except Exception as exc:
        row["state"] = "unverified"
        row["error_type"] = type(exc).__name__
        row["error"] = str(exc)[:300]
    return row

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="seo-report/live-preflight.json")
    p.add_argument("--urls", nargs="*", default=DEFAULT_URLS)
    args = p.parse_args()
    if len(args.urls) > 20:
        p.error("At most 20 explicitly reviewed URLs")
    rows = [check(url) for url in args.urls]
    report = {"mode": "read_only", "checked_at": datetime.now(timezone.utc).isoformat(),
              "urls": rows, "notes": ["HTTP observation does not establish Google/Bing indexing.",
              "Errors are unverified, not proof of HTTP 404.", "Redirects never followed.",
              "No sitemap submission, website edits or DNS changes."]}
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"observed": sum(r["state"] == "observed" for r in rows),
                       "unverified": sum(r["state"] == "unverified" for r in rows),
                       "report": str(target)}))
if __name__ == "__main__":
    main()
