import concurrent.futures, datetime, ftplib, hashlib, html, html.parser, io, json, os, posixpath, re, sys, time, urllib.error, urllib.parse, urllib.request, uuid
import xml.etree.ElementTree as ET
BASE = "https://www.arquindex.com.br"
HOSTS = {"arquindex.com.br", "www.arquindex.com.br"}
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
TODAY = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
class Info(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.robots = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical.append(a.get("href", ""))
        if tag == "meta" and a.get("name", "").lower() in ("robots", "googlebot"):
            self.robots.append(a.get("content", "").lower())
def fetch(url):
    result = {"url": url}
    p = urllib.parse.urlsplit(url)
    if p.hostname not in HOSTS or p.scheme not in ("http", "https"):
        return dict(result, skipped="other_host")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ArquindexSEORecovery/1.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read(3 * 1024 * 1024 + 1)
            if len(data) > 3 * 1024 * 1024:
                return dict(result, error="too_large")
            info = Info()
            info.feed(data.decode("utf-8", errors="replace"))
            result.update(status=r.status, final=r.url, canonical=info.canonical, noindex=any("noindex" in x for x in info.robots), data=data)
    except urllib.error.HTTPError as e:
        result["status"] = e.code
    except (OSError, ValueError) as e:
        result["error"] = type(e).__name__
    return result
def slash_equivalent(a, b):
    x, y = urllib.parse.urlsplit(a), urllib.parse.urlsplit(b)
    return x.scheme == y.scheme and x.netloc == y.netloc and x.query == y.query and x.fragment == y.fragment and x.path.rstrip("/") == y.path.rstrip("/")
def patch_canonical(text, old, new):
    count = 0
    def link(m):
        nonlocal count
        tag = m.group(0)
        rel = re.search(r'\brel\s*=\s*(["\x27])(.*?)\1', tag, re.I | re.S)
        if not rel or "canonical" not in rel.group(2).lower().split():
            return tag
        def href(h):
            nonlocal count
            if html.unescape(h.group(2)) != old:
                return h.group(0)
            count += 1
            return "href=" + h.group(1) + html.escape(new, quote=True) + h.group(1)
        return re.sub(r'\bhref\s*=\s*(["\x27])(.*?)\1', href, tag, flags=re.I | re.S)
    result = re.sub(r"<link\b[^>]*>", link, text, flags=re.I | re.S)
    return result, count
def patch_links(text, page_url, mapping):
    count = 0
    def anchor(m):
        nonlocal count
        tag = m.group(0)
        def href(h):
            nonlocal count
            raw = html.unescape(h.group(2))
            if not raw or raw.startswith("#"):
                return h.group(0)
            absolute = urllib.parse.urljoin(page_url, raw)
            parsed = urllib.parse.urlsplit(absolute)
            key = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
            if key not in mapping:
                return h.group(0)
            target = mapping[key] + ("#" + parsed.fragment if parsed.fragment else "")
            if target == absolute:
                return h.group(0)
            count += 1
            return "href=" + h.group(1) + html.escape(target, quote=True) + h.group(1)
        return re.sub(r'\bhref\s*=\s*(["\x27])(.*?)\1', href, tag, flags=re.I | re.S)
    return re.sub(r"<a\b[^>]*>", anchor, text, flags=re.I | re.S), count
def main():
    password = os.environ.get("FTP_PASSWORD", "")
    if not password:
        sys.exit("FTP_PASSWORD ausente")
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(os.environ["FTP_HOST"], 21)
    ftp.login(os.environ["FTP_USERNAME"], password)
    ftp.cwd("public_html")
    root = ftp.pwd()
    parent = posixpath.dirname(root.rstrip("/")) or "/"
    if root.rstrip("/") == parent.rstrip("/"):
        sys.exit("Backup fora da raiz publica nao pode ser confirmado.")
    cache = {}
    def read(path):
        if path in cache:
            return cache[path]
        output = bytearray()
        def receive(chunk):
            output.extend(chunk)
            if len(output) > 8 * 1024 * 1024:
                raise ValueError("Arquivo acima do limite")
        ftp.retrbinary("RETR " + posixpath.join(root, path), receive)
        cache[path] = bytes(output)
        return cache[path]
    def exists(path):
        try:
            ftp.size(posixpath.join(root, path))
            return True
        except ftplib.error_perm:
            return False
    original_index = read("sitemap.xml")
    index = ET.fromstring(original_index)
    if index.tag != "{" + NS + "}sitemapindex":
        sys.exit("sitemap.xml nao e um indice reconhecido.")
    maps = {}
    for loc in index.findall(".//{" + NS + "}loc"):
        p = urllib.parse.urlsplit(loc.text or "")
        if p.hostname != "www.arquindex.com.br" or not p.path.endswith(".xml"):
            sys.exit("Indice contem destino fora do escopo.")
        path = urllib.parse.unquote(p.path).lstrip("/")
        xml = ET.fromstring(read(path))
        if xml.tag != "{" + NS + "}urlset":
            sys.exit("Mapa filho nao reconhecido.")
        maps[path] = xml
    urls = list(dict.fromkeys((loc.text or "").strip() for x in maps.values() for loc in x.findall(".//{" + NS + "}loc")))
    print("Verificando URLs de " + str(len(maps)) + " mapas: " + str(len(urls)), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        checks = dict(zip(urls, pool.map(fetch, urls)))
    mapping, source_pages, review = {}, {}, []
    for url, check in checks.items():
        final = check.get("final", "")
        if check.get("status") != 200 or check.get("noindex") or urllib.parse.urlsplit(url).query:
            review.append({"url": url, "status": check.get("status"), "reason": check.get("error", "query_or_not_indexable")})
            continue
        p = urllib.parse.urlsplit(final)
        canon = check.get("canonical", [])
        if p.hostname != "www.arquindex.com.br" or p.scheme != "https" or len(canon) != 1:
            review.append({"url": url, "reason": "canonical_review"})
            continue
        if not slash_equivalent(canon[0], final):
            review.append({"url": url, "reason": "different_canonical"})
            continue
        if final != url and slash_equivalent(url, final):
            mapping[url] = final
        path = urllib.parse.unquote(p.path).lstrip("/")
        source = (path + "index.html") if p.path.endswith("/") else path
        if not source:
            source = "index.html"
        if not source.endswith(".html") or ".." in source.split("/"):
            continue
        try:
            raw = read(source)
        except ftplib.error_perm:
            review.append({"url": url, "reason": "source_not_found"})
            continue
        if hashlib.sha256(raw).digest() != hashlib.sha256(check["data"]).digest():
            review.append({"url": url, "reason": "source_public_mismatch"})
            continue
        source_pages[source] = {"url": final, "old_canonical": canon[0], "data": raw}
    changes, canonical_changes, link_changes, sitemap_changes = {}, 0, 0, 0
    for path, page in source_pages.items():
        text = page["data"].decode("utf-8")
        if page["old_canonical"] != page["url"]:
            text, n = patch_canonical(text, page["old_canonical"], page["url"])
            if n != 1:
                sys.exit("Numero inesperado de canonicas; nenhum arquivo publicado.")
            canonical_changes += n
        text, n = patch_links(text, page["url"], mapping)
        link_changes += n
        new = text.encode("utf-8")
        if new != page["data"]:
            changes[path] = new
    for path, xml in maps.items():
        n = 0
        for loc in xml.findall(".//{" + NS + "}loc"):
            old = (loc.text or "").strip()
            if old in mapping:
                loc.text = mapping[old]
                n += 1
        if n:
            new = ET.tostring(xml, encoding="utf-8", xml_declaration=True) + b"\n"
            ET.fromstring(new)
            changes[path] = new
            sitemap_changes += n
    for child in index.findall("{" + NS + "}sitemap"):
        loc = child.find("{" + NS + "}loc")
        path = urllib.parse.urlsplit(loc.text or "").path.lstrip("/")
        if path in changes:
            lm = child.find("{" + NS + "}lastmod")
            if lm is not None:
                child.remove(lm)
    if any(path in changes for path in maps):
        changes["sitemap.xml"] = ET.tostring(index, encoding="utf-8", xml_declaration=True) + b"\n"
    summary = {"checked_urls": len(urls), "http_200": sum(x.get("status") == 200 for x in checks.values()), "http_404": sum(x.get("status") == 404 for x in checks.values()), "canonicals_corrected": canonical_changes, "internal_links_corrected": link_changes, "sitemap_urls_corrected": sitemap_changes, "files_to_change": len(changes), "review_count": len(review)}
    print("PLANO " + json.dumps(summary), flush=True)
    for row in review[:12]:
        print("REVISAO " + json.dumps(row, ensure_ascii=False), flush=True)
    if not changes:
        ftp.quit()
        print("Nenhuma alteracao necessaria dentro deste escopo.")
        return
    if os.environ.get("APPLY_CHANGES") != "true":
        ftp.quit()
        print("Modo verificacao; nenhum arquivo alterado.")
        return
    token = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    backup = posixpath.join(parent, "seo-recovery-backups", token)
    def mkdirs(path):
        current = "/"
        for part in path.strip("/").split("/"):
            current = posixpath.join(current, part)
            try:
                ftp.mkd(current)
            except ftplib.error_perm:
                ftp.cwd(current)
        ftp.cwd(root)
    mkdirs(backup)
    originals = {path: read(path) for path in changes}
    for path, data in originals.items():
        destination = posixpath.join(backup, path)
        mkdirs(posixpath.dirname(destination))
        ftp.storbinary("STOR " + destination, io.BytesIO(data))
        restored = bytearray()
        ftp.retrbinary("RETR " + destination, restored.extend)
        if bytes(restored) != data:
            sys.exit("Backup nao verificado; nenhum arquivo do site alterado.")
    applied = []
    try:
        for path, data in changes.items():
            current = bytearray()
            destination = posixpath.join(root, path)
            ftp.retrbinary("RETR " + destination, current.extend)
            if bytes(current) != originals[path]:
                raise RuntimeError("Arquivo mudou durante a auditoria")
            temp = destination + ".seo-" + token
            ftp.storbinary("STOR " + temp, io.BytesIO(data))
            staged = bytearray()
            ftp.retrbinary("RETR " + temp, staged.extend)
            if bytes(staged) != data:
                raise RuntimeError("Upload temporario divergiu")
            ftp.rename(temp, destination)
            applied.append(path)
            public_url = BASE + "/" + urllib.parse.quote(path, safe="/")
            check = fetch(public_url)
            if check.get("status") != 200 or check.get("data") != data:
                raise RuntimeError("Publicacao nao verificada")
            print("PUBLICADO " + path, flush=True)
    except Exception:
        for path in reversed(applied):
            ftp.storbinary("STOR " + posixpath.join(root, path), io.BytesIO(originals[path]))
        ftp.quit()
        raise RuntimeError("Falha na verificacao; arquivos publicados restaurados")
    ftp.quit()
    print("CONCLUIDO " + json.dumps(dict(summary, files_published=len(applied), backup=backup, verified=True)), flush=True)
if __name__ == "__main__":
    main()
