"""Complete HomeHost backup in resumable, fully read-back-verified archive parts.
Only writes /seo-backups; never deletes or modifies source files.
"""
import concurrent.futures as futures
from datetime import datetime, timezone, timedelta
import ftplib
import hashlib
import gzip
import io
import json
import os
from pathlib import Path
import posixpath
import socket
import ssl
import tarfile
import tempfile
import time

HOST='h59.servidorhh.com'
BASE='/seo-backups'
WORKERS=3
CHUNK_FILES=250
CHUNK_BYTES=64*1024*1024
MAX_FILES=200000
MAX_BYTES=8*1024*1024*1024
SYSTEM={'.cpanel','.trash','etc','logs','mail','tmp','ssl','public_ftp','seo-backups'}

def canonical(data):return json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(data):return hashlib.sha256(data).hexdigest()

def connect():
    expected=set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2])
    if not expected.intersection(socket.gethostbyname_ex(HOST)[2]):raise RuntimeError('HOST_IP_MISMATCH')
    ftp=ftplib.FTP_TLS(timeout=90,context=ssl.create_default_context());ftp.connect(HOST,21)
    if ftp.sock.getpeername()[0] not in expected:ftp.close();raise RuntimeError('PEER_IP_MISMATCH')
    ftp.auth();ftp.login('arquind2',os.environ['FTP_PASSWORD']);ftp.prot_p();ftp.cwd('/')
    return ftp

def mkdir(ftp,path):
    current=''
    for part in path.strip('/').split('/'):
        current+='/'+part
        try:ftp.mkd(current)
        except ftplib.error_perm:ftp.cwd(current)
    ftp.cwd('/')

def rows(ftp,path):
    result=[]
    for name,facts in ftp.mlsd(path,facts=['type','size','modify']):
        if name in ('.','..'):continue
        if '/' in name or '\\' in name or '\r' in name or '\n' in name:raise RuntimeError('UNSAFE_SOURCE_NAME')
        result.append((name,facts))
    return result

def read(ftp,path):
    out=io.BytesIO();ftp.retrbinary('RETR '+path,out.write);return out.getvalue()

def upload_verified(ftp,path,data):
    temporary=path+'.upload'
    ftp.storbinary('STOR '+temporary,io.BytesIO(data))
    digest=hashlib.sha256();ftp.retrbinary('RETR '+temporary,digest.update)
    if digest.hexdigest()!=sha(data):raise RuntimeError('REMOTE_HASH_MISMATCH '+path)
    ftp.rename(temporary,path)

def discover(ftp):
    top=rows(ftp,'/');dirs=[n for n,f in top if f.get('type')=='dir']
    roots=[]
    if 'public_html' in dirs:roots.append('public_html')
    for name in sorted(dirs):
        if name.startswith('.') or name in SYSTEM or name=='public_html':continue
        names={n.lower() for n,_ in rows(ftp,'/'+name)}
        if names.intersection({'index.html','index.php','robots.txt','sitemap.xml'}):roots.append(name)
    if not roots:raise RuntimeError('NO_PUBLIC_ROOT')
    return sorted(roots)

def inventory(ftp,roots):
    stack=['/'+p for p in roots];files=[];total=0;empty=[]
    while stack:
        path=stack.pop();listing=rows(ftp,path)
        if not listing:empty.append(path.lstrip('/'))
        for name,facts in listing:
            full=posixpath.join(path,name)
            if full.startswith('/public_html/seo-backups/') or full=='/public_html/seo-backups' or name.startswith('.upload-'):continue
            kind=facts.get('type')
            if kind=='dir':stack.append(full)
            elif kind=='file':
                size=int(facts.get('size','0'));total+=size
                files.append({'path':full.lstrip('/'),'bytes':size,'modify':facts.get('modify')})
                if len(files)>MAX_FILES or total>MAX_BYTES:raise RuntimeError('BACKUP_LIMIT_EXCEEDED')
            else:raise RuntimeError('UNSUPPORTED_ENTRY_TYPE '+full+' '+str(kind))
        if len(files)//1000!=(len(files)-len(listing))//1000:print('INVENTORY_PROGRESS',len(files),total,flush=True)
    return {'roots':roots,'files':sorted(files,key=lambda f:f['path']),'empty_directories':sorted(empty)}

def chunks(files):
    group=[];size=0
    for file in files:
        if group and (len(group)>=CHUNK_FILES or size+file['bytes']>CHUNK_BYTES):yield group;group=[];size=0
        group.append(file);size+=file['bytes']
    if group:yield group

