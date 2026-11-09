#!/usr/bin/env python3
"""Inspect robots.txt and sitemap.xml over HTTPS; read-only, no redirects."""
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

SITES = ["https://www.arquindex.com.br", "https://ecm.arquindex.com.br"]
MAX_BYTES = 2 * 1024 * 1024

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch(url):
    opener = urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(url, headers={"User-Agent": "Arquindex-SEO-ReadOnly/1.0"})
    try:
        try:
            response = opener.open(request, timeout=15)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            data = response.read(MAX_BYTES + 1)
            return {"status": response.status, "content_type": response.headers.get("Content-Type", ""),
                    "too_large": len(data) > MAX_BYTES,
                    "body": data[:MAX_BYTES].decode("utf-8", errors="replace")}
    except Exception as exc:
        return {"error": type(exc).__name__, "detail": str(exc)[:240]}

def inspect_robots(body):
    groups = []
    sitemaps = []
    disallow_all = False
    active_agents = []
    for line in body.splitlines():
        text = line.split("#", 1)[0].strip()
        if ":" not in text:
            continue
        name, value = (x.strip() for x in text.split(":", 1))
        name = name.lower()
        if name == "user-agent":
            active_agents.append(value.lower())
            groups.append(value)
        elif name == "sitemap":
            sitemaps.append(value)
            active_agents = []
        elif name == "disallow" and value == "/" and "*" in active_agents:
            disallow_all = True
    return {"agents_seen": sorted(set(groups)), "sitemap_directives": sorted(set(sitemaps)),
            "possible_global_disallow": disallow_all,
            "warning": "Robots group semantics need manual verification; flag is only a heuristic."}

def inspect_sitemap(body, site):
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        return {"valid_xml": False, "error": str(exc)[:150]}
    kind = root.tag.rsplit("}", 1)[-1]
    locs = [(node.text or "").strip() for node in root.iter()
            if node.tag.rsplit("}", 1)[-1] == "loc"]
    hosts = sorted({urlsplit(loc).hostname for loc in locs if urlsplit(loc).hostname})
    return {"valid_xml": kind in {"urlset", "sitemapindex"}, "root_type": kind,
            "loc_count": len(locs), "hosts": hosts,
            "cross_host_locations": sum(urlsplit(loc).hostname != urlsplit(site).hostname for loc in locs),
            "examples": locs[:8],
            "notes": "Cross-host locations are not always an error; inspect delegation and sitemap ownership."}

def main():
    output = {"checked_at": datetime.now(timezone.utc).isoformat(),
              "scope": "two explicitly approved hosts, read-only", "results": []}
    for site in SITES:
        entry = {"site": site}
        for path, key in [("/robots.txt", "robots"), ("/sitemap.xml", "sitemap")]:
            response = fetch(site + path)
            public = {k: v for k, v in response.items() if k != "body"}
            if response.get("status") == 200 and not response.get("too_large"):
                public["analysis"] = (inspect_robots(response["body"]) if key == "robots"
                                      else inspect_sitemap(response["body"], site))
            entry[key] = public
        output["results"].append(entry)
    dest = Path("seo-report/robots-sitemap-live.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(dest), "hosts": len(output["results"]),
                      "statuses": [{ "site": row["site"], "robots": row["robots"].get("status"),
                                    "sitemap": row["sitemap"].get("status")} for row in output["results"]]}))

if __name__ == "__main__":
    main()
