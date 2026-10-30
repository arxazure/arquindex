#!/usr/bin/env python3
"""Rank *review candidates* from an exported GSC query report, offline."""
import argparse
import csv
import json
import re
from pathlib import Path

TOPICS = {
 "digitalizacao": r"digitaliza|ocr|escane|scanner",
 "alfresco_ecm": r"alfresco|\becm\b|\bged\b|gest[aã]o de documentos|gest[aã]o documental",
 "lgpd": r"lgpd|\bdpo\b|prote[cç][aã]o de dados|privacidade|\bropa\b|\bripd\b",
 "guarda": r"guarda|armazen|arquivamento|acervo",
}
def classify(query):
 for label, pattern in TOPICS.items():
  if re.search(pattern,query,re.I):return label
 return None

def prioritize(rows, min_impressions=10):
 output=[]
 for row in rows:
  query=str(row.get("query","")).strip()
  topic=classify(query)
  if not topic:continue
  try:
   impressions=int(float(row.get("impressions",0)))
   clicks=int(float(row.get("clicks",0)))
   position=float(row.get("position",0))
  except (ValueError,TypeError):continue
  if impressions<min_impressions or not 1<=position<=60:continue
  tier="near_top10" if 4<=position<=20 else "needs_foundation"
  if position<4:tier="defend_existing"
  score=round(impressions*max(0,61-position)/60,2)
  output.append(dict(query=query,topic=topic,impressions=impressions,
                     clicks=clicks,position=round(position,2),tier=tier,score=score))
 return sorted(output,key=lambda row:(-row["score"],-row["impressions"],row["query"]))

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--input",required=True,help="CSV: query,clicks,impressions,position")
 ap.add_argument("--output",default="gsc-opportunities.md")
 ap.add_argument("--min-impressions",type=int,default=10)
 args=ap.parse_args()
 with open(args.input,encoding="utf-8-sig",newline="") as stream:
  rows=list(csv.DictReader(stream))
 found=prioritize(rows,args.min_impressions)
 lines=["# Arquindex — oportunidades por consulta (GSC)","",
        "Triagem heurística, não estimativa de ranking nem promessa de Top 10.","",
        "| Tema | Consulta | Impressões | Cliques | Posição | Prioridade |",
        "|---|---|---:|---:|---:|---|"]
 for r in found:
  q=r["query"].replace("|","\\|").replace("\n"," ")
  lines.append(f'| {r["topic"]} | {q} | {r["impressions"]} | {r["clicks"]} | {r["position"]} | {r["tier"]} |')
 Path(args.output).write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(f"Candidates: {len(found)}; report: {args.output}")
if __name__=="__main__":main()
