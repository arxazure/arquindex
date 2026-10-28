import ftplib,ssl,os,io,re,json,hashlib,urllib.request
from datetime import datetime,timezone
HOSTS=["quanto-custa-servico-dpo-externo-brasil","software-reconhecimento-texto-documentos-digitalizados","solucoes-digitalizacao-documentos-empresariais","cedoc","consultoria-decreto10278-solucao","digitalizacao-documental-curitiba-empresas-recomendadas-contrat","digitalizacao-documental-paulo-empresas-melhor-custo-beneficio","digitalizar-arquivos-solucao","ecm","servicos","arquivardocumento","arquivos-educacao"]
report=[]
def get(f,p):
 b=io.BytesIO();f.retrbinary('RETR '+p,b.write);return b.getvalue()
def put(f,p,b): f.storbinary('STOR '+p,io.BytesIO(b))
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
css='<style id="arq-responsive-repair-20261028">*,*:before,*:after{box-sizing:border-box}img,video,iframe,canvas,svg{max-width:100%}main,section,article,header,footer,nav,.container{min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere}table{display:block;max-width:100%;overflow-x:auto}@media(max-width:600px){body{min-width:0!important}body>*{max-width:100%}main,section,article,.container{max-width:100%!important;overflow-wrap:anywhere}#arq-floating,.aq-brand-wa,#wa-widget-send-button{max-width:calc(100vw - 24px)!important}input,textarea,select{max-width:100%}}</style>'
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
 for h in HOSTS:
  host=h+'.arquindex.com.br';leaf='diagnostico.html' if h==HOSTS[0] else 'custo.html' if h=='ecm' else 'index.html'
  url='https://'+host+'/'+('' if leaf=='index.html' else leaf)
  item={'url':url,'published':False};report.append(item)
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'ArquindexRepair/1.0'})
   with urllib.request.urlopen(req,timeout=40) as r: original=r.read();assert r.status==200 and r.url==url
   target=None
   for root in ['/public_html/'+host,'/'+host,'/public_html/'+h,'/'+h]:
    try:
     data=get(f,root+'/'+leaf)
     if data==original: target=root+'/'+leaf;break
    except ftplib.error_perm: pass
   if not target: raise RuntimeError('SOURCE_MAPPING_NOT_CONFIRMED')
   text=original.decode('utf-8')
   text=re.sub(r'<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>', '<link rel="canonical" href="'+url+'">',text,flags=re.I)
   def title(m):
    value=re.sub(r'(?:\s*\|\s*Arquindex)+\s*$',' | Arquindex',m.group(1),flags=re.I)
    return '<title>'+value+'</title>'
   text=re.sub(r'<title>(.*?)</title>',title,text,flags=re.I|re.S)
   if 'arq-responsive-repair-20261028' not in text: text=text.replace('</head>',css+'</head>')
   updated=text.encode()
   assert updated!=original or 'arq-responsive-repair-20261028' in text
   backup=target+'.pre-repair-'+stamp
   put(f,backup,original);assert get(f,backup)==original
   put(f,target,updated)
   if get(f,target)!=updated:
    put(f,target,original);raise RuntimeError('READBACK_FAILED_ROLLED_BACK')
   item.update(published=True,target=target,sha256=hashlib.sha256(updated).hexdigest())
   with urllib.request.urlopen(req,timeout=40) as r: public=r.read()
   item['http_verified']=public==updated
  except Exception as e: item['error']=type(e).__name__+': '+str(e)
os.makedirs('repair-report',exist_ok=True)
open('repair-report/result.json','w').write(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
if not all(x.get('http_verified') for x in report): raise SystemExit(1)
