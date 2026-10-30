"""Submit only HTTP-verified pages; credentials stay in runner memory."""
from pathlib import Path
import json,os,urllib.request,urllib.parse,urllib.error,urllib.robotparser
P=Path('publish-report/autoridade-20261030');r=json.loads((P/'publication.json').read_text());assert r.get('http_verified') and r.get('sitemap_verified') and r.get('key_file_verified')
urls=r['pages'];rp=urllib.robotparser.RobotFileParser();rp.parse((P/'robots.txt').read_text().splitlines());assert all(rp.can_fetch(a,u) for a in ['Googlebot','bingbot'] for u in urls),'ROBOTS_BLOCKED'
key=json.loads((P/'indexnow-public-key.json').read_text());r['discovery']={}
def request(url,data=None,headers=None,method=None):
 with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers or {},method=method),timeout=40) as x:return x.status,x.read()
try:
 payload=json.dumps({'host':'www.arquindex.com.br','key':key['key'],'keyLocation':key['url'],'urlList':urls}).encode()
 status,_=request('https://api.indexnow.org/indexnow',payload,{'Content-Type':'application/json'},'POST')
 r['discovery']['bing_indexnow']={'http':status,'submitted':status in (200,202),'url_count':len(urls),'key_file_verified':True,'indexed':False,'pending_key_validation':status==202};print('INDEXNOW_ENDPOINT_RESPONSE',status,len(urls),'INDEXING_NOT_CONFIRMED',flush=True)
except Exception as e:r['discovery']['bing_indexnow']={'submitted':False,'error':type(e).__name__};print('INDEXNOW_NOT_SUBMITTED',type(e).__name__,flush=True)
credentials={name:(os.environ.get('GSC_'+suffix) or os.environ.get('GOOGLE_'+suffix) or '') for name,suffix in [('client_id','CLIENT_ID'),('client_secret','CLIENT_SECRET'),('refresh_token','REFRESH_TOKEN')]}
if not all(credentials.values()):
 r['discovery']['google']={'submitted':False,'reason':'OAuth configuration missing','indexed':False};print('GOOGLE_NOT_SUBMITTED_OAUTH_CONFIGURATION_MISSING',flush=True)
else:
 try:
  _,raw=request('https://oauth2.googleapis.com/token',urllib.parse.urlencode({**credentials,'grant_type':'refresh_token'}).encode());token=json.loads(raw)['access_token'];headers={'Authorization':'Bearer '+token}
  _,raw=request('https://www.googleapis.com/webmasters/v3/sites',headers=headers)
  allowed=[x for x in json.loads(raw).get('siteEntry',[]) if x['siteUrl'] in ('sc-domain:arquindex.com.br','https://www.arquindex.com.br/') and x.get('permissionLevel') in ('siteOwner','siteFullUser')];assert allowed,'WRITABLE_PROPERTY_NOT_FOUND'
  site=next((x['siteUrl'] for x in allowed if x['siteUrl'].startswith('sc-domain:')),allowed[0]['siteUrl']);sitemap='https://www.arquindex.com.br/sitemap-autoridade-20261030.xml'
  endpoint='https://www.googleapis.com/webmasters/v3/sites/'+urllib.parse.quote(site,safe='')+'/sitemaps/'+urllib.parse.quote(sitemap,safe='')
  status,_=request(endpoint,data=b'',headers=headers,method='PUT');r['discovery']['google']={'submitted':status in (200,204),'http':status,'sitemap':sitemap,'indexed':False};print('GOOGLE_SITEMAP_ENDPOINT_RESPONSE',status,'INDEXING_NOT_CONFIRMED',flush=True)
 except Exception as e:r['discovery']['google']={'submitted':False,'error':type(e).__name__,'indexed':False};print('GOOGLE_SUBMISSION_FAILED',type(e).__name__,flush=True)
(P/'publication.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
