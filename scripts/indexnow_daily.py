#!/usr/bin/env python3
"""Notify IndexNow of changed public Arquindex pages; never claim indexing."""
import concurrent.futures
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = 'https://api.indexnow.org/indexnow'
STATE = Path('.indexnow-state/accepted.json')
REPORT = Path('indexnow-report/report.json')
MAX_BYTES = 8 * 1024 * 1024
MAX_URLS = 25000
KEY_RE = re.compile(r'[A-Za-z0-9-]{8,128}')


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
              'received_200': 0, 'pending_202': 0, 'errors': [], 'batches': []}
    accepted = dict(old)
    try:
        key, location = key_for(host)
        pages = discover(host)
        changed = {}
        for url in pages:
            try:
                status, body, _ = request(url)
                if status != 200:
                    raise ValueError('page not HTTP 200')
                digest = hashlib.sha256(body).hexdigest()
                result['checked'] += 1
                if old.get(url) == digest:
                    result['unchanged'] += 1
                else:
                    changed[url] = digest
            except Exception as exc:
                result['errors'].append({'url': url, 'error': str(exc)})
        result['changed'] = len(changed)
        urls = sorted(changed)
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
    except Exception as exc:
        result['errors'].append({'error': str(exc)})
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
