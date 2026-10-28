"""Regressão das três páginas comerciais estáticas em staging."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"staging"/"seo"/"paginas-pilares-20261028"
SLUGS=[
 "contratar-digitalizacao-documentos-armazenamento-nuvem",
 "compliance-digitalizacao-preco",
 "mapeamento-juridico",
]
class Tags(HTMLParser):
 def __init__(self):
  super().__init__();self.tags={};self.links=[];self.canonicals=[];self.titles=[];self._title=False;self._title_text=""
 def handle_starttag(self,tag,attrs):
  self.tags[tag]=self.tags.get(tag,0)+1
  d=dict(attrs)
  if tag=="a":self.links.append(d.get("href",""))
  if tag=="link" and "canonical" in d.get("rel","").split():self.canonicals.append(d.get("href",""))
  if tag=="title":self._title=True;self._title_text=""
 def handle_endtag(self,tag):
  if tag=="title":self._title=False;self.titles.append(self._title_text.strip())
 def handle_data(self,data):
  if self._title:self._title_text+=data

class LandingPages(unittest.TestCase):
 def test_structure_and_contextual_links(self):
  for slug in SLUGS:
   with self.subTest(slug=slug):
    html=(ROOT/slug/"index.html").read_text(encoding="utf-8")
    p=Tags();p.feed(html)
    self.assertEqual(p.tags.get("h1"),1)
    self.assertEqual(p.tags.get("main"),1)
    self.assertEqual(p.tags.get("title"),1)
    self.assertEqual(len(p.canonicals),1)
    self.assertEqual(p.canonicals[0],f"https://{slug}.arquindex.com.br/")
    self.assertTrue(p.titles[0])
    self.assertIn('application/ld+json',html)
    self.assertIn('name="description"',html)
    self.assertIn('name="viewport"',html)
    self.assertIn('class="faq"',html)
    self.assertIn('arquindex-logo-oficial.webp',html)
    self.assertTrue(all(any(f"https://{other}.arquindex.com.br/"==url for url in p.links) for other in SLUGS if other!=slug))
    self.assertNotIn('aggregateRating',html)
    self.assertNotIn('"review"',html)

if __name__=="__main__":unittest.main()
