"""Offline end-to-end backup/restore evidence and publication gate regressions."""
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ftplib


def module(name,path):
 spec=importlib.util.spec_from_file_location(name,Path(path));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
backup=module('backup','scripts/backup-homehost-resumable.py')
publisher=module('publisher','scripts/publish-pr-digital.py')

class MemoryFTP:
 def __init__(self):
  self.files={'/public_html/index.html':b'original home','/public_html/a.txt':b'preserve me'}
  self.dirs={'/','/public_html'};self.source_writes=0;self.copies=0
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def cwd(self,path):
  if path not in self.dirs:raise ftplib.error_perm('550 missing directory')
 def mkd(self,path):
  if path in self.dirs:raise ftplib.error_perm('550 exists')
  self.dirs.add(path)
 def mlsd(self,path,facts=None):
  if path not in self.dirs:raise ftplib.error_perm('550 missing directory')
  prefix=path.rstrip('/')+'/'
  rows=[]
  for directory in sorted(self.dirs):
   if directory.startswith(prefix) and directory!=path and '/' not in directory[len(prefix):]:rows.append((directory[len(prefix):],{'type':'dir'}))
  for filename,data in sorted(self.files.items()):
   if filename.startswith(prefix) and '/' not in filename[len(prefix):]:rows.append((filename[len(prefix):],{'type':'file','size':str(len(data)),'modify':'20261025000000'}))
  return rows
 def retrbinary(self,command,callback,blocksize=8192):
  path=command[5:]
  if path not in self.files:raise ftplib.error_perm('550 missing file')
  if path.startswith('/public_html/'):self.copies+=1
  callback(self.files[path])
 def storbinary(self,command,source):
  path=command[5:]
  if path.startswith('/public_html/'):self.source_writes+=1
  self.files[path]=source.read()
 def rename(self,old,new):
  if new in self.files:raise ftplib.error_perm('550 exists')
  self.files[new]=self.files.pop(old)
 def size(self,path):return len(self.files[path])
 def sendcmd(self,command):return '213 20261025000000'

class BackupTests(unittest.TestCase):
 def test_chunk_count_and_size_boundaries(self):
  files=[{'path':str(i),'bytes':1} for i in range(501)]
  self.assertEqual([len(p) for p in backup.chunks(files)],[250,250,1])
  files=[{'path':'a','bytes':backup.CHUNK_BYTES},{'path':'b','bytes':1}]
  self.assertEqual([len(p) for p in backup.chunks(files)],[1,1])
 def test_archives_are_reproducible_and_restore_all_bytes(self):
  ftp=MemoryFTP();entries=[{'path':p.lstrip('/'),'bytes':len(data),'modify':'20261025000000'} for p,data in ftp.files.items()]
  import tarfile
  with patch.object(backup,'connect',return_value=ftp),tempfile.TemporaryDirectory() as first,tempfile.TemporaryDirectory() as second:
   a=backup.archive_part(entries,first,0);b=backup.archive_part(entries,second,0)
   self.assertEqual(a.read_bytes(),b.read_bytes())
   with tarfile.open(a,'r:gz') as tar:
    self.assertEqual({m.name:tar.extractfile(m).read() for m in tar.getmembers()},{p.lstrip('/'):data for p,data in ftp.files.items()})
 def test_complete_backup_and_publisher_acceptance(self):
  ftp=MemoryFTP();original=dict(ftp.files)
  with patch.object(backup,'connect',return_value=ftp),patch.dict(backup.os.environ,{'BACKUP_BUDGET_SECONDS':'300'}):self.assertTrue(backup.main())
  self.assertEqual(ftp.source_writes,0)
  for path,data in original.items():self.assertEqual(ftp.files[path],data)
  reports=[p for p in ftp.files if p.startswith('/seo-backups/weekly-inventory-')]
  self.assertEqual(len(reports),1)
  report=json.loads(ftp.files[reports[0]]);self.assertEqual(report['files'],2)
  with patch.object(publisher.ftplib,'FTP_TLS',return_value=ftp),patch.object(publisher.socket,'gethostbyname_ex',return_value=('',[],['192.0.2.1'])),patch.dict(publisher.os.environ,{'FTP_PASSWORD':'test-only'}),patch.object(publisher,'get_public',side_effect=lambda path:ftp.files['/public_html'+path+('index.html' if path.endswith('/') else '')] if path.startswith('/pr-digital/') else b'ok'):
   ftp.connect=lambda *a:None;ftp.auth=lambda:None;ftp.login=lambda *a:None;ftp.prot_p=lambda:None;ftp.sock=type('Socket',(),{'getpeername':lambda self:('192.0.2.1',21)})()
   publisher.main()
  self.assertGreater(ftp.source_writes,0)
 def test_checkpoint_resume_skips_downloaded_source(self):
  ftp=MemoryFTP()
  with patch.object(backup,'connect',return_value=ftp),patch.dict(backup.os.environ,{'BACKUP_BUDGET_SECONDS':'300'}):backup.main()
  for p in list(ftp.files):
   if p.endswith('/complete.json') or p.startswith('/seo-backups/weekly-inventory-'):del ftp.files[p]
  before=ftp.copies
  with patch.object(backup,'connect',return_value=ftp),patch.dict(backup.os.environ,{'BACKUP_BUDGET_SECONDS':'300'}):self.assertTrue(backup.main())
  self.assertEqual(ftp.copies,before)
 def test_corrupt_remote_upload_never_gets_receipt(self):
  ftp=MemoryFTP()
  original=ftp.storbinary
  def corrupt(command,source):original(command,source);ftp.files[command[5:]]+=b'corrupt'
  ftp.storbinary=corrupt
  with self.assertRaisesRegex(RuntimeError,'REMOTE_HASH_MISMATCH'):backup.upload_verified(ftp,'/seo-backups/test',b'content')
  self.assertNotIn('/seo-backups/test',ftp.files)
if __name__=='__main__':unittest.main()
