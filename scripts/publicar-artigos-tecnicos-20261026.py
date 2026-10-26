"""Publica os artigos de 26/10/2026 com backup, rollback e validação pública."""
import ftplib, hashlib, io, json, os, pathlib, re, socket, ssl, time
import urllib.request, urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT = "https://www.arquindex.com.br/"
DATE = "2026-10-26"
SITEMAP = "/public_html/sitemap-artigos.xml"
ARTICLES = [
    {
        "source": pathlib.Path("artigos-tecnicos/2026-10-26/metadados-decreto-10278-indice-digitalizacao/index.html"),
        "target": "/public_html/blog/metadados-decreto-10278-indice-digitalizacao/index.html",
        "url": ROOT + "blog/metadados-decreto-10278-indice-digitalizacao/",
        "marker": "ARQ-ARTICLE-20261026-METADADOS-DECRETO-10278",
    },
    {
        "source": pathlib.Path("artigos-tecnicos/2026-10-26/tipos-aspectos-pastas-alfresco-modelagem-documental/index.html"),
        "target": "/public_html/blog/tipos-aspectos-pastas-alfresco-modelagem-documental/index.html",
        "url": ROOT + "blog/tipos-aspectos-pastas-alfresco-modelagem-documental/",
        "marker": "ARQ-ARTICLE-20261026-ALFRESCO-TIPOS-ASPECTOS-PASTAS",
    },
]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.canonical = []
        self.robots = []
        self.article = 0
        self.skip = 0
        self.text = []
        self.ld = 0
        self.json = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href"))
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.robots.append(values.get("content", ""))
        if tag == "article":
            self.article += 1
        if tag in {"script", "style", "nav", "footer", "aside"}:
            self.skip += 1
        if tag == "script" and values.get("type") == "application/ld+json":
            self.ld += 1

    def handle_endtag(self, tag):
        if tag == "article":
            self.article = max(0, self.article - 1)
        if tag in {"script", "style", "nav", "footer", "aside"}:
            self.skip = max(0, self.skip - 1)
        if tag == "script" and self.ld:
            self.ld -= 1

    def handle_data(self, data):
        if self.article and not self.skip:
            self.text.append(data)
        if self.ld:
            self.json.append(data)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate(data, spec):
    text = data.decode("utf-8")
    page = Page()
    page.feed(text)
    words = re.findall(r"\b[\wÀ-ÿ][\wÀ-ÿ’'-]*\b", " ".join(page.text))
    assert page.h1 == 1 and page.canonical == [spec["url"]]
    assert len(page.robots) == 1
    assert "index" in page.robots[0].lower() and "follow" in page.robots[0].lower()
    assert len(words) >= 1500 and spec["marker"] in text
    assert "comercial@arquindex.com.br" in text and "5531973632725" in text
    assert 'datePublished":"' + DATE in text
    schemas = json.loads("".join(page.json))
    assert schemas["@context"] == "https://schema.org"
    return len(words)


