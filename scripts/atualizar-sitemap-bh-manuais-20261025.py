import ftplib, hashlib, io, os, ssl, time, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "h59.servidorhh.com"
USER = "arquind2"
REMOTE = "/public_html/sitemap-bh.xml"
URLS = [
    "https://www.arquindex.com.br/digitalizacao-ocr-manual-tecnico-bh/",
    "https://www.arquindex.com.br/guarda-fisica-custodia-manual-planos-bh/",
]
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
Path("artifacts").mkdir(exist_ok=True)

def public_ok(url):
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ArquindexSitemapVerifier/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read()
                if r.status == 200 and b'noindex' not in body:
                    return True
                last = RuntimeError(f"{url}: HTTP {r.status} ou noindex")
        except Exception as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Falha de verificacao publica: {url}: {last}")

for url in URLS:
    public_ok(url)
    print("PAGE_PUBLIC_VERIFIED", url)

context = ssl.create_default_context()
with ftplib.FTP_TLS(context=context, timeout=50) as ftp:
    ftp.connect(HOST, 21)
    ftp.login(USER, os.environ["FTP_PASSWORD"])
    ftp.prot_p()

    old_buffer = io.BytesIO()
    ftp.retrbinary("RETR " + REMOTE, old_buffer.write)
    old = old_buffer.getvalue()
    Path("artifacts/sitemap-bh-before.xml").write_bytes(old)

    root = ET.fromstring(old)
    if root.tag != f"{{{NS}}}urlset":
        raise RuntimeError("sitemap-bh.xml nao e urlset padrao")

    existing = {
        (node.find(f"{{{NS}}}loc").text or "").strip()
        for node in root.findall(f"{{{NS}}}url")
        if node.find(f"{{{NS}}}loc") is not None
    }
    for url in URLS:
        if url not in existing:
            node = ET.SubElement(root, f"{{{NS}}}url")
            ET.SubElement(node, f"{{{NS}}}loc").text = url
            ET.SubElement(node, f"{{{NS}}}lastmod").text = "2026-10-25"
            existing.add(url)
            print("SITEMAP_ADD", url)
        else:
            print("SITEMAP_EXISTING", url)

    updated = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    ET.fromstring(updated)
    Path("artifacts/sitemap-bh-after.xml").write_bytes(updated)

    if updated != old:
        try:
            ftp.storbinary("STOR " + REMOTE, io.BytesIO(updated))
            check = io.BytesIO()
            ftp.retrbinary("RETR " + REMOTE, check.write)
            if check.getvalue() != updated:
                raise RuntimeError("releitura FTPS difere do XML enviado")
        except Exception:
            ftp.storbinary("STOR " + REMOTE, io.BytesIO(old))
            raise

print("SITEMAP_FTPS_VERIFIED", REMOTE, hashlib.sha256(updated).hexdigest(), len(existing))
