"""Read-only DNS and authorized cPanel diagnostics, never prints secrets."""
import concurrent.futures as cf
import json, os, socket, urllib.parse as up
from pathlib import Path
import dns.resolver
import requests
OUT=Path('audit-56-config'); OUT.mkdir(exist_ok=True)
hosts=[e['host'] for e in json.loads(Path('seo-regional/56-sites/manifest.json').read_text())]

def query(host,server,typ='A'):
    r=dns.resolver.Resolver(configure=False); r.nameservers=[server]; r.lifetime=5
    try: return {'server':server,'type':typ,'status':'ANSWER','answers':[str(x) for x in r.resolve(host,typ)]}
    except dns.resolver.NXDOMAIN: return {'server':server,'type':typ,'status':'NXDOMAIN'}
    except dns.resolver.NoAnswer: return {'server':server,'type':typ,'status':'NOANSWER'}
    except Exception as e: return {'server':server,'type':typ,'status':type(e).__name__}

def check(h):
    result={'host':h,'queries':[query(h,s,t) for s in ['1.1.1.1','8.8.8.8'] for t in ['A','AAAA']]}
    print(json.dumps(result),flush=True); return result
with cf.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(check,hosts))
Path(OUT/'dns.json').write_text(json.dumps(results,indent=2))
cp={'credentials':{k:bool(os.getenv(k)) for k in ['CPANEL_HOST','CPANEL_USER','CPANEL_API_TOKEN']}}
host=os.getenv('CPANEL_HOST','').strip().rstrip('/')
if host and not host.startswith('https://'): host='https://'+host
if not all(cp['credentials'].values()):
    cp['result']='BLOCKED: CPANEL_HOST/CPANEL_USER/CPANEL_API_TOKEN incompletos; nenhuma alteração'
elif up.urlparse(host).scheme!='https' or up.urlparse(host).hostname not in ['arquindex.com.br','www.arquindex.com.br','cpanel.arquindex.com.br','ftp.arquindex.com.br'] or up.urlparse(host).port!=2083:
    cp['result']='BLOCKED: endpoint cPanel fora dos destinos confirmados; credenciais não enviadas'
else:
    try:
        auth={'Authorization':'cpanel '+os.environ['CPANEL_USER']+':'+os.environ['CPANEL_API_TOKEN']}
        r=requests.get(host+'/execute/DomainInfo/domains_data',headers=auth,timeout=20,allow_redirects=False)
        cp['http_status']=r.status_code
        if r.status_code==200:
            j=r.json(); cp['api_status']=j.get('status')
            if j.get('status')==1:
                cp['data']=j.get('data'); cp['result']='READ_ONLY_OK'
            else: cp['result']='API não confirmou leitura'
        else: cp['result']='Autenticação/endpoint não disponível'
    except Exception as e: cp['result']='BLOCKED: '+type(e).__name__
Path(OUT/'cpanel.json').write_text(json.dumps(cp,indent=2))
print('CPANEL',cp.get('result'),flush=True)
lines=['## Confirmação DNS e acesso à configuração (somente leitura)', '', 'Execução: '+os.getenv('AUDIT_RUN_URL',''), '', 'cPanel: '+cp['result'], '', '| Endereço | Cloudflare A / AAAA | Google A / AAAA |','|---|---|---|']
for r in results:
    q=r['queries']; lines.append('| '+r['host']+' | '+q[0]['status']+' / '+q[1]['status']+' | '+q[2]['status']+' / '+q[3]['status']+' |')
Path(OUT/'report.md').write_text('\n'.join(lines)+'\n')
