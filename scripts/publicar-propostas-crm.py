"""Publicação restrita ao chat e formulário comercial, com backup e readback FTPS."""
import os,io,ftplib,hashlib,time
from pathlib import Path
ftp=ftplib.FTP_TLS('ftp.arquindex.com.br',timeout=45)
ftp.login('arquind2',os.environ['FTP_PASSWORD']);ftp.prot_p()
root=None
for candidate in ['/public_html','/home/arquind2/public_html','/']:
    try:
        ftp.cwd(candidate)
        names=[n.rsplit('/',1)[-1] for n in ftp.nlst()]
        if 'index.html' in names or 'index.php' in names:root=ftp.pwd();break
    except ftplib.all_errors:pass
if root is None:raise RuntimeError('Raiz pública não encontrada')
backup=Path('backups-propostas');backup.mkdir(exist_ok=True)
for filename in ['solicitar-proposta-crm.html','solicitar-proposta-contratacao.html']:
    source=Path('conteudo/publicacao')/filename
    payload=source.read_bytes()
    if b'</html>' not in payload.lower():raise RuntimeError('HTML inválido')
    current=bytearray()
    try:ftp.retrbinary('RETR '+filename,current.extend)
    except ftplib.error_perm as e:
        if not str(e).startswith('550'):raise
    if current==payload:print('Sem alteração:',filename);continue
    if current:(backup/filename).write_bytes(current)
    ftp.storbinary('STOR '+filename,io.BytesIO(payload))
    verify=bytearray();ftp.retrbinary('RETR '+filename,verify.extend)
    if hashlib.sha256(verify).digest()!=hashlib.sha256(payload).digest():
        if current:ftp.storbinary('STOR '+filename,io.BytesIO(current))
        raise RuntimeError('Falha de integridade; conteúdo anterior restaurado: '+filename)
    print('Publicado e verificado:',filename)
ftp.quit()
