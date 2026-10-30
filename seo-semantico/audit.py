#!/usr/bin/env python3
"""Arquindex semantic SEO audit: read-only, stdlib-only, safe by default."""
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
  super().__init__(); self.title=""; self.h1=[]; self.meta={}; self.links=[]; self.jsonld=[]; self.current=None; self.skip=0; self.body=[]
 def handle_starttag(self, tag, attrs):
  a=dict(attrs)
  if tag in ("script","style"): self.skip+=1
  if tag=="title": self.current="title"
  if tag=="h1": self.current="h1"; self.h1.append("")
  if tag=="meta":
   k=(a.get("name") or a.get("property") or "").lower()
   if k: self.meta[k]=a.get("content","")
  if tag=="link": self.links.append(a)
 def handle_endtag(self,tag):
  if tag in ("script","style"): self.skip=max(0,self.skip-1)
  if tag in ("title","h1"): self.current=None
 def handle_data(self,data):
  if self.current=="title": self.title+=data
  elif self.current=="h1": self.h1[-1]+=data
  elif not self.skip: self.body.append(data)
def audit(url):
 req=urllib.request.Request(url,headers={"User-Agent":"ArquindexSEOAudit/1.0 (+https://www.arquindex.com.br/)"})
 result={"url":url}
 try:
  with urllib.request.urlopen(req,timeout=12) as r:
   result["status"]=r.status; result["final_url"]=r.url
   result["content_type"]=r.headers.get("Content-Type","")
   html=r.read(1000000).decode("utf-8","replace")
  if "html" not in result["content_type"].lower(): return result
  p=Page();p.feed(html)
  txt=" ".join(p.body).lower()
  canonical=next((x.get("href") for x in p.links if "canonical" in x.get("rel","").lower()),None)
  result.update(title=p.title.strip(),h1=p.h1,description=p.meta.get("description",""),canonical=canonical,
   robots=p.meta.get("robots",""),word_count=len(txt.split()),
   topics={k:sum(txt.count(term) for term in terms) for k,terms in TOPICS.items()},
   internal_links=sum(1 for x in p.links if x.get("href","").startswith("/")),
   issues=[])
  if not p.title.strip():result["issues"].append("missing_title")
  if len(p.h1)!=1:result["issues"].append("h1_count")
  if not p.meta.get("description"):result["issues"].append("missing_description")
  if not canonical:result["issues"].append("missing_canonical")
  if "noindex" in p.meta.get("robots","").lower():result["issues"].append("noindex")
  if len(txt.split())<150:result["issues"].append("thin_content_review")
 except Exception as e:result["error"]=str(e)
 return result

def main():
 a=argparse.ArgumentParser();a.add_argument("--sites",required=True,help="one URL per line");a.add_argument("--output",default="seo-audit.json");a.add_argument("--workers",type=int,default=4);args=a.parse_args()
 urls=[s.strip() for s in Path(args.sites).read_text().splitlines() if s.strip() and not s.lstrip().startswith("#")]
 urls=list(dict.fromkeys(u for u in urls if urllib.parse.urlsplit(u).scheme in ("http","https")))
 with concurrent.futures.ThreadPoolExecutor(max_workers=min(5,max(1,args.workers))) as pool: data=list(pool.map(audit,urls))
 Path(args.output).write_text(json.dumps({"audited":len(data),"results":data},ensure_ascii=False,indent=2),encoding="utf-8")
 print("Audited:",len(data),"Errors:",sum("error" in x for x in data))
if __name__=="__main__":main()
