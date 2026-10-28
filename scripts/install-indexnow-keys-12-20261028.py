import ftplib,ssl,os,io,secrets,urllib.request,json
hosts=["quanto-custa-servico-dpo-externo-brasil","software-reconhecimento-texto-documentos-digitalizados","solucoes-digitalizacao-documentos-empresariais","cedoc","consultoria-decreto10278-solucao","digitalizacao-documental-curitiba-empresas-recomendadas-contrat","digitalizacao-documental-paulo-empresas-melhor-custo-beneficio","digitalizar-arquivos-solucao","ecm","servicos","arquivardocumento","arquivos-educacao"]
results=[]
with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
 f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
 for h in hosts:
  host=h+'.arquindex.com.br';root='/'+host;key=secrets.token_hex(16)
  try:
   f.cwd(root)
   data=io.BytesIO();f.retrbinary('RETR indexnow-key.txt',data.write);key=data.getvalue().decode().strip()
  except ftplib.error_perm:
   f.cwd(root);f.storbinary('STOR indexnow-key.txt',io.BytesIO(key.encode()))
  with urllib.request.urlopen('https://'+host+'/indexnow-key.txt',timeout=30) as r: assert r.status==200 and r.read().decode().strip()==key
  results.append({'host':host,'key_verified':True})
print(json.dumps(results))
