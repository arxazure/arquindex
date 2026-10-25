#!/usr/bin/env python3
"""Private, append-only FTPS backup chunks. Never writes to a public root."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
import posixpath
import re
import socket
import ssl
import tarfile
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

spec = importlib.util.spec_from_file_location('weekly', Path(__file__).with_name('homehost-weekly-audit-20261023.py'))
weekly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(weekly)
PREFIX = '/seo-backups/resumable'
RUN_RE = re.compile(r'^\d{8}T\d{6}Z-[0-9a-f]{12}$')


def safe_relative(path):
    return (isinstance(path, str) and bool(path) and not path.startswith('/')
            and not any(c in path for c in '\r\n\\\x00')
            and all(p not in ('', '.', '..') for p in path.split('/')))


def safe_name(name):
    if not safe_relative(name) or '/' in name:
        raise ValueError('UNSAFE_FTP_NAME')
    return name


def private_path(run, filename):
    if not RUN_RE.fullmatch(run) or not re.fullmatch(r'(?:chunk-\d{6}-[0-9a-f]{12}\.tar\.gz|checkpoint-\d{6}-[0-9a-f]{12}\.json)', filename):
        raise ValueError('INVALID_BACKUP_PATH')
    return f'{PREFIX}/{run}/{filename}'


def read_json(ftp, path):
    payload = bytearray()
    def receive(block):
        payload.extend(block)
        if len(payload) > 64 * 1024 * 1024:
            raise ValueError('CHECKPOINT_TOO_LARGE')
    ftp.retrbinary('RETR ' + path, receive)
    return json.loads(payload)


def validate_state(state):
    if not isinstance(state, dict) or state.get('schema') != 1 or not RUN_RE.fullmatch(state.get('run', '')):
        raise ValueError('INVALID_CHECKPOINT')
    roots = state.get('roots')
    if not isinstance(roots, list) or not roots or any(not safe_relative(r) or '/' in r or r in weekly.SYSTEM_ROOTS for r in roots):
        raise ValueError('INVALID_ROOTS')
    for key in ('files', 'bytes', 'revision'):
        if type(state.get(key)) is not int or state[key] < 0:
            raise ValueError('INVALID_COUNTER')
    if state['files'] > weekly.MAX_FILES or state['bytes'] > weekly.MAX_BYTES:
        raise ValueError('BACKUP_LIMIT_EXCEEDED')
    if not isinstance(state.get('todo'), list) or not isinstance(state.get('chunks'), list):
        raise ValueError('INVALID_CHECKPOINT_LIST')
    for entry in state['todo']:
        if not isinstance(entry, dict) or not safe_relative(entry.get('path')) or entry['path'].split('/')[0] not in roots or entry.get('type') not in ('dir', 'file'):
            raise ValueError('INVALID_PENDING_PATH')
        if entry['type'] == 'file' and (type(entry.get('size')) is not int or entry['size'] < 0):
            raise ValueError('INVALID_FILE_SIZE')
    expected_files = expected_bytes = 0
    for index, chunk in enumerate(state['chunks'], 1):
        if (not isinstance(chunk, dict) or not isinstance(chunk.get('path'), str) or not re.fullmatch(re.escape(f"{PREFIX}/{state['run']}/chunk-{index:06}-") + r'[0-9a-f]{12}\.tar\.gz', chunk['path'])
                or not re.fullmatch(r'[0-9a-f]{64}', chunk.get('sha256', ''))
                or any(type(chunk.get(k)) is not int or chunk[k] < 0 for k in ('bytes', 'source_bytes', 'files'))):
            raise ValueError('INVALID_CHUNK')
        expected_files += chunk['files']
        expected_bytes += chunk['source_bytes']
    if expected_files != state['files'] or expected_bytes != state['bytes']:
        raise ValueError('CHECKPOINT_TOTAL_MISMATCH')
    if state.get('state') not in ('in_progress', 'complete') or (state['state'] == 'complete' and state['todo']):
        raise ValueError('INVALID_COMPLETION_STATE')
    return state


def verify_remote(ftp, path, size, sha):
    ftp.voidcmd('TYPE I')
    if ftp.size(path) != size:
        raise RuntimeError('REMOTE_SIZE_MISMATCH')
    digest = hashlib.sha256()
    count = 0
    def receive(block):
        nonlocal count
        count += len(block)
        digest.update(block)
    ftp.retrbinary('RETR ' + path, receive)
    if count != size or digest.hexdigest() != sha:
        raise RuntimeError('REMOTE_HASH_MISMATCH')


def upload_verified(ftp, path, stream):
    # MLST may fail for permission reasons too: only an explicit missing-file
    # response is safe. The UUID namespace plus exclusive existence check
    # prevents intentional replacement of checkpoints or prior chunks.
    try:
        ftp.sendcmd('MLST ' + path)
    except ftplib.error_perm as exc:
        if not str(exc).startswith('550'):
            raise
    else:
        raise RuntimeError('DESTINATION_ALREADY_EXISTS')
    stream.seek(0)
    digest = hashlib.sha256()
    size = 0
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        size += len(block)
        digest.update(block)
    stream.seek(0)
    ftp.storbinary('STOR ' + path, stream)
    sha = digest.hexdigest()
    verify_remote(ftp, path, size, sha)
    return {'bytes': size, 'sha256': sha}


def checkpoint(ftp, state):
    validate_state(state)
    state['revision'] += 1
    state['updated_at'] = datetime.now(timezone.utc).isoformat()
    path = private_path(state['run'], f"checkpoint-{state['revision']:06}-{uuid.uuid4().hex[:12]}.json")
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True).encode()
    verified = upload_verified(ftp, path, io.BytesIO(payload))
    print('BACKUP_CHECKPOINT', json.dumps({'path': path, **verified,
          'files': state['files'], 'source_bytes': state['bytes'], 'state': state['state']}), flush=True)
    return path


def expand(ftp, task):
    result = []
    for name, facts in sorted(weekly.mlsd(ftp, task['path']), reverse=True):
        safe_name(name)
        kind = facts.get('type')
        if kind not in ('file', 'dir'):
            raise RuntimeError('UNSUPPORTED_ENTRY_TYPE')
        row = {'path': posixpath.join(task['path'], name), 'type': kind}
        if kind == 'file':
            if not str(facts.get('size', '')).isdigit():
                raise RuntimeError('MISSING_FILE_SIZE')
            row.update(size=int(facts['size']), modify=facts.get('modify'))
        result.append(row)
    return result


def collect_chunk(ftp, state, clock=time.monotonic, max_seconds=1200, max_files=250, max_bytes=64*1024*1024):
    start = clock()
    count = total = 0
    # Never mutate the committed checkpoint until this chunk is fully verified.
    pending = list(state['todo'])
    with tempfile.TemporaryFile() as bundle:
        with tarfile.open(fileobj=bundle, mode='w:gz', compresslevel=1) as archive:
            while pending and count < max_files and total < max_bytes and clock() - start < max_seconds:
                task = pending.pop()
                path = task['path']
                if task['type'] == 'dir':
                    children = expand(ftp, task)
                    info = tarfile.TarInfo(path)
                    info.type = tarfile.DIRTYPE
                    info.mode = 0o755
                    archive.addfile(info)
                    pending.extend(children)
                    continue
                size = task['size']
                if state['files'] + count + 1 > weekly.MAX_FILES or state['bytes'] + total + size > weekly.MAX_BYTES:
                    raise RuntimeError('BACKUP_LIMIT_EXCEEDED')
                with tempfile.SpooledTemporaryFile(max_size=8*1024*1024) as source:
                    actual = 0
                    def receive(block):
                        nonlocal actual
                        actual += len(block)
                        if actual > size:
                            raise RuntimeError('SOURCE_SIZE_CHANGED')
                        source.write(block)
                    ftp.retrbinary('RETR ' + path, receive)
                    if actual != size:
                        raise RuntimeError('SOURCE_SIZE_CHANGED')
                    source.seek(0)
                    info = tarfile.TarInfo(path)
                    info.size = actual
                    info.mode = 0o600
                    archive.addfile(info, source)
                count += 1
                total += actual
        path = private_path(state['run'], f"chunk-{len(state['chunks'])+1:06}-{uuid.uuid4().hex[:12]}.tar.gz")
        verified = upload_verified(ftp, path, bundle)
    state['chunks'].append({'path': path, **verified, 'files': count, 'source_bytes': total})
    state['files'] += count
    state['bytes'] += total
    state['todo'] = pending


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', default='')
    args = parser.parse_args()
    password = os.environ.get('FTP_PASSWORD')
    if not password:
        raise RuntimeError('FTP_PASSWORD_MISSING')
    host = os.environ.get('FTP_TLS_HOST', 'h59.servidorhh.com').strip()
    expected = set(socket.gethostbyname_ex('ftp.arquindex.com.br')[2])
    if not expected.intersection(socket.gethostbyname_ex(host)[2]):
        raise RuntimeError('HOST_IP_MISMATCH')
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    with ftplib.FTP_TLS(timeout=60, context=context) as ftp:
        ftp.connect(host, 21)
        if ftp.sock.getpeername()[0] not in expected:
            raise RuntimeError('SERVER_IP_CHANGED')
        ftp.auth()
        ftp.login(os.environ.get('FTP_USER', 'arquind2'), password)
        ftp.prot_p()
        if args.resume:
            match = re.fullmatch(re.escape(PREFIX) + r'/(\d{8}T\d{6}Z-[0-9a-f]{12})/checkpoint-(\d{6})-[0-9a-f]{12}\.json', args.resume)
            if not match:
                raise ValueError('INVALID_RESUME_PATH')
            state = validate_state(read_json(ftp, args.resume))
            if state['run'] != match[1] or int(match[2]) != state['revision']:
                raise ValueError('CHECKPOINT_PATH_MISMATCH')
            for chunk in state['chunks']:
                verify_remote(ftp, chunk['path'], chunk['bytes'], chunk['sha256'])
        else:
            root_dirs = [n for n, f in weekly.mlsd(ftp, '/') if f.get('type') == 'dir']
            roots = sorted(n for n in root_dirs if n == 'public_html' or
                           (n not in weekly.SYSTEM_ROOTS and not n.startswith('.') and weekly.has_site_signature(ftp, n)))
            state = {'schema': 1, 'run': datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:12],
                     'roots': roots, 'todo': [{'path': r, 'type': 'dir'} for r in reversed(roots)],
                     'chunks': [], 'files': 0, 'bytes': 0, 'revision': 0, 'state': 'in_progress'}
            validate_state(state)
            weekly.ensure_dir(ftp, f"{PREFIX}/{state['run']}")
            checkpoint(ftp, state)
        deadline = time.monotonic() + 40*60
        while state['todo'] and time.monotonic() < deadline:
            collect_chunk(ftp, state)
            checkpoint(ftp, state)
        if not state['todo']:
            # Completion requires full readback of every archived chunk, even
            # when chunks were created in prior jobs.
            for chunk in state['chunks']:
                verify_remote(ftp, chunk['path'], chunk['bytes'], chunk['sha256'])
            state['state'] = 'complete'
            checkpoint(ftp, state)
            print('BACKUP_COMPLETE_VERIFIED', state['run'], flush=True)
        else:
            print('BACKUP_PARTIAL_RESUME_REQUIRED', flush=True)


if __name__ == '__main__':
    main()
