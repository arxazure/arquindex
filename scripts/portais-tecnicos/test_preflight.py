import importlib.util, pathlib, unittest, urllib.error, ssl, json, subprocess, os
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('publisher',pathlib.Path(__file__).with_name('publish.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class PreflightTests(unittest.TestCase):
 def env(self):return dict(CPANEL_HOST='https://cpanel.arquindex.com.br:2083',CPANEL_USER='test',CPANEL_API_TOKEN='secret',FTP_PASSWORD='different')
 def test_missing_each(self):
  for key in self.env():
   env=self.env();del env[key]
   with self.assertRaisesRegex(m.PreflightError,key):m.config(env)
 def test_no_ftp_fallback(self):
  with self.assertRaisesRegex(m.PreflightError,'CPANEL_API_TOKEN'):m.config({'FTP_PASSWORD':'secret'})
 def test_token_header(self):self.assertEqual(m.config(self.env())[2],'cpanel test:secret')
 def test_bad_endpoints(self):
  for host in ['http://cpanel.arquindex.com.br:2083','https://evil.test:2083','https://cpanel.arquindex.com.br:2083/?x=1','https://a:b@cpanel.arquindex.com.br:2083']:
   with self.assertRaises(m.PreflightError):m.config(dict(self.env(),CPANEL_HOST=host))
 def test_safe_errors(self):
  for status,code in [(401,'CPANEL_AUTH_REJECTED'),(403,'CPANEL_ACCESS_DENIED'),(500,'CPANEL_HTTP_ERROR')]:
   self.assertEqual(m.failure(urllib.error.HTTPError('https://secret',status,'secret',{},None)),code)
  self.assertEqual(m.failure(urllib.error.URLError(ssl.SSLError('secret'))),'COMMUNICATION_TLS')
  self.assertEqual(m.failure(TimeoutError('secret')),'COMMUNICATION_TIMEOUT')
  self.assertEqual(m.failure(urllib.error.URLError('secret')),'COMMUNICATION_NETWORK')
 def test_unapproved_pilot(self):
  with patch('sys.argv',['publish.py','--mode','pilot','--portal','conarq-guias']):
   with self.assertRaisesRegex(m.PreflightError,'APPROVAL'):m.options()
 def test_missing_config_no_network(self):
  with patch.dict(os.environ,{},clear=True),patch('sys.argv',['publish.py']),patch.object(m,'domains') as network:
   with self.assertRaises(SystemExit) as ex:m.main()
   self.assertEqual(ex.exception.code,1);network.assert_not_called()
