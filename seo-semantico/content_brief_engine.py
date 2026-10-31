#!/usr/bin/env python3
"""Competitive topic research -> SEO brief -> original, review-required draft.
Only approved HTTPS URLs. Respect robots.txt. No automated posting or ranking claims.
"""
import argparse
from collections import Counter
from datetime import date
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

UA = "ArquindexContentResearch/1.0 (+https://www.arquindex.com.br/)"
STOP = set("""para como mais sobre entre pelas pelos esta esse esses essas numa desta deste
onde quando porque quais qual seus suas todo toda todos todas uma umas uns dos das
com sem por aos nas nos que não sim são foi tem ser ter sua seu eles elas pelo
the and for with this from into your esse sobre ainda também muito cada""".split())
SEED = {
 "digitalizacao": ["digitalização certificada", "OCR pesquisável", "indexação", "PDF/A",
                    "conferência de qualidade", "metadados", "rastreabilidade"],
 "alfresco": ["Alfresco Community", "ECM", "fluxo de aprovação", "metadados",
              "permissões", "versionamento", "integração"],
 "lgpd": ["LGPD", "inventário de dados", "ROPA", "RIPD", "encarregado",
          "direitos dos titulares", "governança"],
 "ged": ["gestão eletrônica de documentos", "temporalidade", "classificação",
         "retenção", "auditoria", "controle de acesso"],
}

