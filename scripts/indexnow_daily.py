#!/usr/bin/env python3
"""Notify IndexNow of changed public Arquindex pages; never claim indexing."""
import concurrent.futures
import hashlib
import json
import os
import re
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser

ENDPOINT = 'https://api.indexnow.org/indexnow'
STATE = Path('.indexnow-state/accepted.json')
REPORT = Path('indexnow-report/report.json')
MAX_BYTES = 8 * 1024 * 1024
MAX_URLS = 25000
KEY_RE = re.compile(r'[A-Za-z0-9-]{8,128}')


class CanonicalAlias(ValueError):
    """The apex sitemap delegates exclusively to the configured www inventory."""


def error_code(exc):
    seen = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, socket.gaierror):
            return 'dns'
        if isinstance(exc, ssl.SSLError):
            return 'tls'
        if isinstance(exc, urllib.error.HTTPError):
            return 'http_' + str(exc.code)
        if isinstance(exc, urllib.error.URLError) and isinstance(exc.reason, BaseException):
            exc = exc.reason
        else:
            exc = exc.__cause__ or exc.__context__
    return 'validation_or_network'


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'bingbot', 'msnbot'):
            tokens = re.split(r'[\s,;]+', attrs.get('content', '').lower())
            self.noindex |= bool({'noindex', 'none'} & set(tokens))


def exclusion_reason(url, body, headers):
    headers = {k.lower(): v for k, v in headers.items()}
    if re.search(r'\b(noindex|none)\b', headers.get('x-robots-tag', ''), re.I):
        return 'x_robots_noindex'
    if 'html' in headers.get('content-type', '').lower() or b'<html' in body[:4096].lower():
        parser = SEOParser()
        parser.feed(body.decode('utf-8', errors='replace'))
        if parser.noindex:
            return 'meta_noindex'
        if len(parser.canonicals) != 1:
            return 'canonical_missing_or_multiple'
        if urllib.parse.urljoin(url, parser.canonicals[0]) != url:
            return 'canonical_points_elsewhere'
    return None


def robots_for(host):
    parser = urllib.robotparser.RobotFileParser()
    try:
        status, body, _ = request('https://' + host + '/robots.txt')
        if status != 200:
            raise ValueError('robots not HTTP 200')
        parser.parse(body.decode('utf-8', errors='replace').splitlines())
    except Exception as exc:
        if error_code(exc) == 'http_404':
            parser.parse([])
        else:
            raise
    return parser


