#!/usr/bin/env python3
"""Read-only SEO audit for a public site. No credentials or production writes."""
import argparse
import json
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

UA = "ArquindexSEOAudit/1.0 (+manual GitHub Actions)"
def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read(1_000_000)
            return {"url": response.geturl(), "status": response.status,
                    "content_type": response.headers.get("Content-Type", ""),
                    "text": data.decode("utf-8", errors="replace")}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "content_type": "", "text": ""}
    except Exception as e:
        return {"url": url, "status": None, "error": str(e), "text": ""}

def audit(site):
    origin = urllib.parse.urlsplit(site)
    if origin.scheme != "https" or not origin.hostname:
        raise ValueError("Use a public HTTPS URL")
    base = urllib.parse.urlunsplit((origin.scheme, origin.netloc, "", "", ""))
    home = get(base + "/")
    robots = get(base + "/robots.txt")
    sitemap = get(base + "/sitemap.xml")
    html = home.get("text", "").lower()
    result = {
        "site": base,
        "homepage": {"status": home.get("status"), "final_url": home.get("url"),
                     "has_title": "<title" in html,
                     "has_meta_description": 'name="description"' in html or "name='description'" in html,
                     "has_canonical": 'rel="canonical"' in html or "rel='canonical'" in html,
                     "has_json_ld": "application/ld+json" in html},
        "robots": {"status": robots.get("status"), "mentions_sitemap": "sitemap:" in robots.get("text", "").lower()},
        "sitemap": {"status": sitemap.get("status"), "xml_valid": False},
    }
    if sitemap.get("status") == 200:
        try:
            root = ET.fromstring(sitemap["text"])
            result["sitemap"]["xml_valid"] = root.tag.endswith(("urlset", "sitemapindex"))
            result["sitemap"]["root_tag"] = root.tag.split("}")[-1]
        except ET.ParseError:
            pass
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="https://arquindex.com.br")
    args = parser.parse_args()
    print(json.dumps(audit(args.site), ensure_ascii=False, indent=2))
