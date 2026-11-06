"""Checks authored pages, canonical, structured data, internal targets and real media."""
import hashlib,json,pathlib,re,subprocess,sys
from html.parser import HTMLParser
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from build import DATA,OUT,host,url
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.canonical=[];self.ld=[];self.inld=False;self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if tag in ('a','source','track','link'):
   for k in ('href','src'):
    if k in a:self.links.append(a[k])
  if tag=='script' and a.get('type')=='application/ld+json':self.inld=True
 def handle_endtag(self,tag):
  if tag=='script':self.inld=False
 def handle_data(self,data):
  if self.inld:self.ld.append(data)
  else:self.text.append(data)
report=[];answers=set()
for t in DATA['topics']:
 d=OUT/host(t);assert t['answer'] not in answers;answers.add(t['answer'])
 for rel in ('index.html','manual/index.html'):
  f=d/rel;s=f.read_text();p=Page();p.feed(s)
  assert p.h1==1 and p.canonical==[url(t,'' if rel=='index.html' else 'manual/')],f
  j=json.loads(''.join(p.ld));assert j['@context']=='https://schema.org'
  if rel=='index.html':
   faq=next(x for x in j['@graph'] if x['@type']=='FAQPage');assert len(faq['mainEntity'])==len(t['faq'])
   assert all(q in s and a in s for q,a in t['faq'])
  assert len(re.findall(r'\w+',' '.join(p.text)))>650,(f,'insufficient detail')
  for target in p.links:
   if target.startswith('/') and not target.startswith('//'):
    file=d/target.split('#')[0].lstrip('/')
    if file.is_dir():file=file/'index.html'
    assert file.exists(),(f,target)
  report.append({'file':str(f.relative_to(OUT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'words':len(re.findall(r'\w+',' '.join(p.text)))})
 for name in ('guia.mp4','poster.jpg','legendas.vtt'):assert (d/'media'/name).stat().st_size>0
 result=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(d/'media/guia.mp4')]))
 assert 23.9<=float(result['format']['duration'])<=24.1
 assert (d/'robots.txt').read_text().endswith(url(t,'sitemap.xml')+'\n')
path=OUT.parent/'qa-report.json';path.write_text(json.dumps({'passed':True,'portals':20,'pages':40,'videos':20,'files':report},ensure_ascii=False,indent=2))
print('QA_OK: 20 portals, 40 pages, 20 MP4 videos; canonical, FAQ, assets and duration verified')