def archive_part(entries,directory,number):
    # Each worker uses one dedicated connection for the whole part.
    def batch(items):
        output=[]
        with connect() as ftp:
            for entry in items:
                local=Path(directory)/sha(entry['path'].encode())
                with local.open('wb') as target:ftp.retrbinary('RETR /'+entry['path'],target.write,blocksize=256*1024)
                if local.stat().st_size!=entry['bytes']:raise RuntimeError('SOURCE_SIZE_CHANGED '+entry['path'])
                if entry.get('modify') and ftp.sendcmd('MDTM /'+entry['path'])[4:].strip()!=entry['modify']:raise RuntimeError('SOURCE_MODIFIED_DURING_BACKUP '+entry['path'])
                output.append((entry,local))
        return output
    downloaded=[]
    with futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for result in pool.map(batch,[entries[n::WORKERS] for n in range(WORKERS)]):downloaded.extend(result)
    archive=Path(directory)/('part-%05d.tar.gz'%number)
    with archive.open('wb') as raw, gzip.GzipFile(filename='',fileobj=raw,mode='wb',compresslevel=1,mtime=0) as compressed, tarfile.open(fileobj=compressed,mode='w|') as tar:
        for entry,local in sorted(downloaded,key=lambda row:row[0]['path']):
            info=tarfile.TarInfo(entry['path']);info.size=entry['bytes']
            info.mtime=int(datetime.strptime(entry['modify'].split('.')[0],'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc).timestamp()) if entry.get('modify') else 0
            with local.open('rb') as src:tar.addfile(info,src)
    # Read every decompressed member locally before uploading.
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers()
        if sorted((m.name,m.size) for m in members)!=sorted((f['path'],f['bytes']) for f in entries):raise RuntimeError('ARCHIVE_MEMBERS_MISMATCH')
        for member in members:
            stream=tar.extractfile(member)
            while stream.read(1024*1024):pass
    return archive

def main():
    started=time.monotonic();budget=int(os.environ.get('BACKUP_BUDGET_SECONDS','18000'))
    with connect() as ftp:
        mkdir(ftp,BASE)
        for name,facts in sorted(rows(ftp,BASE),reverse=True):
            if facts.get('type')!='file' or not name.startswith('weekly-inventory-') or not name.endswith('.json'):continue
            report=json.loads(read(ftp,BASE+'/'+name))
            try:age=datetime.now(timezone.utc)-datetime.strptime(report.get('run',''),'%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
            except ValueError:continue
            if timedelta(0)<=age<=timedelta(hours=48) and report.get('state')=='backup_verified_inventory_complete_cleanup_held' and 'public_html' in report.get('roots',[]) and report.get('backup',{}).get('verified_by_full_readback') is True:
                print('EXISTING_REPORT_FOR_PUBLISHER_VALIDATION',BASE+'/'+name,flush=True);return True
        # A partial session has immutable inventory, part files and independent completion receipts.
        sessions=sorted([n for n,f in rows(ftp,BASE) if f.get('type')=='dir' and n.startswith('parallel-full-')],reverse=True)
        session=None;inv=None
        for name in sessions[:3]:
            contents={n for n,_ in rows(ftp,BASE+'/'+name)}
            if 'inventory.json' in contents and 'complete.json' not in contents:
                session=BASE+'/'+name;inv=json.loads(read(ftp,session+'/inventory.json'));break
        if inv is None:
            stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');session=BASE+'/parallel-full-'+stamp
            roots=discover(ftp);print('BACKUP_ROOTS',json.dumps(roots),flush=True)
            inv=inventory(ftp,roots);inv['run']=stamp
            mkdir(ftp,session);upload_verified(ftp,session+'/inventory.json',canonical(inv))
        inv_hash=sha(canonical(inv));groups=list(chunks(inv['files']));completed=[]
        print('BACKUP_PLAN',json.dumps({'session':session,'files':len(inv['files']),'parts':len(groups),'bytes':sum(x['bytes'] for x in inv['files'])}),flush=True)
        names={n for n,f in rows(ftp,session) if f.get('type')=='file'}
        for number,group in enumerate(groups):
            filename='part-%05d.tar.gz'%number;receipt='part-%05d.json'%number
            if receipt in names:
                part=json.loads(read(ftp,session+'/'+receipt))
                if part.get('inventory_sha256')!=inv_hash or part.get('files')!=len(group):raise RuntimeError('CHECKPOINT_MISMATCH')
                digest=hashlib.sha256();ftp.retrbinary('RETR '+part['path'],digest.update)
                if digest.hexdigest()!=part['sha256']:raise RuntimeError('CHECKPOINT_HASH_MISMATCH')
                completed.append(part);continue
            if time.monotonic()-started>budget:
                print('BACKUP_CHECKPOINTED',json.dumps({'session':session,'parts_completed':len(completed),'parts_total':len(groups)}),flush=True)
                return False
            with tempfile.TemporaryDirectory(prefix='homehost-backup-') as local:
                archive=archive_part(group,local,number);data=archive.read_bytes();target=session+'/'+filename
                # Resume handles an uploaded archive without a completion receipt without deleting it.
                if filename in names:
                    digest=hashlib.sha256();ftp.retrbinary('RETR '+target,digest.update)
                    if digest.hexdigest()!=sha(data):raise RuntimeError('ORPHAN_PART_REQUIRES_REVIEW '+target)
                else:upload_verified(ftp,target,data)
                part={'path':target,'bytes':len(data),'sha256':sha(data),'files':len(group),'source_bytes':sum(x['bytes'] for x in group),'inventory_sha256':inv_hash}
                upload_verified(ftp,session+'/'+receipt,canonical(part));completed.append(part)
            print('BACKUP_PART_VERIFIED',json.dumps({'part':number+1,'total':len(groups),'files':sum(p['files'] for p in completed)}),flush=True)
        backup={'format':'tar.gz.parts.v1','parts':completed,'bytes':sum(p['bytes'] for p in completed),'sha256':sha(canonical(completed)),'outside_public_html':True,'verified_by_full_readback':True,'inventory_path':session+'/inventory.json','inventory_sha256':inv_hash}
        report={'run':datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'started_at':inv['run'],'state':'backup_verified_inventory_complete_cleanup_held','roots':inv['roots'],'files':len(inv['files']),'bytes':sum(x['bytes'] for x in inv['files']),'empty_directories':inv['empty_directories'],'backup':backup,'deleted':0,'moved':0}
        upload_verified(ftp,BASE+'/weekly-inventory-'+report['run']+'.json',canonical(report))
        upload_verified(ftp,session+'/complete.json',canonical(report))
        print('FULL_BACKUP_VERIFIED',json.dumps({'report':BASE+'/weekly-inventory-'+report['run']+'.json','files':report['files'],'parts':len(completed),'sha256':backup['sha256']}),flush=True)
        return True

if __name__=='__main__':
    if not main():raise SystemExit('Backup checkpointed but incomplete; publication remains blocked. Rerun to resume.')