class Reader(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.title = ""; self.headings=[]; self.paragraphs=[]
  self._capture=None; self._buf=[]; self._skip=0
 def handle_starttag(self, tag, attrs):
  if tag in ("script","style","nav","footer","header"): self._skip+=1
  if not self._skip and tag in ("title","h1","h2","h3","p"):
   self._capture=tag; self._buf=[]
 def handle_data(self, value):
  if self._capture and not self._skip:self._buf.append(value)
 def handle_endtag(self, tag):
  if self._capture==tag:
   value=re.sub(r"\s+"," "," ".join(self._buf)).strip()
   if value:
    if tag=="title":self.title+=value
    elif tag in ("h1","h2","h3"):self.headings.append(value)
    else:self.paragraphs.append(value)
   self._capture=None;self._buf=[]
  if tag in ("script","style","nav","footer","header"):
   self._skip=max(0,self._skip-1)

def slug(value):
 value=re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-")
 return value[:65] or "site"

def public_https(url):
 parsed=urlsplit(url)
 return parsed.scheme=="https" and bool(parsed.hostname) and not parsed.username and not parsed.password

def collect(url, delay=2.0):
 if not public_https(url):raise ValueError("Only public HTTPS URLs accepted")
 origin=urlsplit(url)
 robots=RobotFileParser()
 robots.set_url(f"{origin.scheme}://{origin.netloc}/robots.txt")
 try:robots.read()
 except Exception as exc:raise ValueError("robots.txt not accessible: "+str(exc)) from exc
 if not robots.can_fetch(UA,url):raise ValueError("robots.txt disallows URL")
 time.sleep(max(0, delay))
 req=Request(url,headers={"User-Agent":UA,"Accept":"text/html"})
 with urlopen(req,timeout=15) as response:
  final=response.geturl()
  if not public_https(final):raise ValueError("Redirected away from HTTPS")
  if "text/html" not in response.headers.get("Content-Type","").lower():
   raise ValueError("Not HTML")
  raw=response.read(500001)
  if len(raw)>500000:raise ValueError("Page exceeds 500KB inspection limit")
  reader=Reader()
  reader.feed(raw.decode("utf-8","replace"))
  return {"url":final,"title":reader.title,"headings":reader.headings[:30],
          "paragraphs":reader.paragraphs[:120]}

def entities(pages, seed):
 corpus=" ".join(" ".join(p["headings"]+p["paragraphs"]) for p in pages).lower()
 words=re.findall(r"[a-záàâãéêíóôõúç0-9][a-záàâãéêíóôõúç0-9/-]*",corpus)
 terms=[w for w in words if len(w)>3 and w not in STOP]
 frequency=Counter(terms)
 phrases=Counter(" ".join(pair) for pair in zip(terms,terms[1:]) if pair[0]!=pair[1])
 selected=[p for p,n in phrases.most_common(30) if n>=2][:15]
 return {"seed_topics":seed,"frequent_terms":[w for w,n in frequency.most_common(25)],
         "candidate_phrases":selected}

def build_brief(topic, config, pages, analysis):
 title=config["title"]
 headings=list(dict.fromkeys(x for p in pages for x in p["headings"]))
 seed=analysis["seed_topics"]
 subtopics=list(dict.fromkeys(seed+analysis["candidate_phrases"][:8]))
 return {"topic":topic,"target_audience":"Empresas e equipes de compras, TI, jurídico e gestão documental",
  "search_intent":"Pesquisa técnica e contratação B2B",
  "proposed_title":title,
  "key_questions":[f"Como avaliar {title.lower()} para uma empresa?",
                   "Quais etapas, entregáveis e controles devem constar no escopo?",
                   "Quais critérios técnicos e de segurança devem ser verificados?",
                   "Como solicitar uma proposta com volumes e requisitos definidos?"],
  "recommended_subtopics":subtopics,
  "competitor_heading_patterns":headings[:20],
  "sources":[p["url"] for p in pages],
  "editorial_requirements":["Confirmar dados técnicos e legais em fontes oficiais",
       "Adicionar autoria e revisão técnica", "Incluir exemplo original autorizado",
       "Verificar alegações comerciais e preços antes de publicar",
       "Não copiar estrutura ou trechos de concorrentes"],
  "status":"draft_review_required"}

def render(brief):
 title=brief["proposed_title"]
 sections=[
  f"# {title}",
  "",
  "> RASCUNHO PARA REVISÃO — não publicar automaticamente. Validar afirmações técnicas, fontes, autoria e serviços ofertados.",
  "",
  f"Empresas que avaliam {title.lower()} precisam definir objetivos, tipos documentais, volumes, integrações, prazos e controles de acesso antes de contratar uma solução. Este guia organiza os pontos de decisão para a equipe responsável.",
 ]
 for term in brief["recommended_subtopics"][:10]:
  sections.extend(["",f"## {term[0].upper()+term[1:]}",
   f"Na avaliação de {term.lower()}, documente os requisitos, os responsáveis pela execução, os critérios de aceite e as evidências verificáveis. Registre como essa etapa se conecta ao processo documental e quais limitações devem ser avaliadas.",
   "",
   "**A complementar na revisão:** exemplo real, fonte técnica e particularidades do serviço Arquindex."])
 sections.extend(["","## Perguntas para tomada de decisão"])
 for question in brief["key_questions"]:
  sections.extend(["",f"### {question}",
   "Defina o escopo com a equipe responsável e peça evidências documentadas de capacidade, segurança, metodologia e entregáveis antes da decisão."])
 sections.extend(["","## Solicite uma avaliação de escopo",
  "Para uma proposta B2B, informe volumes aproximados, formatos dos arquivos, localização do acervo, requisitos de OCR e indexação, temporalidade e necessidades de integração.",
  "",
  "**Revisão pendente:** inserir link de contato confirmado, autor, data e referências oficiais."])
 return "\n".join(sections)+"\n"

def run(config, out, skip_fetch=False):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 summaries={}
 for topic, item in config["briefs"].items():
  pages=[]
  for url in item.get("competitor_urls",[]):
   host=urlsplit(url).hostname or ""
   folder=out/"concorrentes"/slug(host)
   if not folder.exists():os.mkdir(folder) if folder.parent.exists() else folder.mkdir(parents=True)
   try:
    if skip_fetch:raise ValueError("Offline mode: no scraping performed")
    page=collect(url)
    pages.append(page)
    # Save metadata/headings, not a mirror of competitor text.
    (folder/(slug(topic)+".json")).write_text(json.dumps(
     {"url":page["url"],"title":page["title"],"headings":page["headings"]},
     ensure_ascii=False,indent=2),encoding="utf-8")
   except Exception as exc:
    (folder/(slug(topic)+"-error.txt")).write_text(str(exc),encoding="utf-8")
  analysis=entities(pages,SEED.get(topic,[]))
  brief=build_brief(topic,item,pages,analysis)
  target=out/"briefs"/slug(topic)
  target.mkdir(parents=True,exist_ok=True)
  (target/"brief.json").write_text(json.dumps(brief,ensure_ascii=False,indent=2),encoding="utf-8")
  (target/"rascunho.md").write_text(render(brief),encoding="utf-8")
  summaries[topic]={"references_analyzed":len(pages),"brief":str(target/"brief.json"),
                    "draft":str(target/"rascunho.md")}
 (out/"summary.json").write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding="utf-8")
 return summaries

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--config",required=True);p.add_argument("--output",default="saida-seo")
 p.add_argument("--offline",action="store_true",help="Create briefs and drafts without requests")
 args=p.parse_args()
 config=json.loads(Path(args.config).read_text(encoding="utf-8"))
 print(json.dumps(run(config,args.output,args.offline),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
