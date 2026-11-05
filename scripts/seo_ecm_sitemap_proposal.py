#!/usr/bin/env python3
"""Create a REVIEW-ONLY ECM sitemap candidate from the live sitemap.

Reads only public HTTPS pages at ecm.arquindex.com.br, never publishes or submits.
"""
import json
import re
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ORIGIN = "https://ecm.arquindex.com.br"
MAX_BYTES = 2 * 1024 * 1024
MAX_URLS = 40
SKIP = re.compile(r"(?:google[a-f0-9]+|sitechecker[a-z0-9]+|bing[a-z0-9]+|yandex_[a-z0-9]+)\.html$", re.I)
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, url):
        return None

class HTMLMeta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "link" and "canonical" in d.get("rel", "").lower().split():
            self.canonicals.append(d.get("href", ""))
        if tag == "meta" and d.get("name", "").lower() in ("robots", "googlebot", "bingbot"):
            self.robots.append(d.get("content", ""))

def allowed(url):
    p = urlsplit(url)
    return (p.scheme == "https" and p.hostname == "ecm.arquindex.com.br"
            and p.port in (None, 443) and not p.username and not p.password
            and not p.query and not p.fragment and p.path.startswith("/"))

def fetch(url):
    if not allowed(url):
        raise ValueError("URL not permitted by ECM-only safety boundary")
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={"User-Agent": "Arquindex-ECM-Sitemap-Review/1.0"})
    try:
        try:
            response = opener.open(req, timeout=12)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Response too large")
            return response.status, dict(response.headers), data
    except urllib.error.URLError as exc:
        raise RuntimeError("network_error: " + str(exc.reason)) from exc

def extract_candidates(xml):
    root = ET.fromstring(xml)
    if root.tag.rsplit("}", 1)[-1] != "urlset":
        raise ValueError("Expected urlset, not sitemapindex")
    locs = [(n.text or "").strip() for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "loc"]
    if len(locs) > MAX_URLS:
        raise ValueError("Too many candidates for bounded review")
    candidates, rejected = [], []
    for value in locs:
        url = urljoin(ORIGIN + "/", value)
        if not allowed(url):
            rejected.append({"value": value, "reason": "outside_scope"})
        elif SKIP.search(urlsplit(url).path.rsplit("/", 1)[-1]):
            rejected.append({"value": value, "reason": "verification_token"})
        elif url not in candidates:
            candidates.append(url)
        else:
            rejected.append({"value": value, "reason": "duplicate"})
    return candidates, rejected

def validate(url):
    row = {"url": url, "accepted": False}
    try:
        status, headers, body = fetch(url)
        row["http_status"] = status
        if status != 200:
            row["reason"] = "not_http_200"
            return row
        if "text/html" not in headers.get("Content-Type", "").lower():
            row["reason"] = "not_html"
            return row
        parsed = HTMLMeta()
        parsed.feed(body.decode("utf-8", errors="replace"))
        robots = ",".join(parsed.robots + [headers.get("X-Robots-Tag", "")]).lower()
        if re.search(r"(?:^|[,;\s])noindex(?:$|[,;\s])", robots):
            row["reason"] = "noindex"
        elif len(parsed.canonicals) != 1:
            row["reason"] = "canonical_count_" + str(len(parsed.canonicals))
        elif urljoin(url, parsed.canonicals[0]) != url:
            row["reason"] = "canonical_other_target"
            row["canonical"] = parsed.canonicals[0]
        else:
            row["accepted"] = True
    except Exception as exc:
        row["reason"] = type(exc).__name__
        row["error"] = str(exc)[:240]
    return row

def run():
    status, headers, body = fetch(ORIGIN + "/sitemap.xml")
    if status != 200:
        raise ValueError("Live sitemap did not return HTTP 200")
    candidates, rejected = extract_candidates(body)
    checked = [validate(url) for url in candidates]
    passed = [item["url"] for item in checked if item["accepted"]]
    # Refuse to produce an incomplete replacement if a page cannot be verified.
    report = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "source": ORIGIN + "/sitemap.xml", "source_count": len(candidates) + len(rejected),
              "eligible": passed, "checked": checked, "excluded": rejected,
              "ready_for_human_review": len(passed) > 0 and all(
                  r["accepted"] or r.get("reason") in {"canonical_other_target", "noindex", "not_http_200", "canonical_count_0", "canonical_count_2"}
                  for r in checked),
              "published": False, "submitted": False,
              "warning": "Candidate only: human approval, backed-up deployment and post-deploy verification required."}
    dest = Path("seo-report/ecm-sitemap-proposal")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not passed:
        print("No eligible pages: XML not produced")
        return
    ET.register_namespace("", NS)
    root = ET.Element("{" + NS + "}urlset")
    for url in passed:
        ET.SubElement(ET.SubElement(root, "{" + NS + "}url"), "{" + NS + "}loc").text = url
    ET.ElementTree(root).write(dest / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    print(json.dumps({"eligible": len(passed), "excluded": len(rejected),
                      "needs_review": sum(not r["accepted"] for r in checked),
                      "ready_for_human_review": report["ready_for_human_review"],
                      "published": False}))

if __name__ == "__main__":
    run()
