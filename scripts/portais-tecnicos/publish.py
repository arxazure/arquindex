"""Scoped HomeHost provisioning and FTPS publication. Secrets never enter reports."""
import argparse,socket,urllib.error,ftplib,hashlib,io,json,os,pathlib,ssl,sys,time,urllib.parse,urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from build import DATA,OUT,ROOT,host,url
REPORT=ROOT/'publish-report/portais-tecnicos-20.json';REPORT.parent.mkdir(exist_ok=True)
report={'published':0,'planned':20,'indexed_confirmed':None,'results':[],'status':'preflight'}
class PreflightError(Exception):pass
def config(env):
 required=('CPANEL_HOST','CPANEL_USER','CPANEL_API_TOKEN','FTP_PASSWORD')
 missing=[k for k in required if not env.get(k,'').strip()]
 if missing:raise PreflightError('CONFIG_MISSING: '+','.join(missing))
 cp=env['CPANEL_HOST'].rstrip('/')
 try:
  p=urllib.parse.urlsplit(cp)
  valid=p.scheme=='https' and p.hostname in ('cpanel.arquindex.com.br','arquindex.com.br','ftp.arquindex.com.br','h59.servidorhh.com') and p.port==2083 and not (p.path or p.query or p.fragment or p.username or p.password)
 except ValueError:valid=False
 if not valid:raise PreflightError('CONFIG_INVALID_ENDPOINT')
 if any(c in env['CPANEL_USER']+env['CPANEL_API_TOKEN'] for c in '\r\n:'):raise PreflightError('CONFIG_INVALID_AUTH')
 return cp,env['CPANEL_USER'],'cpanel '+env['CPANEL_USER']+':'+env['CPANEL_API_TOKEN'],env['FTP_PASSWORD']
def failure(ex):
 if isinstance(ex,PreflightError):return str(ex)
 if isinstance(ex,urllib.error.HTTPError):
  return {401:'CPANEL_AUTH_REJECTED',403:'CPANEL_ACCESS_DENIED',429:'CPANEL_RATE_LIMITED'}.get(ex.code,'CPANEL_HTTP_ERROR')
 if isinstance(ex,ssl.SSLError):return 'COMMUNICATION_TLS'
 if isinstance(ex,(TimeoutError,socket.timeout)):return 'COMMUNICATION_TIMEOUT'
 if isinstance(ex,urllib.error.URLError):return failure(ex.reason) if isinstance(ex.reason,(ssl.SSLError,TimeoutError,socket.timeout,socket.gaierror)) else 'COMMUNICATION_NETWORK'
 if isinstance(ex,socket.gaierror):return 'COMMUNICATION_DNS'
 if isinstance(ex,json.JSONDecodeError):return 'CPANEL_INVALID_RESPONSE'
 if isinstance(ex,ftplib.error_perm):return 'FTPS_ACCESS_REJECTED'
 return 'VALIDATION_OR_OPERATION_FAILED'
def options():
 ap=argparse.ArgumentParser()
 ap.add_argument('--mode',choices=('preflight','pilot','verify'),default='preflight')
 ap.add_argument('--portal',choices=[t['slug'] for t in DATA['topics']])
 ap.add_argument('--approval',default='')
 args=ap.parse_args()
 if args.mode in ('pilot','verify') and (not args.portal or args.approval!='APPROVED:'+args.portal):raise PreflightError('PUBLICATION_APPROVAL_REQUIRED')
 return args
def save():REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
def api(path,params=None):
 endpoint=cp+path+('?' +urllib.parse.urlencode(params) if params else '')
 req=urllib.request.Request(endpoint,headers={'Authorization':auth,'Accept':'application/json'})
 # No redirects: credentials stay at the verified cPanel endpoint.
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args):return None
 with urllib.request.build_opener(NoRedirect).open(req,timeout=35) as r:return json.load(r)
def get(ftp,path):
 b=bytearray();ftp.retrbinary('RETR '+path,b.extend);return bytes(b)
def exists(ftp,path):
 try:return get(ftp,path)
 except ftplib.error_perm as ex:
  if str(ex).startswith('550'):return None
  raise
def ensure(ftp,path):
 for n in range(1,len(path.strip('/').split('/'))+1):
  p='/'+'/'.join(path.strip('/').split('/')[:n])
  try:ftp.cwd(p)
  except ftplib.error_perm:ftp.mkd(p)
def put(ftp,path,data):
 ensure(ftp,path.rsplit('/',1)[0]);ftp.storbinary('STOR '+path,io.BytesIO(data));assert get(ftp,path)==data,'FTPS_READBACK_FAILED'
def public(target):
 with urllib.request.urlopen(urllib.request.Request(target,headers={'User-Agent':'ArquindexPortalVerification/1.0','Cache-Control':'no-cache'}),timeout=25) as r:
  assert r.status==200 and r.url==target,'PUBLIC_REDIRECT_OR_STATUS'
  assert 'noindex' not in r.headers.get('X-Robots-Tag','').lower(),'HEADER_NOINDEX'
  return r.read()
def domains():
 j=api('/execute/DomainInfo/domains_data',{'format':'hash'})
 if j.get('status')!=1:raise PreflightError('CPANEL_API_OPERATION_REJECTED')
 data=j.get('data') or {};main=data.get('main_domain')
 assert isinstance(main,dict) and main.get('domain')=='arquindex.com.br','ACCOUNT_MISMATCH'
 sub=data.get('sub_domains') or {};addon=data.get('addon_domains') or {}
 result={}
 for records in (sub,addon):
  if isinstance(records,dict): records=records.values()
  for x in records:
   if isinstance(x,dict) and x.get('domain'):result[x['domain']]=x.get('documentroot')
 return result
