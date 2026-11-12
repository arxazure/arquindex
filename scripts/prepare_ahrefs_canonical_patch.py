"""Prepare reviewed canonical replacements locally. Never connects to FTP or publishes.

Obtain a fresh source snapshot and validate the full HomeHost backup before deployment.
Usage: python scripts/prepare_ahrefs_canonical_patch.py SOURCE_ROOT OUTPUT_ROOT
"""
import hashlib
import json
import sys
from pathlib import Path
from seo_recovery import Info, patch_canonical


def corrected(raw, record):
    if hashlib.sha256(raw).hexdigest() != record['original_sha256']:
        raise ValueError('Source changed; review again: ' + record['url'])
    text = raw.decode('utf-8')
    before = Info(); before.feed(text)
    if before.canonical != [record['old_canonical']]:
        raise ValueError('Ambiguous canonical: ' + record['url'])
    new, count = patch_canonical(text, record['old_canonical'], record['new_canonical'])
    after = Info(); after.feed(new)
    if count != 1 or after.canonical != [record['new_canonical']]:
        raise ValueError('Unexpected replacement: ' + record['url'])
    return new.encode('utf-8')


def main():
    source, output = map(Path, sys.argv[1:])
    if source.resolve() == output.resolve():
        raise ValueError('Use a separate output directory')
    manifest = Path(__file__).resolve().parents[1] / 'seo/ahrefs-recovery-20261024/manifest.json'
    prepared = []
    for row in json.loads(manifest.read_text()):
        relative = row['source_relative']
        src = source / relative
        if not src.is_file():
            print('MISSING_SOURCE', relative)
            continue
        data = corrected(src.read_bytes(), row)
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        prepared.append(relative)
    print('PREPARED_LOCAL_ONLY', len(prepared))


if __name__ == '__main__':
    main()
