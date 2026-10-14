import concurrent.futures, datetime, ftplib, hashlib, html, io, json, os, posixpath, re, sys, urllib.parse, urllib.request, uuid, zipfile
import xml.etree.ElementTree as ET
from seo_recovery import BASE, NS, fetch, patch_links

EMBED = 'https://app.trysoro.com/api/embed/da4cf361-eac9-4fc5-8f6e-f4f34a4291a5'
PREFIX = 'blog-original'
CSS = '''body{margin:0;font:18px/1.7 system-ui,sans-serif;color:#183139;background:#f4f8f8}header,footer{background:#103b45;color:white;padding:24px}nav,main,.footer{max-width:1000px;margin:auto}nav{display:flex;gap:24px;flex-wrap:wrap}nav a,footer a{color:white}main{padding:40px 24px}article{background:white;border-radius:14px;padding:36px;overflow-wrap:anywhere}h1{font-size:clamp(28px,4vw,44px);line-height:1.2}h2{line-height:1.3}a{color:#006977}img{max-width:100%;height:auto;border-radius:10px}time{color:#51676c}.cards{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}.cards article{padding:24px}.cards h2{font-size:23px}aside{margin-top:40px}li{margin-bottom:10px}@media(max-width:600px){article{padding:22px}main{padding:24px 12px}}'''

def shell(title, description, url, body, data=None):
    structured = '' if data is None else '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace('<','\\u003c') + '</script>'
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + ' | Arquindex</title><meta name="description" content="' + html.escape(description, quote=True) + '"><link rel="canonical" href="' + url + '"><style>' + CSS + '</style>' + structured + '</head><body><header><nav aria-label="Navegação principal"><a href="/">Arquindex</a><a href="/' + PREFIX + '/">Artigos originais</a><a href="/blog/">Guias e manuais</a><a href="/servicos/">Serviços</a><a href="/contato.html">Contato</a></nav></header><main>' + body + '</main><footer><div class="footer">Arquindex — Digitalização e gestão documental. <a href="/">Conheça a empresa</a></div></footer></body></html>\n').encode('utf-8')

def get_article(slug):
    with urllib.request.urlopen(EMBED + '?post=' + urllib.parse.quote(slug), timeout=30) as response:
        text = response.read(4*1024*1024).decode('utf-8')
    marker = re.search(r'var\s+SORO_ARTICLES\s*=\s*', text)
    if not marker:
        raise ValueError('Dados originais indisponiveis')
    articles, _ = json.JSONDecoder().raw_decode(text[marker.end():])
    matches = [a for a in articles if a.get('slug') == slug]
    if len(matches) != 1:
        raise ValueError('Slug ausente no catalogo original')
    article=matches[0]
    if not article.get('content') and re.fullmatch(r'[a-f0-9-]{36}',article.get('id','')):
        with urllib.request.urlopen(EMBED+'/article/'+article['id'],timeout=30) as response:
            recovered=json.load(response)
        article['content']=recovered.get('content')
    if not article.get('title') or not isinstance(article.get('content'), str) or len(article['content']) < 300:
        raise ValueError('Conteudo original ausente ou incompleto')
    if re.search(r'<(?:script|iframe|form|object)\b|\son\w+\s*=|javascript:',matches[0]['content'],re.I):
        raise ValueError('Conteudo exige revisao de HTML')
    return article

