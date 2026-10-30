#!/usr/bin/env python3
"""Generate truthful, reviewable JSON-LD service blocks from explicit input."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_TYPES = {"Service", "Article"}
def validate_url(value):
 p=urlparse(value)
 if p.scheme != "https" or not p.netloc or p.username or p.password:
  raise ValueError("URLs must be absolute HTTPS addresses")
 return value

def build(item):
 for key in ("type","url","title","description"):
  if not isinstance(item.get(key),str) or not item[key].strip():
   raise ValueError("Missing required field: "+key)
 if item["type"] not in ALLOWED_TYPES:
  raise ValueError("Unsupported type")
 url=validate_url(item["url"])
 graph={
  "@context":"https://schema.org",
  "@type":item["type"],
  "@id":url+"#"+item["type"].lower(),
  "url":url,
  "name" if item["type"]=="Service" else "headline":item["title"],
  "description":item["description"],
 }
 if item["type"]=="Service":
  graph["provider"]={"@type":"Organization","name":"Arquindex Gestão Documental LTDA","url":"https://www.arquindex.com.br/"}
  if item.get("serviceType"):graph["serviceType"]=item["serviceType"]
  if item.get("areaServed"):graph["areaServed"]=[{"@type":"AdministrativeArea","name":a} for a in item["areaServed"]]
 else:
  for field in ("datePublished","dateModified"):
   if item.get(field):graph[field]=item[field]
  if item.get("author"):
   graph["author"]={"@type":"Person","name":item["author"]}
 return graph

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--input",required=True);parser.add_argument("--output",required=True)
 args=parser.parse_args()
 items=json.loads(Path(args.input).read_text(encoding="utf-8"))
 if not isinstance(items,list):raise ValueError("Expected an array")
 result=[build(item) for item in items]
 Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("Generated",len(result),"reviewable JSON-LD blocks")
if __name__=="__main__":main()
