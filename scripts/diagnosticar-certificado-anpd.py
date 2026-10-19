import ftplib,ssl,socket,json
ctx=ssl.create_default_context()
ctx.check_hostname=False
with ftplib.FTP_TLS(context=ctx,timeout=20) as probe:
 probe.connect('ftp.arquindex.com.br',21)
 probe.auth()
 cert=probe.sock.getpeercert()
 print('FTPS_CERT_DIAGNOSTIC',json.dumps({'subject':cert.get('subject'),'SAN':cert.get('subjectAltName'),'issuer':cert.get('issuer'),'peer':probe.sock.getpeername(),'dns':socket.gethostbyname_ex('ftp.arquindex.com.br')},default=str),flush=True)
raise RuntimeError('READ_ONLY_DIAGNOSTIC_NO_CREDENTIALS_SENT')
