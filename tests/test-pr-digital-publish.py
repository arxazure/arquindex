import importlib.util
from pathlib import Path
from unittest.mock import patch
import unittest
spec=importlib.util.spec_from_file_location('publisher',Path('scripts/publish-pr-digital.py'))
publisher=importlib.util.module_from_spec(spec);spec.loader.exec_module(publisher)
class FakeFTP:
 def __init__(self,*args,**kwargs):self.sock=self;self.writes=0
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def getpeername(self):return ('192.0.2.1',21)
 def connect(self,*args):pass
 def auth(self):pass
 def login(self,*args):pass
 def prot_p(self):pass
 def cwd(self,*args):pass
 def mlsd(self,*args):return []
 def storbinary(self,*args):self.writes+=1;raise AssertionError('Must not write without full backup')
class PublishSafety(unittest.TestCase):
 def test_missing_backup_prevents_all_writes(self):
  ftp=FakeFTP()
  with patch.object(publisher.ftplib,'FTP_TLS',return_value=ftp),patch.object(publisher.socket,'gethostbyname_ex',return_value=('',[],['192.0.2.1'])),patch.dict(publisher.os.environ,{'FTP_PASSWORD':'dummy-test-only'}),patch.object(publisher,'get_public') as public:
   with self.assertRaisesRegex(RuntimeError,'no verified full backup'):publisher.main()
   public.assert_not_called()
   self.assertEqual(ftp.writes,0)
if __name__=='__main__':unittest.main()