def main():
    ftp=ftplib.FTP(os.environ['FTP_HOST'],timeout=35)
    ftp.login(os.environ['FTP_USERNAME'],os.environ['FTP_PASSWORD'])
    ftp.cwd('public_html'); root=ftp.pwd(); parent=posixpath.dirname(root.rstrip('/')) or '/'
    if root.rstrip('/') == parent.rstrip('/'): raise ValueError('Backup fora da raiz indisponivel')
    originals={}
    def read(path, optional=False):
        if path in originals: return originals[path]
        output=bytearray()
        try:
            ftp.retrbinary('RETR '+posixpath.join(root,path),output.extend)
        except ftplib.error_perm as e:
            if optional and str(e).startswith('550'): originals[path]=None;return None
            raise
        if len(output)>8*1024*1024:raise ValueError('Limite de arquivo')
        originals[path]=bytes(output);return originals[path]
    sitemap=ET.fromstring(read('sitemap-blog-original.xml'))
    old_urls=[(x.text or '').strip() for x in sitemap.findall('.//{'+NS+'}loc')]
    requested={}
    for url in old_urls:
        p=urllib.parse.urlsplit(url); q=urllib.parse.parse_qs(p.query)
        if p.hostname!='www.arquindex.com.br' or p.path!='/index.html' or set(q)!={'post'} or len(q['post'])!=1:raise ValueError('URL fora do escopo')
        slug=q['post'][0]
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Slug invalido')
        requested[slug]=url
    def recover(slug):
        try:return slug,get_article(slug),None
        except ValueError as e:return slug,None,str(e)
        except Exception as e:return slug,None,type(e).__name__
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: results=list(pool.map(recover,requested))
    articles={slug:a for slug,a,error in results if a}
    missing=[{'slug':slug,'reason':error} for slug,a,error in results if error]
    print('RECUPERADOS',json.dumps({'requested':len(requested),'original_articles':len(articles),'missing':missing}),flush=True)
    if not articles:raise ValueError('Nenhum artigo recuperado')
    mapping={requested[slug]:BASE+'/'+PREFIX+'/'+slug+'/' for slug in articles}
    changes={}; links=0
    for slug,a in articles.items():
        url=mapping[requested[slug]]
        content,n=patch_links(a['content'],requested[slug],mapping);links+=n
        # Embedded articles originally resolve relative references on the homepage.
        def absolute_reference(match):
            value=html.unescape(match.group(3))
            if not value or value.startswith('#') or urllib.parse.urlsplit(value).scheme:
                return match.group(0)
            target=urllib.parse.urljoin(requested[slug],value)
            return match.group(1)+'='+match.group(2)+html.escape(target,quote=True)+match.group(2)
        content=re.sub(r'(?<![\w:-])(href|src)\s*=\s*(["\x27])(.*?)\2',absolute_reference,content,flags=re.I|re.S)
        related=[(s,b) for s,b in articles.items() if s!=slug][:6]
        body='<article><h1>'+html.escape(a['title'])+'</h1><time datetime="'+html.escape(a.get('isoDate') or '',quote=True)+'">'+html.escape(a.get('date') or '')+'</time>'
        image=a.get('image') or ''
        if image.startswith('https://'):body+='<p><img src="'+html.escape(image,quote=True)+'" alt="'+html.escape(a['title'],quote=True)+'"></p>'
        body+='<div class="article-content">'+content+'</div></article><aside aria-label="Artigos relacionados"><h2>Leia também</h2><ul>'
        body+=''.join('<li><a href="'+mapping[requested[s]]+'">'+html.escape(b['title'])+'</a></li>' for s,b in related)+'</ul><a href="/'+PREFIX+'/">Todos os artigos</a></aside>'
        data={'@context':'https://schema.org','@type':'BlogPosting','headline':a['title'],'description':a.get('excerpt') or '', 'mainEntityOfPage':url,'publisher':{'@type':'Organization','name':'Arquindex','url':BASE+'/'}}
        if a.get('isoDate'):data['datePublished']=a['isoDate']
        if image.startswith('https://'):data['image']=image
        path=PREFIX+'/'+slug+'/index.html'
        if read(path,optional=True) is not None:raise ValueError('Destino ja existe; publicar exige comparacao')
        changes[path]=shell(a['title'],a.get('excerpt') or '',url,body,data)
    index_path=PREFIX+'/index.html'
    if read(index_path,optional=True) is not None:raise ValueError('Indice ja existe')
    cards='<h1>Artigos da Arquindex</h1><p>Digitalização, gestão documental, privacidade e soluções ECM.</p><div class="cards">'+''.join('<article><h2><a href="'+mapping[requested[s]]+'">'+html.escape(a['title'])+'</a></h2><p>'+html.escape(a.get('excerpt') or '')+'</p></article>' for s,a in articles.items())+'</div>'
    changes[index_path]=shell('Artigos originais da Arquindex','Artigos sobre digitalização, gestão documental, LGPD e ECM.',BASE+'/'+PREFIX+'/',cards)
    # Only change existing public HTML whose bytes match the served document.
    for path in ['index.html','blog/index.html']:
        raw=read(path);public=fetch(BASE+'/'+path)
        if public.get('status')!=200 or public.get('data')!=raw:raise ValueError('HTML publico divergiu')
        text,n=patch_links(raw.decode('utf-8'),BASE+'/'+path,mapping);links+=n
        if path=='blog/index.html':
            if text.lower().count('</main>')!=1:raise ValueError('Limite de main inesperado')
            text=text.replace('</main>','<section><h2>Artigos originais</h2><p><a href="/'+PREFIX+'/">Explore todos os artigos da Arquindex sobre digitalização, gestão documental e LGPD.</a></p></section></main>')
        if text.encode('utf-8')!=raw:changes[path]=text.encode('utf-8')
    excluded=[]
    for row in missing:
        if row['reason']=='Slug ausente no catalogo original':
            old=requested[row['slug']];check=fetch(old)
            if check.get('status')==200 and check.get('canonical')==[BASE+'/']:
                excluded.append(old)
    for entry in list(sitemap.findall('{'+NS+'}url')):
        loc=entry.find('{'+NS+'}loc')
        if loc is not None and loc.text in excluded:sitemap.remove(entry)
    for loc in sitemap.findall('.//{'+NS+'}loc'):
        if loc.text in mapping:loc.text=mapping[loc.text]
    changes['sitemap-blog-original.xml']=ET.tostring(sitemap,encoding='utf-8',xml_declaration=True)+b'\n'
    index=ET.fromstring(read('sitemap.xml'))
    for child in index.findall('{'+NS+'}sitemap'):
        loc=child.find('{'+NS+'}loc')
        if loc is not None and loc.text==BASE+'/sitemap-blog-original.xml':
            lm=child.find('{'+NS+'}lastmod')
            if lm is not None:child.remove(lm)
    changes['sitemap.xml']=ET.tostring(index,encoding='utf-8',xml_declaration=True)+b'\n'
    ht=read('.htaccess');text=ht.decode('utf-8')
    if '# BEGIN ARQUINDEX ORIGINAL BLOG RECOVERY' in text:raise ValueError('Regras de recuperacao ja existem')
    block='# BEGIN ARQUINDEX ORIGINAL BLOG RECOVERY\n<IfModule mod_rewrite.c>\nRewriteEngine On\n'
    for slug in articles:
        block+='RewriteCond %{QUERY_STRING} ^post='+slug+'$\nRewriteRule ^(?:index\\.html)?$ /'+PREFIX+'/'+slug+'/? [R=301,L,NE]\n'
    block+='</IfModule>\n# END ARQUINDEX ORIGINAL BLOG RECOVERY\n'
    changes['.htaccess']=(block+text).encode('utf-8')
    print('PLANO',json.dumps({'static_articles':len(articles),'files':len(changes),'internal_links_corrected':links,'redirects':len(mapping),'obsolete_home_duplicates_excluded':excluded}),flush=True)
    if os.environ.get('APPLY_CHANGES')!='true':ftp.quit();return
    token=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    backup=posixpath.join(parent,'seo-blog-recovery-backups',token)
    def mkdirs(path):
        current='/'
        for part in path.strip('/').split('/'):
            current=posixpath.join(current,part)
            try:ftp.mkd(current)
            except ftplib.error_perm:ftp.cwd(current)
        ftp.cwd(root)
    mkdirs(backup)
    archive=io.BytesIO()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in changes:
            raw=read(path,optional=True)
            if raw is not None:z.writestr(path,raw)
        z.writestr('manifest.json',json.dumps({'new_files':[p for p in changes if originals[p] is None],'changed_files':list(changes),'articles':list(articles),'mapping':mapping},ensure_ascii=False))
        z.writestr('recovered-original-articles.json',json.dumps(articles,ensure_ascii=False))
    zipped=archive.getvalue();ftp.storbinary('STOR '+backup+'/originais.zip',io.BytesIO(zipped))
    verified=bytearray();ftp.retrbinary('RETR '+backup+'/originais.zip',verified.extend)
    if bytes(verified)!=zipped:raise ValueError('Backup divergiu')
    with zipfile.ZipFile(io.BytesIO(verified)) as z:
        if z.testzip() is not None:raise ValueError('Backup invalido')
    applied=[]
    try:
        # New pages, navigation and sitemaps before activating redirects.
        for path,data in changes.items():
            destination=posixpath.join(root,path);mkdirs(posixpath.dirname(destination))
            current=bytearray()
            try:ftp.retrbinary('RETR '+destination,current.extend);existing=bytes(current)
            except ftplib.error_perm:existing=None
            if existing!=originals[path]:raise ValueError('Arquivo mudou durante a preparacao')
            temp=destination+'.seo-'+token
            ftp.storbinary('STOR '+temp,io.BytesIO(data));check=bytearray();ftp.retrbinary('RETR '+temp,check.extend)
            if bytes(check)!=data:raise ValueError('Upload temporario divergiu')
            ftp.rename(temp,destination);applied.append(path)
            if path!='.htaccess':
                result=fetch(BASE+'/'+urllib.parse.quote(path,safe='/'))
                if result.get('status')!=200 or result.get('data')!=data:raise ValueError('Publicacao divergiu: '+path)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            checks=list(pool.map(fetch,mapping))
        for (old,new),c in zip(mapping.items(),checks):
            if c.get('status')!=200 or c.get('final')!=new or c.get('canonical')!=[new] or c.get('noindex'):raise ValueError('Redirecionamento ou canonica divergiu')
        home=fetch(BASE+'/')
        if home.get('status')!=200 or home.get('canonical')!=[BASE+'/']:raise ValueError('Pagina inicial divergiu')
    except Exception:
        for path in reversed(applied):
            destination=posixpath.join(root,path)
            if originals[path] is None:ftp.delete(destination)
            else:ftp.storbinary('STOR '+destination,io.BytesIO(originals[path]))
        ftp.quit();raise RuntimeError('Publicacao falhou; alteracoes restauradas')
    ftp.quit()
    print('CONCLUIDO',json.dumps({'articles_published':len(articles),'files_published':len(applied),'internal_links_corrected':links,'sitemap_urls_replaced':len(mapping),'redirects_verified':len(checks),'obsolete_home_duplicates_excluded':excluded,'unresolved':missing,'backup':backup,'verified':True}),flush=True)

if __name__=='__main__':main()
