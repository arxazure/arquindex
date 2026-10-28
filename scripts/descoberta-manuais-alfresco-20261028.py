"""One bounded submission: verify five published URLs; IndexNow and existing GSC OAuth."""
import datetime, hashlib, json, os, pathlib, re, urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

BASE='https://arquindex-capture-doc-ocr-scan.arquindex-capture.stream/'
PREFIX='manuais/alfresco/'
SLUGS=['','planejamento-implantacao-alfresco-community/','instalacao-alfresco-debian-docker-compose/','erros-alfresco-diagnostico-solucoes/','migracao-alfresco-windows-railway-validacao/']
URLS=[BASE+PREFIX+s for s in SLUGS]
REPORT={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':[], 'indexnow':{'attempted':False,'indexed':'not_claimed'},'google':{'submitted':False,'indexed':'not_claimed'}}
class Page(HTMLParser):
    def __init__(self,b):super().__init__();self.canonical=[];self.noindex=False;self.h1=0;self.feed(b.decode())
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='h1':self.h1+=1
        if t=='link' and d.get('rel')=='canonical':self.canonical.append(d.get('href'))
        if t=='meta' and d.get('name','').lower()=='robots' and 'noindex' in d.get('content','').lower():self.noindex=True
def request(url,data=None,headers=None,method=None):
    req=urllib.request.Request(url,data=data,headers={'User-Agent':'Arquindex-Manual-Discovery/1.0',**(headers or {})},method=method)
    with urllib.request.urlopen(req,timeout=45) as r:return r.status,r.url,r.headers,r.read()
def api_error(e):
    result={'type':type(e).__name__}
    if isinstance(e,urllib.error.HTTPError):
        result['http']=e.code
        try:
            obj=json.loads(e.read());error=obj.get('error',{})
            result['reason']=error if isinstance(error,str) else [x.get('reason') for x in error.get('errors',[])]
        except Exception:pass
    return result
def main():
    status,final,headers,raw=request(BASE+'sitemap.xml')
    ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    locs={x.text for x in ET.fromstring(raw).iter(ns+'loc')}
    assert set(URLS)<=locs and status==200 and final==BASE+'sitemap.xml'
    status,_,_,raw=request(BASE+'robots.txt')
    from urllib.robotparser import RobotFileParser
    robot=RobotFileParser();robot.parse(raw.decode().splitlines())
    for url in URLS:
        status,final,headers,body=request(url);page=Page(body)
        assert status==200 and final==url and page.canonical==[url] and page.h1==1
        assert not page.noindex and 'noindex' not in headers.get('X-Robots-Tag','').lower()
        assert robot.can_fetch('Googlebot',url) and robot.can_fetch('bingbot',url)
        REPORT['pages'].append({'url':url,'http':status,'canonical':page.canonical[0],'sha256':hashlib.sha256(body).hexdigest()})
    status,_,_,keybytes=request(BASE+'indexnow-key.txt');key=keybytes.decode().strip()
    assert status==200 and re.fullmatch('[A-Za-z0-9-]{8,128}',key)
    status,_,_,matching=request(BASE+key+'.txt');assert status==200 and matching.decode().strip()==key
    REPORT['indexnow']['key_file_verified']=True
    payload=json.dumps({'host':urllib.parse.urlsplit(BASE).hostname,'key':key,'keyLocation':BASE+'indexnow-key.txt','urlList':URLS}).encode()
    # Single write, no automatic retries after an uncertain response.
    REPORT['indexnow']['attempted']=True
    try:
        status,_,_,_=request('https://api.indexnow.org/indexnow',payload,{'Content-Type':'application/json'})
        REPORT['indexnow'].update({'http':status,'urls':URLS,'status':'submitted_key_validated' if status==200 else 'accepted_pending_key_validation' if status==202 else 'unexpected_response'})
    except Exception as e:REPORT['indexnow']['error']=api_error(e)
    creds={k:(os.environ.get('GSC_'+v) or os.environ.get('GOOGLE_'+v) or '').strip() for k,v in [('client_id','CLIENT_ID'),('client_secret','CLIENT_SECRET'),('refresh_token','REFRESH_TOKEN')]}
    if not all(creds.values()):
        REPORT['google']['blocked']='Existing GitHub OAuth secrets unavailable';return
    try:
        payload=urllib.parse.urlencode({**creds,'grant_type':'refresh_token'}).encode()
        _,_,_,b=request('https://oauth2.googleapis.com/token',payload)
        token=json.loads(b)['access_token'];auth={'Authorization':'Bearer '+token}
        _,_,_,b=request('https://www.googleapis.com/webmasters/v3/sites',headers=auth)
        host=urllib.parse.urlsplit(BASE).hostname
        domain_parts=host.split('.')
        domains={'sc-domain:'+'.'.join(domain_parts[i:]) for i in range(len(domain_parts)-1)}
        sites=[s for s in json.loads(b).get('siteEntry',[]) if s.get('permissionLevel') in ('siteOwner','siteFullUser') and (s['siteUrl'] in domains or BASE.startswith(s['siteUrl']))]
        if not sites:REPORT['google']['blocked']='No verified writable property covering the manual host';return
        site=max(sites,key=lambda x:len(x['siteUrl']))['siteUrl']
        endpoint='https://www.googleapis.com/webmasters/v3/sites/'+urllib.parse.quote(site,safe='')+'/sitemaps/'+urllib.parse.quote(BASE+'sitemap.xml',safe='')
        status,_,_,_=request(endpoint,b'',auth,method='PUT')
        REPORT['google'].update({'submitted':status in (200,204),'http':status,'property':site,'sitemap':BASE+'sitemap.xml'})
    except Exception as e:REPORT['google']['error']=api_error(e)
try:
    main()
except Exception as e:REPORT['verification_error']=api_error(e)
finally:
    out=pathlib.Path('publish-report');out.mkdir(exist_ok=True)
    (out/'descoberta-manuais-alfresco-20261028.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2))
    print(json.dumps(REPORT,ensure_ascii=False,indent=2),flush=True)
