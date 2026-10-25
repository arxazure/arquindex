import os,ssl,ftplib,io,json
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=30) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p();f.cwd('/public_html')
 for folder in ['', 'gestao-documental/', 'geo-ai-search/']:
  result={'folder':folder or '/public_html'}
  try:
   result['entries']=[name.rsplit('/',1)[-1] for name in f.nlst(folder or '.')][:60]
  except ftplib.error_perm as e:result['list_status']=str(e)[:60]
  b=io.BytesIO()
  try:
   f.retrbinary('RETR '+folder+'.htaccess',b.write)
   lines=b.getvalue().decode('utf-8','replace').splitlines()
   result['htaccess_present']=True
   result['rewrite_directives']=sum(1 for line in lines if line.strip().lower().startswith(('rewriterule','rewritecond')))
   result['route_rules']=[line.split('#',1)[0][:250] for line in lines if line.strip().lower().startswith('rewriterule') and any(x in line for x in ['geo-ai','gestao-documental','index.php']) and not any(x in line.lower() for x in ['token','password','secret','key='])]
  except ftplib.error_perm as e:result['htaccess_status']=str(e)[:60]
  print('ROUTE_INVENTORY',json.dumps(result,ensure_ascii=False))
