from pathlib import Path
from html.parser import HTMLParser
import json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]
rows=json.loads((R/'seo/autoridade-20261030-manifest.json').read_text())
class Check(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.canonical=[];self.schemas=[];self.inschema=False;self.schema='';self.hrefs=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if t=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if t=='script' and a.get('type')=='application/ld+json':self.inschema=True;self.schema=''
  if t=='a':self.hrefs.append(a.get('href',''))
 def handle_data(self,d):
  if self.inschema:self.schema+=d
 def handle_endtag(self,t):
  if t=='script' and self.inschema:self.schemas.append(json.loads(self.schema));self.inschema=False
titles=[]
for r in rows:
 s=(R/r['path']).read_text();p=Check();p.feed(s)
 assert p.h1==1 and p.canonical==[r['url']] and p.schemas
 assert 'noindex' not in s and 'ARQ-AUTORIDADE-20261030' in s
 assert all(q['url'] in p.hrefs for q in rows if q!=r)
 assert '<meta name="description"' in s
 titles.append(r['title'])
assert len(titles)==len(set(titles))==9
xml=ET.parse(R/'sitemap-autoridade-20261030.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
assert {e.text for e in xml.findall('s:url/s:loc',ns)}=={r['url'] for r in rows}
print('PASS: nine pages, unique titles, canonical, JSON-LD, navigation and sitemap')
