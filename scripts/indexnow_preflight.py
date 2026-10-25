#!/usr/bin/env python3
"""Read-only IndexNow readiness inventory. Never submits or updates accepted state."""
import concurrent.futures
import json
import os
import socket
import ssl
import urllib.error
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import indexnow_daily as daily

OUT = Path('indexnow-preflight')


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


def check_host(host):
    result = {'host': host, 'status': 'blocked', 'dns': [], 'key': 'unchecked',
              'sitemap': 'unchecked', 'pages_in_sitemap': 0, 'errors': []}
    try:
        result['dns'] = sorted({r[4][0] for r in socket.getaddrinfo(
            host, 443, type=socket.SOCK_STREAM)})
    except Exception as exc:
        result['errors'].append({'stage': 'dns', 'code': error_code(exc),
                                 'error': str(exc)})
        return result
    # Inspect both independently: a missing key must not conceal a broken sitemap.
    for stage, function in [('key', daily.key_for), ('sitemap', daily.discover)]:
        try:
            value = function(host)
            result[stage] = 'ok'
            if stage == 'sitemap':
                result['pages_in_sitemap'] = len(value)
        except Exception as exc:
            result[stage] = 'blocked'
            result['errors'].append({'stage': stage, 'code': error_code(exc),
                                     'error': str(exc)})
    if not result['errors']:
        result['status'] = 'ready_for_page_checks'
    return result


def main():
    hosts = daily.hosts_from_repository()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = sorted(pool.map(check_host, hosts), key=lambda r: r['host'])
    blocked = sum(r['status'] == 'blocked' for r in results)
    counts = Counter((e['stage'], e['code']) for r in results for e in r['errors'])
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
              'mode': 'read_only_preflight', 'submitted': False,
              'accepted_state_changed': False, 'blocked_hosts': blocked,
              'status': 'blocked' if blocked else 'ready_for_page_checks',
              'notice': 'Readiness is not submission, crawling or indexing. '
                        'Repository sitemaps are candidates, not proof of deployed hosts.',
              'hosts': results}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    lines = ['## IndexNow: diagnóstico sem envios', '',
             f'**Estado: {report["status"]}; {blocked}/{len(hosts)} hosts bloqueados.**', '',
             'Nenhuma submissão, alteração de DNS/FTP/fila ou atualização do cache de recebimentos.',
             'Chave e sitemap válidos ainda exigem checagem das páginas antes de qualquer envio.', '',
             '| Etapa | Código | Ocorrências |', '|---|---|---:|']
    lines += [f'| {stage} | {code} | {count} |' for (stage, code), count in sorted(counts.items())]
    lines += ['', '| Host | Estado | Chave | Sitemap | URLs |', '|---|---|---|---|---:|']
    lines += [f'| {r["host"]} | {r["status"]} | {r["key"]} | {r["sitemap"]} | {r["pages_in_sitemap"]} |'
              for r in results]
    summary = '\n'.join(lines) + '\n'
    (OUT / 'report.md').write_text(summary)
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as stream:
            stream.write(summary)
    for result in results:
        print(json.dumps(result, ensure_ascii=False), flush=True)
    print('PREFLIGHT', report['status'], 'BLOCKED', blocked, 'TOTAL', len(hosts), 'SUBMITTED', False)
    # Exit success means the diagnostic completed; health is explicit in its report.
    # The production sender still fails on any host error and is not modified here.


if __name__ == '__main__':
    main()
