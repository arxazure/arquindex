#!/usr/bin/env python3
"""Read-only check of robots.txt and XML sitemap endpoints on approved hosts."""
import argparse
import json
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

def check(url):
 result={"url":url}
 req=urllib.request.Request(url,headers={"User-Agent":"ArquindexSEOAudit/1.2 (+https://arquindex.com.br/)"})
 try:
  with urllib.request.urlopen(req,timeout=15) as response:
   result.update(status=response.status,final_url=response.url,content_type=response.headers.get("Content-Type",""))
   body=response.read(2000000)
  if url.endswith("robots.txt"):
   lines=body.decode("utf-8","replace").splitlines()
   result["sitemaps"]=[x.split(":",1)[1].strip() for x in lines if x.lower().startswith("sitemap:")]
   result["wildcard_disallow_all"]=any(x.strip().lower()=="disallow: /" for x in lines)
  else:
   root=ET.fromstring(body)
   tag=root.tag.split("}")[-1].lower()
   result["xml_root"]=tag
   result["url_count"]=len(root.findall("{*}url"))
   result["sitemap_count"]=len(root.findall("{*}sitemap"))
   if tag not in ("urlset","sitemapindex"):result["warning"]="unexpected_xml_root"
 except (urllib.error.URLError,ValueError,ET.ParseError,TimeoutError) as e:
  result["error"]=str(e)
 return result

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--site",default="https://arquindex.com.br/")
 ap.add_argument("--output",default="technical-endpoints.json")
 args=ap.parse_args()
 base=urllib.parse.urlsplit(args.site)
 if base.scheme!="https" or base.netloc not in ("arquindex.com.br","www.arquindex.com.br"):
  raise SystemExit("Only approved Arquindex hosts")
 robots=check(urllib.parse.urljoin(args.site,"/robots.txt"))
 sitemap_urls=robots.get("sitemaps",[])[:12]
 results=[robots]+[check(u) for u in sitemap_urls if urllib.parse.urlsplit(u).hostname and
  (urllib.parse.urlsplit(u).hostname=="arquindex.com.br" or urllib.parse.urlsplit(u).hostname.endswith(".arquindex.com.br"))]
 Path(args.output).write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(f"Endpoints inspected: {len(results)}; errors: {sum(bool(x.get('error')) for x in results)}")
if __name__=="__main__":main()
