import os,ssl,ftplib,io,hashlib,json
from html.parser import HTMLParser
paths=['gestao-documental/sao-paulo/captura-documental-varejo-8/','gestao-documental/sao-paulo/digitalizacao-de-documentos-industria-4/','gestao-documental/lgpd/governanca-documental-dados-sensiveis-10/','gestao-documental/sao-paulo/compliance-documental-industria-9/','geo-ai-search/lgpd-financeiro-goiania-11/','geo-ai-search/digitalizacao-inteligente-juridico-rio-de-janeiro-25/']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.c=[];self.title=False;self.t='';self.text=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='link' and 'canonical' in d.get('rel','').lower():self.c.append(d.get('href'))
  if t=='title':self.title=True
 def handle_endtag(self,t):
  if t=='title':self.title=False
 def handle_data(self,d):
  if self.title:self.t+=d
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=30) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.cwd('/public_html')
 for path in paths:
  result={'url':'https://arquindex.com.br/'+path}
  for name in ['index.html','index.php']:
   b=io.BytesIO()
   try:f.retrbinary('RETR '+path+name,b.write)
   except ftplib.error_perm as e:
    result[name]=str(e)[:80];continue
   raw=b.getvalue();p=Page();p.feed(raw.decode('utf-8','replace'))
   result.update(file=path+name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),title=p.t,canonicals=p.c)
   break
  print('SOURCE_AUDIT',json.dumps(result,ensure_ascii=False))
