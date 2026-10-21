"""Publica dois artigos técnicos novos com backup, sitemap, rollback e validação pública."""
import ftplib
import hashlib
import io
import json
import os
import pathlib
import re
import socket
import ssl
import time
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT = "https://www.arquindex.com.br/"
DATE = "2026-10-21"
SITEMAP_TARGET = "/public_html/sitemap-artigos.xml"
ARTICLES = [
    {
        "source": pathlib.Path("artigos-tecnicos/2026-10-21/temporalidade-no-alfresco-eventos-retencao-bloqueio/index.html"),
        "target": "/public_html/blog/temporalidade-no-alfresco-eventos-retencao-bloqueio/index.html",
        "url": ROOT + "blog/temporalidade-no-alfresco-eventos-retencao-bloqueio/",
        "marker": "ARQ-ARTICLE-20261021-ALFRESCO-TEMPORALIDADE",
    },
    {
        "source": pathlib.Path("artigos-tecnicos/2026-10-21/indice-mestre-databook-completude-aprovacao/index.html"),
        "target": "/public_html/blog/indice-mestre-databook-completude-aprovacao/index.html",
        "url": ROOT + "blog/indice-mestre-databook-completude-aprovacao/",
        "marker": "ARQ-ARTICLE-20261021-DATABOOK-INDICE-MESTRE",
    },
]


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.canonical = []
        self.robots = []
        self.article_depth = 0
        self.skip_depth = 0
        self.text = []
        self.ld_depth = 0
        self.ld = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content", ""))
        if tag == "article":
            self.article_depth += 1
        if tag in {"script", "style", "nav", "footer", "aside"}:
            self.skip_depth += 1
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.ld_depth += 1

    def handle_endtag(self, tag):
        if tag == "article":
            self.article_depth = max(0, self.article_depth - 1)
        if tag in {"script", "style", "nav", "footer", "aside"}:
            self.skip_depth = max(0, self.skip_depth - 1)
        if tag == "script" and self.ld_depth:
            self.ld_depth -= 1

    def handle_data(self, data):
        if self.article_depth and not self.skip_depth:
            self.text.append(data)
        if self.ld_depth:
            self.ld.append(data)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_page(data, spec):
    text = data.decode("utf-8")
    parser = ArticleParser()
    parser.feed(text)
    words = re.findall(r"\b[\wÀ-ÿ][\wÀ-ÿ’'-]*\b", " ".join(parser.text))
    assert parser.h1 == 1, ("H1_COUNT", parser.h1)
    assert parser.canonical == [spec["url"]], ("CANONICAL", parser.canonical)
    assert len(parser.robots) == 1 and "index" in parser.robots[0] and "follow" in parser.robots[0]
    assert len(words) >= 1500, ("MAIN_WORDS", len(words))
    assert spec["marker"] in text
    assert "comercial@arquindex.com.br" in text and "5531973632725" in text
    assert "datePublished\":\"2026-10-21" in text
    json_text = "".join(parser.ld)
    parsed = json.loads(json_text)
    assert parsed.get("@context") == "https://schema.org"
    return len(words)


def http(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "ArquindexEditorialVerification/2026.10", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=40) as response:
        return response.status, response.url, response.headers, response.read()


def ftp_get(ftp, path):
    out = bytearray()
    ftp.retrbinary("RETR " + path, out.extend)
    return bytes(out)


def ftp_put(ftp, path, data):
    ftp.storbinary("STOR " + path, io.BytesIO(data))
    assert ftp_get(ftp, path) == data, ("FTPS_READBACK", path)


def ensure_dir(ftp, path):
    current = ftp.pwd()
    try:
        ftp.cwd("/")
        partial = ""
        for part in path.strip("/").split("/"):
            partial += "/" + part
            try:
                ftp.cwd(partial)
            except ftplib.error_perm as exc:
                if not str(exc).startswith("550"):
                    raise
                ftp.mkd(partial)
                ftp.cwd(partial)
    finally:
        ftp.cwd(current)


def missing_file(exc):
    return str(exc).startswith("550")


sources = {}
for article in ARTICLES:
    data = article["source"].read_bytes()
    article["words"] = validate_page(data, article)
    article["sha256"] = digest(data)
    sources[article["target"]] = data

report = {
    "date": DATE,
    "started_at": datetime.now(timezone.utc).isoformat(),
    "published": False,
    "articles": [
        {k: a[k] for k in ("url", "target", "marker", "words", "sha256")}
        for a in ARTICLES
    ],
}
pathlib.Path("publish-report").mkdir(exist_ok=True)

expected_ips = set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
provider_ips = set(socket.gethostbyname_ex("h59.servidorhh.com")[2])
assert expected_ips & provider_ips, "PROVIDER_DNS_MISMATCH"

previous = {}
planned = dict(sources)
applied = []
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

