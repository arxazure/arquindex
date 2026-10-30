#!/usr/bin/env python3
"""Read-only SEO inspection for explicitly approved Arquindex URLs."""
import argparse
import concurrent.futures
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

TOPICS = {
 "digitalizacao": ["digitalização", "digitalizacao", "ocr", "pdf/a", "decreto 10.278"],
 "alfresco": ["alfresco", "ecm", "gestão documental", "gestao documental"],
 "lgpd": ["lgpd", "dpo", "proteção de dados", "protecao de dados", "ropa", "ripd"],
 "guarda": ["guarda documental", "armazenamento de documentos", "arquivo físico"],
}

class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.title = ""; self.h1 = []; self.meta = {}; self.links = []
  self.anchors = []; self.body = []
  self._title = False; self._h1 = False; self._skip = 0
 def handle_starttag(self, tag, attrs):
  a = dict(attrs)
  if tag in ("script", "style", "noscript"): self._skip += 1
  if tag == "title": self._title = True
  if tag == "h1": self._h1 = True; self.h1.append("")
  if tag == "meta":
   key = (a.get("name") or a.get("property") or "").lower()
   if key: self.meta[key] = a.get("content", "")
  if tag == "link": self.links.append(a)
  if tag == "a": self.anchors.append(a.get("href", ""))
 def handle_endtag(self, tag):
  if tag in ("script", "style", "noscript"): self._skip = max(0, self._skip-1)
  if tag == "title": self._title = False
  if tag == "h1": self._h1 = False
 def handle_data(self, data):
  if self._title: self.title += data
  elif self._h1: self.h1[-1] += data
  if not self._skip: self.body.append(data)

def parse_html(html, url):
 p = Page(); p.feed(html)
 text = " ".join(p.body).lower()
 rel = lambda item: (item.get("rel") or "").lower().split()
 canonical = next((x.get("href") for x in p.links if "canonical" in rel(x)), None)
 canonical = urllib.parse.urljoin(url, canonical) if canonical else None
 issues = []
 if not p.title.strip(): issues.append("missing_title")
 if len(p.h1) != 1: issues.append("h1_count")
 if not p.meta.get("description", "").strip(): issues.append("missing_description")
 if not canonical: issues.append("missing_canonical")
 if "noindex" in p.meta.get("robots", "").lower(): issues.append("noindex")
 if len(text.split()) < 150: issues.append("thin_content_review")
 if canonical and urllib.parse.urlsplit(canonical).netloc != urllib.parse.urlsplit(url).netloc:
  issues.append("external_canonical_review")
 return {
  "title": p.title.strip(), "h1": [x.strip() for x in p.h1],
  "description": p.meta.get("description", ""), "canonical": canonical,
  "robots": p.meta.get("robots", ""), "word_count": len(text.split()),
  "topics": {k: sum(text.count(t) for t in ts) for k, ts in TOPICS.items()},
  "internal_links": sum(1 for href in p.anchors if href and
    urllib.parse.urlsplit(urllib.parse.urljoin(url, href)).netloc ==
    urllib.parse.urlsplit(url).netloc),
  "issues": issues
 }

def audit(url):
 result = {"url": url}
 request = urllib.request.Request(url, headers={"User-Agent": "ArquindexSEOAudit/1.1 (+https://www.arquindex.com.br/)"})
 try:
  with urllib.request.urlopen(request, timeout=12) as response:
   result.update(status=response.status, final_url=response.url,
                 content_type=response.headers.get("Content-Type", ""))
   raw = response.read(1000000)
  if "html" not in result["content_type"].lower(): return result
  result.update(parse_html(raw.decode("utf-8", "replace"), result["final_url"]))
 except urllib.error.HTTPError as exc:
  result.update(status=exc.code, error=f"HTTP {exc.code}")
 except (urllib.error.URLError, TimeoutError, ValueError) as exc:
  result["error"] = str(exc)
 return result

def main():
 ap = argparse.ArgumentParser()
 ap.add_argument("--sites", required=True)
 ap.add_argument("--output", default="seo-audit.json")
 ap.add_argument("--workers", type=int, default=2)
 args = ap.parse_args()
 urls = [s.strip() for s in Path(args.sites).read_text(encoding="utf-8").splitlines()
         if s.strip() and not s.lstrip().startswith("#")]
 urls = list(dict.fromkeys(u for u in urls if urllib.parse.urlsplit(u).scheme in ("http", "https")))
 with concurrent.futures.ThreadPoolExecutor(max_workers=min(3, max(1, args.workers))) as pool:
  results = list(pool.map(audit, urls))
 Path(args.output).write_text(json.dumps({"audited": len(results), "results": results},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
 print(f"Audited {len(results)} URLs; errors: {sum('error' in r for r in results)}")
if __name__ == "__main__": main()
