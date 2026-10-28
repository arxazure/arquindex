#!/usr/bin/env python3
"""Read-only local sitemap inventory preflight, without HTTP calls or submissions."""
import argparse
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

SKIP = {'.git', 'node_modules', '.next', 'dist', 'build', 'vendor'}
def inspect(path):
    result = {'file': str(path), 'urls': 0, 'issues': [], 'hosts': []}
    try:
        root = ET.parse(path).getroot()
        kind = root.tag.rsplit('}', 1)[-1]
        if kind not in ('urlset', 'sitemapindex'):
            result['issues'].append('invalid_root')
            return result
        hosts, seen = set(), set()
        for node in root.iter():
            if node.tag.rsplit('}', 1)[-1] != 'loc':
                continue
            value = (node.text or '').strip()
            result['urls'] += 1
            parsed = urlsplit(value)
            if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
                result['issues'].append('invalid_absolute_https_loc')
            if value in seen:
                result['issues'].append('duplicate_loc')
            seen.add(value)
            if parsed.hostname:
                hosts.add(parsed.hostname.lower())
                if parsed.hostname != 'arquindex.com.br' and not parsed.hostname.endswith('.arquindex.com.br'):
                    result['issues'].append('outside_arq_domain')
        result['hosts'] = sorted(hosts)
        if result['urls'] > 50000:
            result['issues'].append('sitemap_over_50000_urls')
    except (ET.ParseError, OSError, ValueError) as exc:
        result['issues'].append('invalid_xml_or_file: ' + str(exc))
    result['issues'] = sorted(set(result['issues']))
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--out', default='seo-report/sitemap-preflight.json')
    args = parser.parse_args()
    files = sorted(p for p in Path(args.root).rglob('sitemap*.xml')
                   if not any(part in SKIP for part in p.parts))
    results = [inspect(p) for p in files]
    summary = dict(Counter(issue for item in results for issue in item['issues']))
    report = {'scope': 'repository_sitemaps_only', 'files_scanned': len(files),
              'issues': summary, 'inventories': results,
              'limitations': ['No live DNS, HTTP, robots, canonical, indexing or search ranking validation.',
                              'Sitemap index URLs may refer to other hosts intentionally; review before correction.']}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files_scanned': len(files), 'issues': summary}, ensure_ascii=False))
if __name__ == '__main__':
    main()
