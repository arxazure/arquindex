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
 # Remove the old widget with correctly escaped regex patterns.
 # A previous version used r'<div\\\\b...', which matched a literal backslash,
 # leaving the old widget in place and causing the duplicate-widget exception.
 style_pattern=r'<style\\b[^>]*\\bid\\s*=\\s*["\\\']arq-floating-style["\\\'][^>]*>.*?</style\\s*>'
 script_pattern=r'<script\\b[^>]*\\bid\\s*=\\s*["\\\'](?:arq-floating-script|arq-dedup-floats)["\\\'][^>]*>.*?</script\\s*>'
 widget_pattern=r'<div\\b[^>]*\\bid\\s*=\\s*["\\\']arq-floating["\\\'][^>]*>.*?(?=<script\\b[^>]*\\bid\\s*=\\s*["\\\'](?:arq-floating-script|arq-dedup-floats)["\\\']|</body\\s*>)'
 html=re.sub(style_pattern,'',html,flags=re.I|re.S)
 html=re.sub(widget_pattern,'',html,flags=re.I|re.S)
 html=re.sub(script_pattern,'',html,flags=re.I|re.S)
 html=re.sub(r'</body\\s*>',lambda m:widget+'\\n'+m.group(),html,count=1,flags=re.I)
 style_count=len(re.findall(r'<style\\b[^>]*\\bid\\s*=\\s*["\\\']arq-floating-style["\\\']',html,re.I))
 widget_count=len(re.findall(r'<div\\b[^>]*\\bid\\s*=\\s*["\\\']arq-floating["\\\']',html,re.I))
 if style_count!=1 or widget_count!=1:
  raise RuntimeError(f'Widget duplicado ou sem CSS: {name} (CSS={style_count}, widgets={widget_count})')
 if html==original:print('UNCHANGED',name);continue
 backup=name+'.backup-arqui-'+str(int(time.time()))
 ftp.storbinary('STOR '+backup,io.BytesIO(data))
 ftp.storbinary('STOR '+name,io.BytesIO(html.encode('utf-8')))
 print('UPDATED',name,'BACKUP',backup)
ftp.quit()
