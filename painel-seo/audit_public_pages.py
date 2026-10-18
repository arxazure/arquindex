"""Public site audit. No fabricated search rankings or privileged GSC access."""
import json, datetime, urllib.request, urllib.parse, xml.etree.ElementTree as ET, re
from pathlib import Path
ROOT='https://www.arquindex.com.br'
MAX_URLS=120
UA={'User-Agent':'Arquindex-SEO-Audit/1.0 (+https://www.arquindex.com.br)'}
def fetch(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=14) as resp:
        body=resp.read(700000).decode('utf-8','replace')
        return resp.status,resp.geturl(),body
def audit(url):
    result={'url':url,'issues':[]}
    try:
        status,final,body=fetch(url)
        result.update(status=status,final_url=final)
        title=re.search(r'<title[^>]*>(.*?)</title>',body,re.I|re.S)
        desc=re.search(r'<meta[^>]*name=["\\\']description["\\\'][^>]*content=["\\\']([^"\\\']+)',body,re.I|re.S)
        canonical=re.search(r'<link[^>]*rel=["\\\']canonical["\\\'][^>]*href=["\\\']([^"\\\']+)',body,re.I|re.S)
        result['title']=re.sub('<[^>]+>','',title.group(1)).strip() if title else ''
        result['description']=desc.group(1).strip() if desc else ''
        result['canonical']=canonical.group(1) if canonical else ''
        if not result['title']:result['issues'].append('Título HTML ausente')
        if not result['description']:result['issues'].append('Meta description ausente')
        if not result['canonical']:result['issues'].append('Canonical ausente')
        if status>=400:result['issues'].append('HTTP '+str(status))
        if re.search(r'<meta[^>]*name=["\\\']robots["\\\'][^>]*content=["\\\'][^"\\\']*noindex',body,re.I):result['issues'].append('Noindex detectado')
    except Exception as e:
        result['issues'].append('Falha ao acessar URL: '+str(e)[:180])
    return result
def main():
    urls=[ROOT+'/']
    sitemap_status='unavailable'
    try:
        status,final,xml=fetch(ROOT+'/sitemap.xml')
        root=ET.fromstring(xml)
        discovered=[e.text.strip() for e in root.iter() if e.tag.endswith('}loc') or e.tag=='loc']
        urls.extend(u for u in discovered if u.startswith(('https://www.arquindex.com.br/','https://arquindex.com.br/')) and not u.endswith('.xml'))
        sitemap_status='ok'
    except Exception as e:sitemap_status=str(e)[:200]
    urls=list(dict.fromkeys(urls))[:MAX_URLS]
    pages=[audit(url) for url in urls]
    issues=[{'url':p['url'],'issues':p['issues']} for p in pages if p['issues']]
    report={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'Live public HTML + sitemap.xml; not Google Search Console','sitemap_status':sitemap_status,'scanned':len(pages),'issues_count':len(issues),'issues':issues,'pages':pages}
    path=Path(__file__).with_name('auditoria-publica.json')
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Scanned',len(pages),'pages; issues',len(issues))
if __name__=='__main__':main()
