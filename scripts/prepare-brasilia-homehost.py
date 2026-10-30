#!/usr/bin/env python3
"""Prepare a minimal diff from an authenticated HomeHost export. Never deploys."""
import argparse
import hashlib
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / 'staging/seo/brasilia-20261029/homehost-patches.json'

class Structure(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonicals = []; self.h1 = 0; self.body = 0; self.blocks = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split(): self.canonicals.append(attrs.get('href'))
        if tag == 'h1': self.h1 += 1
        if tag == 'body': self.body += 1
        if attrs.get('id') == 'arquindex-brasilia-20261029': self.blocks += 1

def prepare(raw, spec, expected_sha256, anchor='</main>'):
    if hashlib.sha256(raw).hexdigest() != expected_sha256: raise ValueError('SOURCE_HASH_MISMATCH')
    text = raw.decode('utf-8', errors='strict')
    before = Structure(); before.feed(text)
    if before.body != 1 or before.h1 != 1 or before.canonicals != [spec['canonical']] or before.blocks:
        raise ValueError('SOURCE_STRUCTURE_OR_CANONICAL_MISMATCH')
    if text.count(anchor) != 1 or text.index(anchor) < text.lower().index('<body') or text.index(anchor) >= text.lower().rfind('</body>'):
        raise ValueError('REQUIRE_UNIQUE_BODY_ANCHOR')
    # Preserve H1, canonical, scripts, analytics, assets and every existing URL.
    result, count = re.subn(r'<title\b[^>]*>.*?</title\s*>', '<title>'+escape(spec['title'])+'</title>', text, flags=re.I|re.S)
    if count != 1: raise ValueError('REQUIRE_ONE_TITLE')
    pattern = r'<meta\b(?=[^>]*\bname\s*=\s*[\"\']description[\"\'])[^>]*>'
    result, count = re.subn(pattern, '<meta name="description" content="'+escape(spec['description'], quote=True)+'">', result, flags=re.I)
    if count != 1: raise ValueError('REQUIRE_ONE_DESCRIPTION')
    result = result.replace(anchor, spec['block']+'\n'+anchor, 1)
    after = Structure(); after.feed(result)
    if after.h1 != before.h1 or after.canonicals != before.canonicals or after.blocks != 1: raise ValueError('REGRESSION')
    return result.encode('utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page', required=True, choices=json.loads(POLICY.read_text()))
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--anchor', default='</main>')
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve(): parser.error('Output must differ from source')
    try: result = prepare(args.input.read_bytes(), json.loads(POLICY.read_text())[args.page], args.sha256, args.anchor)
    except (ValueError, UnicodeError) as error: parser.error(str(error))
    with args.output.open('xb') as output: output.write(result)
    print(json.dumps({'state':'staged_only','page':args.page,'before_sha256':args.sha256,'after_sha256':hashlib.sha256(result).hexdigest(),'publication':'not_performed'}))
if __name__ == '__main__': main()
