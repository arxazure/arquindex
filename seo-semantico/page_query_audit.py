#!/usr/bin/env python3
"""Analyze page-query GSC rows; never change canonical or delete sites automatically."""
import argparse,csv,collections,json,re
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode

def canonicalize_candidate(url):
 p=urlsplit(url)
 # For comparison only. Query params are not stripped blindly, as they can identify content.
 return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path or "/",p.query,""))

def analyze(rows):
 by_query=collections.defaultdict(list)
 by_page=collections.defaultdict(list)
 for r in rows:
  query=(r.get("query") or "").strip()
  page=(r.get("page") or "").strip()
  if not query or not page:continue
  try:
   record={"query":query,"page":canonicalize_candidate(page),
           "clicks":float(r.get("clicks",0)),"impressions":float(r.get("impressions",0)),
           "position":float(r.get("position",0))}
  except (ValueError,TypeError):continue
  by_query[query.casefold()].append(record)
  by_page[record["page"]].append(record)
 duplicates=[]
 for query,items in by_query.items():
  urls={x["page"] for x in items}
  if len(urls)>1:
   duplicates.append({"query":query,"page_count":len(urls),"impressions":sum(x["impressions"] for x in items),
                      "pages":sorted(urls),"review":"Overlap is not proof of harmful cannibalization"})
 duplicates.sort(key=lambda x:(-x["impressions"],-x["page_count"]))
 return {"query_page_overlaps":duplicates,"page_count":len(by_page),
         "query_count":len(by_query),"rows_read":sum(len(x) for x in by_query.values())}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--input",required=True,help="CSV with query,page,clicks,impressions,position")
 ap.add_argument("--output",default="page-query-report.json")
 args=ap.parse_args()
 with open(args.input,encoding="utf-8-sig",newline="") as f:
  report=analyze(csv.DictReader(f))
 Path(args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(f'Queries: {report["query_count"]}; overlapping: {len(report["query_page_overlaps"])}')
if __name__=="__main__":main()