try:
    with ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=55) as ftp:
        ftp.connect("h59.servidorhh.com", 21)
        assert ftp.sock.getpeername()[0] in expected_ips, "PROVIDER_IP_MISMATCH"
        ftp.login("arquind2", os.environ["FTP_PASSWORD"])
        ftp.prot_p()
        ftp.set_pasv(True)
        homepage = ftp_get(ftp, "/public_html/index.html")
        assert b"arquindex" in homepage.lower(), "WRONG_DOCUMENT_ROOT"

        for article in ARTICLES:
            ensure_dir(ftp, article["target"].rsplit("/", 1)[0])
            try:
                previous[article["target"]] = ftp_get(ftp, article["target"])
            except ftplib.error_perm as exc:
                if not missing_file(exc):
                    raise
                previous[article["target"]] = None
            assert previous[article["target"]] in (None, planned[article["target"]]), (
                "DESTINATION_ALREADY_EXISTS_WITH_OTHER_CONTENT",
                article["target"],
            )

        sitemap_before = ftp_get(ftp, SITEMAP_TARGET)
        previous[SITEMAP_TARGET] = sitemap_before
        ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
        ET.register_namespace("", ns)
        root = ET.fromstring(sitemap_before)
        assert root.tag == "{" + ns + "}urlset", "UNEXPECTED_ARTICLE_SITEMAP"
        existing = {node.text for node in root.iter("{" + ns + "}loc")}
        for article in ARTICLES:
            if article["url"] not in existing:
                entry = ET.SubElement(root, "{" + ns + "}url")
                ET.SubElement(entry, "{" + ns + "}loc").text = article["url"]
                ET.SubElement(entry, "{" + ns + "}lastmod").text = DATE
        sitemap_after = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        planned[SITEMAP_TARGET] = sitemap_after
        before_urls = {node.text for node in ET.fromstring(sitemap_before).iter("{" + ns + "}loc")}
        after_urls = {node.text for node in ET.fromstring(sitemap_after).iter("{" + ns + "}loc")}
        assert before_urls.issubset(after_urls)

        backup = "/seo-backups/artigos-20261021-" + stamp
        ensure_dir(ftp, "/seo-backups")
        ftp.mkd(backup)
        ftp_put(ftp, backup + "/.htaccess", b"Require all denied\n")
        manifest = {}
        for path, old in previous.items():
            if old is not None:
                name = hashlib.sha256(path.encode()).hexdigest() + ".bak"
                ftp_put(ftp, backup + "/" + name, old)
                manifest[path] = {"backup": name, "sha256": digest(old)}
        ftp_put(ftp, backup + "/manifest.json", json.dumps(manifest, indent=2).encode())
        report["backup"] = backup

        robot_status, _, _, robot_body = http(ROOT + "robots.txt")
        assert robot_status == 200
        robot = urllib.robotparser.RobotFileParser()
        robot.parse(robot_body.decode("utf-8").splitlines())
        for article in ARTICLES:
            assert robot.can_fetch("Googlebot", article["url"]), ("ROBOTS_BLOCKED", article["url"])

        try:
            for path, data in planned.items():
                old = previous[path]
                if old == data:
                    continue
                if old is not None:
                    assert ftp_get(ftp, path) == old, ("CONCURRENT_CHANGE", path)
                applied.append(path)
                ftp_put(ftp, path, data)

            for article in ARTICLES:
                verified = None
                for attempt in range(7):
                    try:
                        status, final, headers, body = http(article["url"])
                        if status == 200 and final == article["url"] and article["marker"].encode() in body:
                            verified = (status, final, headers, body)
                            break
                    except Exception:
                        pass
                    time.sleep(5)
                assert verified is not None, ("PUBLIC_ARTICLE_NOT_VISIBLE", article["url"])
                status, final, headers, body = verified
                words = validate_page(body, article)
                assert digest(body) == article["sha256"], ("PUBLIC_BYTES_MISMATCH", article["url"])
                assert "noindex" not in headers.get("X-Robots-Tag", "").lower()
                article["verified_words"] = words
                article["http"] = status

            status, final, headers, public_sitemap = http(ROOT + "sitemap-artigos.xml")
            assert status == 200 and final == ROOT + "sitemap-artigos.xml"
            public_root = ET.fromstring(public_sitemap)
            public_urls = {node.text for node in public_root.iter("{" + ns + "}loc")}
            assert all(a["url"] in public_urls for a in ARTICLES)
            assert ftp_get(ftp, "/public_html/index.html") == homepage, "HOMEPAGE_CHANGED"
            report["published"] = True
            report["sitemap"] = ROOT + "sitemap-artigos.xml"
            report["completed_at"] = datetime.now(timezone.utc).isoformat()
            report["articles"] = [
                {k: a[k] for k in ("url", "target", "marker", "words", "sha256", "http", "verified_words")}
                for a in ARTICLES
            ]
            print("ARTIGOS_20261021_HTTP200_CANONICAL_ROBOTS_SITEMAP_VERIFIED", flush=True)
        except Exception:
            rolled_back = []
            for path in reversed(applied):
                if ftp_get(ftp, path) != planned[path]:
                    continue
                if previous[path] is None:
                    ftp.delete(path)
                else:
                    ftp_put(ftp, path, previous[path])
                rolled_back.append(path)
            report["rolled_back"] = rolled_back
            raise
finally:
    pathlib.Path("publish-report/artigos-20261021.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False), flush=True)
