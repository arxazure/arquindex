import os,ftplib,io,re,time
from pathlib import Path
password=os.environ['FTP_PASSWORD']
widget=Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')
ftp=ftplib.FTP_TLS('ftp.arquindex.com.br',timeout=35)
ftp.login('arquind2',password);ftp.prot_p()
root=None
for p in ['/public_html','/home/arquind2/public_html','/']:
 try:
  ftp.cwd(p)
  names=[x.rsplit('/',1)[-1] for x in ftp.nlst()]
  if 'index.html' in names or 'index.php' in names:root=ftp.pwd();break
 except ftplib.all_errors:continue
if not root:raise RuntimeError('Raiz pública não encontrada')
print('ROOT',root)
names=[x.rsplit('/',1)[-1] for x in ftp.nlst()]
targets=['index.html','index.php','solicitar-proposta-contratacao.html','alfresco-ecm-automacao-documental-ia.html','gestao-documental-software-ged-processos-ia.html','como-automatizar-a-gestao-documental-processos-ia.html']
for name in targets:
 if name not in names:continue
 data=bytearray();ftp.retrbinary('RETR '+name,data.extend)
 try:html=data.decode('utf-8')
 except UnicodeDecodeError:print('SKIP_ENCODING',name);continue
 if '</body>' not in html.lower():print('SKIP_NO_BODY',name);continue
 original=html
 # Replace the entire legacy widget, including its missing stylesheet.
 # This prevents old markup from surviving without CSS on the live homepage.
 html=re.sub(r'<style\\b[^>]*id=["\\\']arq-floating-style["\\\'][^>]*>.*?</style>','',html,flags=re.I|re.S)
 html=re.sub(r'<script\\b[^>]*id=["\\\'](?:arq-floating-script|arq-dedup-floats)["\\\'][^>]*>.*?</script>','',html,flags=re.I|re.S)
 html=re.sub(r'<div\\b[^>]*id=["\\\']arq-floating["\\\'][^>]*>.*?(?=<script\\b|</body>)','',html,flags=re.I|re.S)
 html=re.sub(r'</body>',lambda m:widget+'\\n'+m.group(),html,count=1,flags=re.I)
 if html.count('id="arq-floating-style"')!=1 or html.count('id="arq-floating"')!=1:
  raise RuntimeError('Widget duplicado ou sem CSS: '+name)
 if html==original:print('UNCHANGED',name);continue
 backup=name+'.backup-arqui-'+str(int(time.time()))
 ftp.storbinary('STOR '+backup,io.BytesIO(data))
 ftp.storbinary('STOR '+name,io.BytesIO(html.encode('utf-8')))
 print('UPDATED',name,'BACKUP',backup)
ftp.quit()
