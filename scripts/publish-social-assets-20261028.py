import ftplib,ssl,os,io,json,re,pathlib,urllib.request,time
from datetime import datetime,timezone
items=json.loads(pathlib.Path('social/20261028/campaign.json').read_text())
brand=json.loads(pathlib.Path('campaign-build/brand.json').read_text())
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def read(f,p):
 b=io.BytesIO();f.retrbinary('RETR '+p,b.write);return b.getvalue()
def put(f,p,b): f.storbinary('STOR '+p,io.BytesIO(b));assert read(f,p)==b
def http(u):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(u,timeout=35) as r:return r.status,r.read()
  except Exception:
   if attempt==2:raise
   time.sleep(2)
report=[]
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
 for folder in ['/public_html/social','/public_html/social/20261028']:
  try:f.mkd(folder)
  except ftplib.error_perm:pass
 for x in items:
  record={'url':x['url'],'published':False};report.append(record)
  try:
   leaf='diagnostico.html' if x['i']==0 else 'custo.html' if x['host']=='ecm.arquindex.com.br' else 'index.html'
   path='/'+x['host']+'/'+leaf;old=read(f,path);text=old.decode()
   assert 'arquindex' in text.lower()
   manual='<section id="manual-tecnico-20261028" class="arq-tech-manual"><p>ROTEIRO TÉCNICO • ARQUINDEX</p><h2>'+x['title']+': etapas e critérios de aceite</h2><ol>'+''.join('<li>'+v+'</li>' for v in x['steps'])+'</ol><h3>Como preparar a solicitação</h3><p>Informe tipo de documento, volume aproximado, cidade e objetivo. Para Belo Horizonte, Contagem, Betim, Nova Lima e demais municípios da RMBH, coleta, execução no local e logística dependem de confirmação na proposta.</p><h3>Conferência da entrega</h3><p>Registre escopo, responsáveis, amostra validada, pendências e evidências de aceite. A digitalização ou aquisição de software, isoladamente, não assegura conformidade legal. Regras de retenção, acesso e tratamento dos originais exigem avaliação específica.</p><p><a href="https://www.arquindex.com.br/atendimento-rmbh/">Conheça o atendimento na RMBH</a> · <a href="https://wa.me/5531973632725">Solicite avaliação do projeto</a></p></section>'
   css='<style id="arq-brand-20261028">body{font-family:'+brand['font']+'}.arq-tech-manual,.arq-tech-manual h2,.arq-tech-manual h3{color:'+'#142d36'+'}a{color:'+brand['accent']+'}.arq-tech-manual{max-width:1120px;margin:48px auto;padding:clamp(20px,4vw,48px);border:1px solid #d6e5e3;border-top:8px solid '+brand['accent']+';border-radius:20px;background:#f4f8f8;line-height:1.8}.arq-tech-manual li{margin-bottom:14px}.arq-tech-manual a{overflow-wrap:anywhere}</style>'
   text=re.sub(r'<style id="arq-brand-20261028">.*?</style>', '', text, flags=re.S)
   text=text.replace('</head>',css+'</head>')
   if 'id="manual-tecnico-20261028"' not in text:text=text.replace('</body>',manual+'</body>')
   updated=text.encode();put(f,path+'.pre-campaign-'+stamp,old);put(f,path,updated)
   image=pathlib.Path('campaign-build/'+str(x['i'])+'.jpg').read_bytes();imagepath='/public_html/social/20261028/'+str(x['i'])+'.jpg';put(f,imagepath,image)
   record.update(published=True,image_url='https://www.arquindex.com.br/social/20261028/'+str(x['i'])+'.jpg',manual_url=x['url']+'#manual-tecnico-20261028')
   status,body=http(x['url']);assert status==200 and b'manual-tecnico-20261028' in body
   status,body=http(record['image_url']);assert status==200 and body[:2]==b'\xff\xd8'
   record['http_verified']=True
  except Exception as e:record['error']=str(e)
pathlib.Path('campaign-build/report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
if not all(x.get('http_verified') for x in report):raise SystemExit(1)