def valid_url(url, host):
    p = urllib.parse.urlsplit(url)
    return (p.scheme == 'https' and p.netloc == host and not p.fragment
            and not p.username and not p.password and not any(c.isspace() for c in url))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Arquindex-IndexNow-Daily/1.0',
        'Content-Type': 'application/json; charset=utf-8' if data else 'text/plain',
        'Cache-Control': 'no-cache',
    })
    for attempt in range(3):
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=20) as res:
                body = res.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise ValueError('response exceeds 8 MiB; not processed')
                return res.status, body, dict(res.headers)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 or 500 <= exc.code <= 599:
                if attempt < 2:
                    delay = exc.headers.get('Retry-After', '')
                    if delay.isdigit() and int(delay) > 60:
                        raise RuntimeError('rate limited; deferred to next run') from exc
                    time.sleep(int(delay) if delay.isdigit() else 5 * (2 ** attempt))
                    continue
            raise RuntimeError('HTTP ' + str(exc.code)) from exc
        except urllib.error.URLError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def hosts_from_repository(root=Path('.')):
    hosts = {'www.arquindex.com.br', 'arquindex.com.br'}
    for path in root.rglob('sitemap*.xml'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        hosts.update(re.findall(r'https://([a-z0-9.-]+\.arquindex\.com\.br)(?=[/:<\s])', text))
    return sorted(h for h in hosts if re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)*arquindex\.com\.br', h))


def discover(host):
    """Read the live sitemap, including sitemap indexes. Never use unpublished URLs."""
    pending = ['https://' + host + '/sitemap.xml']
    seen, pages = set(), set()
    while pending:
        url = pending.pop()
        if url in seen:
            continue
        if len(seen) >= 200:
            raise ValueError('sitemap limit reached; split inventory before retrying')
        seen.add(url)
        if not valid_url(url, host):
            raise ValueError('sitemap outside this host')
        status, body, _ = request(url)
        if status != 200:
            raise ValueError('sitemap not HTTP 200')
        tree = ET.fromstring(body)
        kind = tree.tag.rsplit('}', 1)[-1]
        if kind not in ('sitemapindex', 'urlset'):
            raise ValueError('invalid sitemap XML')
        locs = [(node.text or '').strip() for node in tree.iter()
                if node.tag.rsplit('}', 1)[-1] == 'loc']
        if host == 'arquindex.com.br' and locs and all(
                valid_url(loc, 'www.arquindex.com.br') for loc in locs):
            raise CanonicalAlias('apex sitemap delegates to www.arquindex.com.br; processed separately')
        for node in tree.iter():
            if node.tag.rsplit('}', 1)[-1] != 'loc':
                continue
            loc = (node.text or '').strip()
            if not valid_url(loc, host):
                raise ValueError('sitemap URL outside this host or invalid URL')
            if kind == 'sitemapindex':
                pending.append(loc)
            else:
                pages.add(loc)
                if len(pages) > MAX_URLS:
                    raise ValueError('URL limit reached; no silent truncation')
    if not pages:
        raise ValueError('empty sitemap')
    return sorted(pages)


def key_for(host):
    url = 'https://' + host + '/indexnow-key.txt'
    status, body, _ = request(url)
    key = body.decode('ascii').strip()
    if status != 200 or not KEY_RE.fullmatch(key):
        raise ValueError('missing or invalid IndexNow key on this host')
    # keyLocation at the root authorizes this exact host, including all paths.
    return key, url


def process_host(host, old):
    result = {'host': host, 'checked': 0, 'unchanged': 0, 'changed': 0,
              'received_200': 0, 'pending_202': 0, 'errors': [], 'batches': [],
              'excluded': [], 'stage': 'sitemap', 'status': 'checking'}
    accepted = dict(old)
    try:
        pages = discover(host)
        result['stage'] = 'key'
        key, location = key_for(host)
        result['stage'] = 'robots'
        robots = robots_for(host)
        result['stage'] = 'pages'
        changed = {}
        for url in pages:
            try:
                if not robots.can_fetch('bingbot', url) or not robots.can_fetch('IndexNow', url):
                    result['excluded'].append({'url': url, 'reason': 'robots_disallow'})
                    continue
                status, body, headers = request(url)
                if status != 200:
                    raise ValueError('page not HTTP 200')
                reason = exclusion_reason(url, body, headers)
                if reason:
                    result['excluded'].append({'url': url, 'reason': reason})
                    continue
                digest = hashlib.sha256(body).hexdigest()
                result['checked'] += 1
                if old.get(url) == digest:
                    result['unchanged'] += 1
                else:
                    changed[url] = digest
            except Exception as exc:
                result['errors'].append({'url': url, 'code': error_code(exc), 'error': str(exc)})
        result['changed'] = len(changed)
        urls = sorted(changed)
        result['stage'] = 'submission'
        for offset in range(0, len(urls), 10000):
            batch = urls[offset:offset + 10000]
            status, _, _ = request(ENDPOINT, {'host': host, 'key': key,
                'keyLocation': location, 'urlList': batch})
            result['batches'].append({'http': status, 'count': len(batch)})
            if status == 200:
                result['received_200'] += len(batch)
                accepted.update({u: changed[u] for u in batch})
            elif status == 202:
                result['pending_202'] += len(batch)
                # Ownership pending: do not suppress the next day's retry.
            else:
                raise ValueError('unexpected submission HTTP ' + str(status))
        result['status'] = 'completed_with_exclusions' if result['excluded'] else 'completed'
    except CanonicalAlias as exc:
        result['status'] = 'delegated_to_www'
        result['delegated_to'] = 'www.arquindex.com.br'
        result['reason'] = str(exc)
    except Exception as exc:
        result['status'] = 'blocked'
        result['errors'].append({'stage': result['stage'], 'code': error_code(exc), 'error': str(exc)})
    if result['errors']:
        result['status'] = 'blocked'
    return result, accepted


def main():
    old = json.loads(STATE.read_text()) if STATE.exists() else {}
    updated = dict(old)
    results = []
    hosts = hosts_from_repository()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        tasks = {pool.submit(process_host, host, old.get(host, {})): host for host in hosts}
        for future in concurrent.futures.as_completed(tasks):
            host = tasks[future]
            result, accepted = future.result()
            results.append(result)
            updated[host] = accepted
            print(json.dumps(result, ensure_ascii=False), flush=True)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    temp = STATE.with_suffix('.tmp')
    temp.write_text(json.dumps(updated, ensure_ascii=False), encoding='utf-8')
    temp.replace(STATE)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
              'notice': 'HTTP 200 means received, not crawled or indexed. HTTP 202 means key validation pending.',
              'hosts': sorted(results, key=lambda r: r['host'])}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = ('IndexNow diário: ' + str(len(hosts)) + ' hosts; '
               + str(sum(r['received_200'] for r in results)) + ' URLs recebidas (200); '
               + str(sum(r['pending_202'] for r in results)) + ' pendentes (202); '
               + str(sum(bool(r['errors']) for r in results)) + ' hosts com erros.\n'
               'Recebimento não comprova rastreamento nem indexação. Consulte report.json.\n')
    print(summary)
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as file:
            file.write(summary)
    return 1 if any(r['errors'] for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())
