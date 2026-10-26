"""Publish only pr-digital after validating a recent full HomeHost backup.
No DNS changes, indexation requests or deletion of pre-existing files.
"""
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import posixpath
import socket
import ssl
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validator',ROOT/'scripts/validate-pr-digital.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)

def get_public(path):
    with urlopen(Request(qa.BASE+path,headers={'User-Agent':'Arquindex-PR-Digital-QA/1.0'}),timeout=30) as response:
        if response.status != 200: raise RuntimeError('HTTP_NOT_200 '+path)
        if response.url != qa.BASE+path: raise RuntimeError('UNEXPECTED_REDIRECT '+path)
        return response.read()

def read_json(ftp,path):
    buffer=io.BytesIO();ftp.retrbinary('RETR '+path,buffer.write)
    if buffer.tell()>20*1024*1024: raise RuntimeError('REPORT_TOO_LARGE')
    return json.loads(buffer.getvalue())

def main():
    errors=qa.validate()
    if errors: raise RuntimeError('\n'.join(errors))
    password=os.environ.get('FTP_PASSWORD')
    if not password: raise RuntimeError('FTP_PASSWORD_MISSING')
    host='h59.servidorhh.com'; expected=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2])
    if not expected.intersection(socket.gethostbyname_ex(host)[2]): raise RuntimeError('HOST_IP_MISMATCH')
    with ftplib.FTP_TLS(timeout=60,context=ssl.create_default_context()) as ftp:
        ftp.connect(host,21)
        if ftp.sock.getpeername()[0] not in expected: raise RuntimeError('PEER_IP_MISMATCH')
        ftp.auth();ftp.login('arquind2',password);ftp.prot_p();ftp.cwd('/')
        try:
            reports=sorted([n for n,f in ftp.mlsd('/seo-backups') if n.startswith('weekly-inventory-') and n.endswith('.json') and f.get('type')=='file'],reverse=True)
        except ftplib.error_perm as exc: raise RuntimeError('BLOCKED: full backup report unavailable; zero production writes') from exc
        backup=None
        for name in reports[:10]:
            report=read_json(ftp,'/seo-backups/'+name)
            candidate=report.get('backup',{})
            try: created=datetime.strptime(report.get('run',''),'%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
            except ValueError: continue
            if not timedelta(0)<=datetime.now(timezone.utc)-created<=timedelta(hours=48): continue
            if report.get('state')!='backup_verified_inventory_complete_cleanup_held': continue
            if 'public_html' not in report.get('roots',[]): continue
            if candidate.get('outside_public_html') is not True or candidate.get('verified_by_full_readback') is not True: continue
            if candidate.get('format')=='tar.gz.parts.v1':
                parts=candidate.get('parts',[])
                encoded=json.dumps(parts,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
                if not parts or hashlib.sha256(encoded).hexdigest()!=candidate.get('sha256'):raise RuntimeError('PART_MANIFEST_HASH_MISMATCH')
                if sum(p.get('files',0) for p in parts)!=report.get('files'):raise RuntimeError('PART_FILE_COUNT_MISMATCH')
                if sum(p.get('source_bytes',0) for p in parts)!=report.get('bytes'):raise RuntimeError('PART_SOURCE_BYTES_MISMATCH')
                if sum(p.get('bytes',0) for p in parts)!=candidate.get('bytes'):raise RuntimeError('PART_BYTES_MISMATCH')
                inventory_path=candidate.get('inventory_path','')
                if not inventory_path.startswith('/seo-backups/parallel-full-') or '..' in inventory_path or not inventory_path.endswith('/inventory.json'):raise RuntimeError('INVALID_INVENTORY_PATH')
                inventory=io.BytesIO();ftp.retrbinary('RETR '+inventory_path,inventory.write)
                if hashlib.sha256(inventory.getvalue()).hexdigest()!=candidate.get('inventory_sha256'):raise RuntimeError('INVENTORY_HASH_MISMATCH')
                manifest=json.loads(inventory.getvalue())
                if len(manifest.get('files',[]))!=report.get('files') or manifest.get('roots')!=report.get('roots'):raise RuntimeError('INVENTORY_COUNT_ROOTS_MISMATCH')
                seen=set()
                for part in parts:
                    path=part.get('path','')
                    if path in seen or not path.startswith(posixpath.dirname(inventory_path)+'/part-') or '..' in path or not path.endswith('.tar.gz'):raise RuntimeError('INVALID_BACKUP_PART_PATH')
                    seen.add(path)
                    if part.get('inventory_sha256')!=candidate.get('inventory_sha256'):raise RuntimeError('PART_INVENTORY_MISMATCH')
                    if ftp.size(path)!=part.get('bytes'):raise RuntimeError('BACKUP_PART_SIZE_MISMATCH')
                    digest=hashlib.sha256();ftp.retrbinary('RETR '+path,digest.update)
                    if digest.hexdigest()!=part.get('sha256'):raise RuntimeError('BACKUP_PART_HASH_MISMATCH')
            else:
                path=candidate.get('path','')
                if not path.startswith('/seo-backups/weekly-full-') or '..' in path or not path.endswith('.tar.gz'):continue
                if ftp.size(path)!=candidate.get('bytes'):continue
                digest=hashlib.sha256();ftp.retrbinary('RETR '+path,digest.update)
                if digest.hexdigest()!=candidate.get('sha256'):raise RuntimeError('BACKUP_HASH_MISMATCH')
            backup=candidate;break
        if not backup: raise RuntimeError('BLOCKED: no verified full backup within 48 hours; zero production writes')
        print('BACKUP_VERIFIED',json.dumps({k:v for k,v in backup.items() if k!='parts'}),flush=True)
        # Required public dependencies must be healthy before any write.
        get_public('/');get_public('/guias-digitalizacao/')
        ftp.cwd('/public_html')
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        changed=[]
        try:
            for source in sorted((ROOT/'pr-digital').rglob('*')):
                if not source.is_file() or source.suffix not in ('.html','.xml'): continue
                relative=source.relative_to(ROOT).as_posix()
                target='/public_html/'+relative
                parent=posixpath.dirname(target)
                current=''
                for part in parent.strip('/').split('/'):
                    current+='/'+part
                    try: ftp.mkd(current)
                    except ftplib.error_perm:
                        ftp.cwd(current)  # Verify existing directory instead of masking permission failures.
                ftp.cwd('/')
                data=source.read_bytes();temporary=target+'.upload-'+stamp
                old=None
                # A directory listing distinguishes absence from a failed RETR.
                names={n for n,f in ftp.mlsd(parent) if f.get('type')=='file'}
                if posixpath.basename(target) in names:
                    original=io.BytesIO();ftp.retrbinary('RETR '+target,original.write)
                    if original.getvalue()==data: continue
                    old=target+'.rollback-'+stamp
                ftp.storbinary('STOR '+temporary,io.BytesIO(data))
                digest=hashlib.sha256();ftp.retrbinary('RETR '+temporary,digest.update)
                if digest.hexdigest()!=hashlib.sha256(data).hexdigest(): raise RuntimeError('UPLOAD_HASH_MISMATCH '+relative)
                if old: ftp.rename(target,old)
                changed.append((target,old))
                ftp.rename(temporary,target)
            for slug in qa.SLUGS:
                path='/pr-digital/'+slug
                page=qa.Page();page.feed(get_public(path).decode('utf-8'))
                if page.canonicals!=[qa.BASE+path]: raise RuntimeError('PUBLIC_CANONICAL_MISMATCH '+path)
                if len(page.h1)!=1: raise RuntimeError('PUBLIC_CONTENT_MISMATCH '+path)
                if slug in qa.ARTICLES and (len(page.schemas)!=1 or page.schemas[0].get('mainEntityOfPage')!=qa.BASE+path): raise RuntimeError('PUBLIC_JSONLD_MISMATCH '+path)
            if get_public('/pr-digital/sitemap.xml')!=(ROOT/'pr-digital/sitemap.xml').read_bytes(): raise RuntimeError('PUBLIC_SITEMAP_MISMATCH')
            print('PUBLISHED_AND_PUBLICLY_VALIDATED',json.dumps({'urls':sorted(qa.URLS),'changed_files':len(changed),'backup_sha256':backup['sha256'],'dns_changed':False,'indexation_submitted':False}),flush=True)
        except Exception:
            rollback_errors=[]
            for target,old in reversed(changed):
                try:
                    # Preserve the failed candidate as well as the pre-existing file.
                    try: ftp.rename(target,target+'.failed-'+stamp)
                    except ftplib.error_perm:
                        if not old: raise
                    if old: ftp.rename(old,target)
                except Exception as exc: rollback_errors.append((target,str(exc)))
            if rollback_errors: print('ROLLBACK_REQUIRES_REVIEW',json.dumps(rollback_errors),flush=True)
            raise

if __name__=='__main__': main()
