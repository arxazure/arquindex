#!/usr/bin/env python3
"""Propose semantic blog enrichment without altering existing HTML or publishing."""
import argparse, csv, html, json, re
from pathlib import Path
from urllib.parse import urlparse

STOP={"para","sobre","como","mais","com","uma","dos","das","por","que","seus","suas","este","esta"}
def words(s):
    return set(re.findall(r"[\wÀ-ÿ]{4,}",s.lower()))-STOP
def choose_terms(article, research, limit=6):
    text=" ".join([article.get("title",""),article.get("description",""),article.get("body","")])
    original=words(text)
    candidates=[str(x).strip() for x in research.get("seed_topics",[])+research.get("candidate_phrases",[])]
    selected=[]
    for term in candidates:
        tok=words(term)
        if tok and (tok & original) and term.casefold() not in text.casefold() and term not in selected:
            selected.append(term)
    return selected[:limit]
def proposals(article, research):
    terms=choose_terms(article,research)
    title=article["title"]
    desc=article.get("description","")
    return {"url":article["url"],"current_title":title,"current_description":desc,
            "recommended_terms":terms,
            "suggested_meta_description":(desc if desc else (title+". Entenda aplicações, requisitos e cuidados técnicos na gestão documental. "))[:155],
            "suggested_section_title":"Aspectos técnicos e perguntas frequentes",
            "suggested_section_text":("Uma avaliação completa deve considerar "+", ".join(terms[:4])+
                ", com fontes verificáveis e exemplos próprios." if terms else
                "Não foram identificados termos novos suficientemente relacionados; revisar manualmente."),
            "approval_required":True}
def run(articles,research):
    return [proposals(a,research.get(a.get("topic",""),{})) for a in articles]
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--articles",required=True,help="JSON list: url, title, description, body, topic")
    p.add_argument("--research",required=True,help="JSON mapping topic -> semantic data")
    p.add_argument("--output",default="blog-semantic-review.json")
    a=p.parse_args()
    result=run(json.loads(Path(a.articles).read_text(encoding="utf-8")),
               json.loads(Path(a.research).read_text(encoding="utf-8")))
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Proposals generated: {len(result)}")
if __name__=="__main__":main()
