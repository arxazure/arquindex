"""Read-only recovery inventory: public DNS/HTTP metadata, never HTML exports."""
import concurrent.futures, hashlib, http.client, ipaddress, json, os, re, socket, ssl, time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import dns.message, dns.query, dns.rdatatype, dns.flags

# Scope comes exclusively from files already public in this repository.
# No Search Console data or manifest is consumed or exported.
pat=re.compile(r'https?://((?:[a-z0-9-]+\.)*arquindex\.com\.br)(?:[/:"\s<]|$)',re.I)
public_hosts=set()
for p in Path('.').rglob('*'):
    if not p.is_file() or '.git' in p.parts or 'tests' in p.parts or p.stat().st_size>5000000 or p.suffix not in {'.csv','.json','.html','.xml','.md','.txt'}:continue
    if p.name.startswith('recovery-'):continue
    for h in pat.findall(p.read_text(errors='ignore')):
        h=h.lower().removeprefix('www.')
        if h!='arquindex.com.br' and all(0<len(x)<=63 for x in h.split('.')):public_hosts.add(h)
HOSTS=sorted(public_hosts)
ORIGINAL_DNS=['177.234.150.42','177.234.150.43']
class Page(HTMLParser):
    def __init__(self): super().__init__(); self.canonical=[]; self.title=False; self.t=''; self.h1=0
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='title': self.title=True
        if t=='h1':self.h1+=1
        if t=='link' and 'canonical' in d.get('rel','').lower():self.canonical.append(d.get('href','')[:250])
    def handle_endtag(self,t):
        if t=='title':self.title=False
    def handle_data(self,d):
        if self.title:self.t+=d
def old_dns(host):
    out={'a':[],'cname':[]}
    for server in ORIGINAL_DNS:
        try:
            ans=dns.query.udp(dns.message.make_query(host,'A'),server,timeout=3)
            if ans.rcode()!=0:out['rcode']=ans.rcode();continue
            for rr in ans.answer:
                if rr.rdtype==dns.rdatatype.A:
                    out['a'] += [str(x) for x in rr if ipaddress.ip_address(str(x)).is_global]
                elif rr.rdtype==dns.rdatatype.CNAME:out['cname'] += [str(x.target).rstrip('.') for x in rr]
            if out['a'] or out['cname']:break
        except Exception as e:out['dns_error']=type(e).__name__
    out['a']=sorted(set(out['a']));out['cname']=sorted(set(out['cname']))
    return out
def origin_get(host,ip,path='/'):
    c=http.client.HTTPConnection(ip,80,timeout=8)
    try:
        c.request('GET',path,headers={'Host':host,'User-Agent':'Arquindex-Recovery/1.0','Accept-Encoding':'identity'})
        r=c.getresponse();data=r.read(2000000)
        result={'status':r.status,'bytes':len(data),'location':r.getheader('Location'),'content_type':r.getheader('Content-Type','')}
        if r.status==200 and 'html' in result['content_type']:
            html=data.decode('utf-8','replace');p=Page();p.feed(html)
            result.update(title=p.t[:170],canonical=p.canonical,h1=p.h1,sha256=hashlib.sha256(data).hexdigest(),directory_listing=bool(re.search(r'<title>Index of|<h1>Index of',html,re.I)),parked=any(x in html.lower() for x in ['default website page','account suspended','cgi-sys/defaultwebpage']))
        return result
    finally:c.close()
def check(host):
    result={'host':host,'dns':old_dns(host)}
    ips=result['dns']['a']
    if not ips and not result['dns']['cname']:ips=['177.234.150.42'];result['fallback_ip']=True
    if ips:
        ip=ips[0];result['origin_ip']=ip
        try:result['origin']=origin_get(host,ip)
        except Exception as e:result['origin']={'error':type(e).__name__}
    print('RESTORE_RECORD '+json.dumps(result,separators=(',',':'),ensure_ascii=False),flush=True)
    return result
start=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:rows=list(pool.map(check,HOSTS))
print('RESTORE_SUMMARY '+json.dumps({'hosts':len(rows),'origin200':sum(x.get('origin',{}).get('status')==200 for x in rows),'seconds':round(time.time()-start)}),flush=True)
