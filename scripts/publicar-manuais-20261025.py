import os,ssl,ftplib,io,hashlib,urllib.request
from pathlib import Path
slugs=['digitalizacao-ocr-manual-tecnico-bh','guarda-fisica-custodia-manual-planos-bh']
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=40) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.cwd('/public_html')
 for slug in slugs:
  p=Path('prepared/servicos-20261025')/slug/'index.html'
  data=p.read_text().replace('<meta name="robots" content="noindex,follow">','<meta name="robots" content="index,follow">').encode()
  try:f.mkd(slug)
  except ftplib.error_perm:pass
  target=slug+'/index.html'
  old=io.BytesIO()
  try:f.retrbinary('RETR '+target,old.write)
  except ftplib.error_perm as e:
   if not str(e).startswith('550'):raise
  if old.getvalue() and old.getvalue()!=data:raise RuntimeError('Existing distinct page: '+target)
  f.storbinary('STOR '+target,io.BytesIO(data));result=io.BytesIO();f.retrbinary('RETR '+target,result.write)
  assert result.getvalue()==data
  print('FTPS_VERIFIED',slug,hashlib.sha256(data).hexdigest())
for slug in slugs:
 url='https://www.arquindex.com.br/'+slug+'/'
 with urllib.request.urlopen(url,timeout=30) as r:
  body=r.read();assert r.status==200 and b'noindex' not in body
  print('PUBLIC_HTTP200',url)