def http(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ArquindexEditorialVerification/2026.10", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.status, response.url, response.headers, response.read()


def get(ftp, path):
    output = bytearray()
    ftp.retrbinary("RETR " + path, output.extend)
    return bytes(output)


def put(ftp, path, data):
    ftp.storbinary("STOR " + path, io.BytesIO(data))
    assert get(ftp, path) == data, ("FTPS_READBACK", path)


def ensure(ftp, path):
    here = ftp.pwd()
    try:
        ftp.cwd("/")
        current = ""
        for part in path.strip("/").split("/"):
            current += "/" + part
            try:
                ftp.cwd(current)
            except ftplib.error_perm as exc:
                if not str(exc).startswith("550"):
                    raise
                ftp.mkd(current)
                ftp.cwd(current)
    finally:
        ftp.cwd(here)


planned = {}
previous = {}
applied = []
for article in ARTICLES:
    data = article["source"].read_bytes()
    article["words"] = validate(data, article)
    article["sha256"] = sha(data)
    planned[article["target"]] = data

report = {
    "date": DATE,
    "started_at": datetime.now(timezone.utc).isoformat(),
    "published": False,
    "articles": [
        {key: article[key] for key in ("url", "target", "marker", "words", "sha256")}
        for article in ARTICLES
    ],
}
pathlib.Path("publish-report").mkdir(exist_ok=True)
expected = set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
provider = set(socket.gethostbyname_ex("h59.servidorhh.com")[2])
assert expected & provider
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

try:
    with ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=60) as ftp:
        ftp.connect("h59.servidorhh.com", 21)
        assert ftp.sock.getpeername()[0] in expected
        ftp.login("arquind2", os.environ["FTP_PASSWORD"])
        ftp.prot_p()
        ftp.set_pasv(True)
        homepage = get(ftp, "/public_html/index.html")
        assert b"arquindex" in homepage.lower()

        for article in ARTICLES:
            ensure(ftp, article["target"].rsplit("/", 1)[0])
            try:
                previous[article["target"]] = get(ftp, article["target"])
            except ftplib.error_perm as exc:
                if not str(exc).startswith("550"):
                    raise
                previous[article["target"]] = None
            assert previous[article["target"]] in (None, planned[article["target"]]), (
                "DESTINATION_CONFLICT",
                article["target"],
            )

        sitemap_before = get(ftp, SITEMAP)
        previous[SITEMAP] = sitemap_before
        namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
        ET.register_namespace("", namespace)
        root = ET.fromstring(sitemap_before)
        assert root.tag == "{" + namespace + "}urlset"
        existing = {node.text for node in root.iter("{" + namespace + "}loc")}
        for article in ARTICLES:
            if article["url"] not in existing:
                node = ET.SubElement(root, "{" + namespace + "}url")
                ET.SubElement(node, "{" + namespace + "}loc").text = article["url"]
                ET.SubElement(node, "{" + namespace + "}lastmod").text = DATE
        planned[SITEMAP] = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        backup = "/seo-backups/artigos-20261026-" + stamp
        ensure(ftp, "/seo-backups")
        ftp.mkd(backup)
        put(ftp, backup + "/.htaccess", b"Require all denied\n")
        manifest = {}
        for path, old in previous.items():
            if old is not None:
                name = hashlib.sha256(path.encode()).hexdigest() + ".bak"
                put(ftp, backup + "/" + name, old)
                manifest[path] = {"backup": name, "sha256": sha(old)}
        put(ftp, backup + "/manifest.json", json.dumps(manifest, indent=2).encode())
        report["backup"] = backup

        status, _, _, body = http(ROOT + "robots.txt")
        assert status == 200
        robot = urllib.robotparser.RobotFileParser()
        robot.parse(body.decode().splitlines())
        assert all(robot.can_fetch("Googlebot", article["url"]) for article in ARTICLES)

        try:
            for path, data in planned.items():
                old = previous[path]
                if old == data:
                    continue
                if old is not None:
                    assert get(ftp, path) == old, ("CONCURRENT_CHANGE", path)
                applied.append(path)
                put(ftp, path, data)

            for article in ARTICLES:
                result = None
                for _ in range(8):
                    try:
                        candidate = http(article["url"])
                        if candidate[0] == 200 and candidate[1] == article["url"] and article["marker"].encode() in candidate[3]:
                            result = candidate
                            break
                    except Exception:
                        pass
                    time.sleep(5)
                assert result, ("PUBLIC_ARTICLE_NOT_VISIBLE", article["url"])
                words = validate(result[3], article)
                assert sha(result[3]) == article["sha256"]
                assert "noindex" not in result[2].get("X-Robots-Tag", "").lower()
                article["http"] = result[0]
                article["verified_words"] = words

            status, final, _, body = http(ROOT + "sitemap-artigos.xml")
            assert status == 200 and final == ROOT + "sitemap-artigos.xml"
            urls = {node.text for node in ET.fromstring(body).iter("{" + namespace + "}loc")}
            assert all(article["url"] in urls for article in ARTICLES)
            assert get(ftp, "/public_html/index.html") == homepage
            report.update(
                {
                    "published": True,
                    "sitemap": ROOT + "sitemap-artigos.xml",
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                    "articles": [
                        {key: article[key] for key in ("url", "target", "marker", "words", "sha256", "http", "verified_words")}
                        for article in ARTICLES
                    ],
                }
            )
            print("ARTIGOS_20261026_HTTP200_CANONICAL_ROBOTS_SITEMAP_VERIFIED", flush=True)
        except Exception:
            rolled = []
            for path in reversed(applied):
                if get(ftp, path) != planned[path]:
                    continue
                if previous[path] is None:
                    ftp.delete(path)
                else:
                    put(ftp, path, previous[path])
                rolled.append(path)
            report["rolled_back"] = rolled
            raise
finally:
    report_path = pathlib.Path("publish-report/artigos-20261026.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False), flush=True)