def main():
 global cp,user,auth
 try:
  args=options()
  cp,user,auth,password=config(os.environ)
  selected=[t for t in DATA['topics'] if t['slug']==args.portal] if args.mode in ('pilot','verify') else DATA['topics']
  inventory=domains();report['cpanel_authenticated']=True;save()
  with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=50) as ftp:
   ftp.connect('h59.servidorhh.com',21);ftp.login(user,password);ftp.prot_p()
   home=get(ftp,'/public_html/index.html');assert b'arquindex' in home.lower(),'FTPS_ORIGIN_MISMATCH'
   if args.mode=='preflight':
    report['status']='preflight_passed';save();print(json.dumps(report));sys.exit(0)
   for t in selected:
    if not (OUT/host(t)/'media/guia.mp4').is_file():raise PreflightError('GENERATED_ARTIFACT_MISSING')
   if args.mode=='verify':
    for t in selected:
     root='public_html/portais-tecnicos/'+t['slug']
     if not inventory.get(host(t),'').endswith('/'+root):raise PreflightError('DOCUMENT_ROOT_MISMATCH')
     report['results'].append({'host':host(t),'url':url(t),'root':root,'state':'uploaded_noindex'})
   else:
    # Refuse all existing domains, even if their root appears compatible. This job creates new sites only.
    conflicts=[host(t) for t in selected if host(t) in inventory]
    assert not conflicts,'EXISTING_DOMAINS_REQUIRE_REVIEW: '+','.join(conflicts)
    for t in selected:
     root='/public_html/portais-tecnicos/'+t['slug']
     try:
      ftp.cwd(root);assert not ftp.nlst(),'DESTINATION_NOT_EMPTY: '+t['slug']
     except ftplib.error_perm as ex:
      if not str(ex).startswith('550'):raise
    report['status']='provisioning';save()
    for t in selected:
     fqdn=host(t);root='public_html/portais-tecnicos/'+t['slug'];r={'host':fqdn,'url':url(t),'root':root,'state':'pending'};report['results'].append(r);save()
     params={'cpanel_jsonapi_user':user,'cpanel_jsonapi_apiversion':2,'cpanel_jsonapi_module':'SubDomain','cpanel_jsonapi_func':'addsubdomain','domain':t['slug'],'rootdomain':'arquindex.com.br','dir':root,'disallowdot':1}
     result=api('/json-api/cpanel',params).get('cpanelresult') or {}
     assert result.get('event',{}).get('result')==1 and any(x.get('result')==1 for x in result.get('data') or []),'CPANEL_CREATE_FAILED: '+fqdn
     fresh=domains();actual=fresh.get(fqdn,'')
     assert actual.endswith('/'+root),'DOCUMENT_ROOT_MISMATCH: '+fqdn
     r['state']='domain_created';save()
     for f in sorted((OUT/fqdn).rglob('*')):
      if not f.is_file():continue
      rel=f.relative_to(OUT/fqdn).as_posix();data=f.read_bytes()
      if rel.endswith('.html'):data=data.replace(b'content="index,follow,max-image-preview:large"',b'content="noindex,follow,max-image-preview:large"')
      put(ftp,'/'+root+'/'+rel,data)
     r['state']='uploaded_noindex';save()
   try:report['autossl_requested']=False # Account-wide AutoSSL requires separate approval.
   except Exception as ex:report['autossl_error']=type(ex).__name__
   save()
   # Read public HTTPS before changing indexing policy. Pending DNS/TLS keeps noindex.
   for t,r in zip(selected,report['results']):
    try:
     for rel in ('index.html','manual/index.html'):
      target=url(t,'' if rel=='index.html' else 'manual/')
      expected=(OUT/host(t)/rel).read_bytes().replace(b'content="index,follow,max-image-preview:large"',b'content="noindex,follow,max-image-preview:large"')
      assert public(target)==expected,'PUBLIC_CONTENT_MISMATCH'
     for rel in [f.relative_to(OUT/host(t)).as_posix() for f in (OUT/host(t)).rglob('*') if f.is_file() and f.suffix!='.html']:
      assert public(url(t,rel))==(OUT/host(t)/rel).read_bytes(),'PUBLIC_ASSET_MISMATCH'
     assert get(ftp,'/public_html/index.html')==home,'INSTITUTIONAL_HOME_CHANGED'
     promoted=[]
     try:
      for rel in ('index.html','manual/index.html'):
       put(ftp,'/'+r['root']+'/'+rel,(OUT/host(t)/rel).read_bytes());promoted.append(rel)
      for rel in promoted:assert public(url(t,'' if rel=='index.html' else 'manual/'))==(OUT/host(t)/rel).read_bytes(),'INDEXABLE_PUBLIC_MISMATCH'
     except Exception:
      for rel in promoted:put(ftp,'/'+r['root']+'/'+rel,(OUT/host(t)/rel).read_bytes().replace(b'content="index,follow,max-image-preview:large"',b'content="noindex,follow,max-image-preview:large"'))
      raise
     r['state']='published_verified';r['sha256']=hashlib.sha256((OUT/host(t)/'index.html').read_bytes()).hexdigest();report['published']+=1
    except Exception as ex:r['state']='pending_dns_tls_or_public_qa';r['error']=failure(ex)
    save()
   assert get(ftp,'/public_html/index.html')==home,'INSTITUTIONAL_HOME_CHANGED'
   report['status']='complete' if report['published']==len(selected) else 'partial';save()
 except Exception as ex:
  report['status']='blocked';report['error']=failure(ex);save();print(json.dumps(report,ensure_ascii=False));sys.exit(1)
 print(json.dumps(report,ensure_ascii=False))
 if report['published']!=len(selected):sys.exit(1)
 

if __name__=='__main__':main()
