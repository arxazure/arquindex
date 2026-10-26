import copy
import ftplib
import hashlib
import importlib.util
import io
import tarfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('backup', Path(__file__).parents[1] / 'seo-rotinas/homehost-resumable-backup.py')
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


class FTP:
    def __init__(self):
        self.data = {'public_html/index.html': b'home', 'public_html/.htaccess': b'rules',
                     'public_html/empty.txt': b'', 'public_html/sub/page.html': b'page'}
        self.writes = []
        self.corrupt = False

    def mlsd(self, path, facts=None):
        rows = {
            'public_html': [('index.html', {'type': 'file', 'size': '4'}),
                            ('.htaccess', {'type': 'file', 'size': '5'}),
                            ('empty.txt', {'type': 'file', 'size': '0'}),
                            ('sub', {'type': 'dir'}), ('empty-dir', {'type': 'dir'})],
            'public_html/sub': [('page.html', {'type': 'file', 'size': '4'})],
            'public_html/empty-dir': [],
        }
        return iter(rows[path])

    def retrbinary(self, command, receive):
        data = self.data[command.removeprefix('RETR ')]
        receive(data)

    def storbinary(self, command, stream):
        path = command.removeprefix('STOR ')
        if not path.startswith(backup.PREFIX + '/'):
            raise AssertionError('PUBLIC_WRITE')
        self.writes.append(path)
        self.data[path] = stream.read() + (b'corrupt' if self.corrupt else b'')

    def size(self, path):
        return len(self.data[path])

    def voidcmd(self, command):
        return '200'

    def sendcmd(self, command):
        if command.removeprefix('MLST ') not in self.data:
            raise ftplib.error_perm('550 Missing')
        return '250 Exists'


def initial():
    return {'schema': 1, 'run': '20261025T010000Z-abcdef123456', 'roots': ['public_html'],
            'todo': [{'path': 'public_html', 'type': 'dir'}], 'chunks': [],
            'files': 0, 'bytes': 0, 'revision': 0, 'state': 'in_progress'}


class BackupTests(unittest.TestCase):
    def test_chunks_resume_without_losing_hidden_empty_or_nested_files(self):
        ftp = FTP()
        state = initial()
        backup.collect_chunk(ftp, state, max_files=2)
        path = backup.checkpoint(ftp, state)
        restored = backup.validate_state(backup.read_json(ftp, path))
        while restored['todo']:
            backup.collect_chunk(ftp, restored, max_files=2)
        self.assertEqual(restored['files'], 4)
        self.assertEqual(restored['bytes'], 13)
        members = {}
        for chunk in restored['chunks']:
            backup.verify_remote(ftp, chunk['path'], chunk['bytes'], chunk['sha256'])
            with tarfile.open(fileobj=io.BytesIO(ftp.data[chunk['path']]), mode='r:gz') as archive:
                for info in archive:
                    if info.isfile():
                        self.assertNotIn(info.name, members)
                        members[info.name] = archive.extractfile(info).read()
                    elif info.name == 'public_html/empty-dir':
                        self.assertTrue(info.isdir())
        self.assertEqual(members, {k: v for k, v in ftp.data.items() if k.startswith('public_html/')})
        self.assertTrue(all(p.startswith(backup.PREFIX + '/') for p in ftp.writes))

    def test_interrupted_chunk_does_not_advance_checkpoint_or_overwrite_orphan(self):
        ftp = FTP()
        state = initial()
        old = copy.deepcopy(state)
        ftp.corrupt = True
        with self.assertRaisesRegex(RuntimeError, 'REMOTE_SIZE_MISMATCH'):
            backup.collect_chunk(ftp, state, max_files=1)
        self.assertEqual(state, old)
        orphan = ftp.writes[-1]
        ftp.corrupt = False
        backup.collect_chunk(ftp, state, max_files=1)
        self.assertNotEqual(state['chunks'][0]['path'], orphan)
        self.assertIn(orphan, ftp.data)

    def test_hash_mismatch_fails_even_when_size_matches(self):
        ftp = FTP()
        path = backup.private_path(initial()['run'], 'chunk-000001-abcdef123456.tar.gz')
        ftp.data[path] = b'abcd'
        with self.assertRaisesRegex(RuntimeError, 'REMOTE_HASH_MISMATCH'):
            backup.verify_remote(ftp, path, 4, hashlib.sha256(b'efgh').hexdigest())

    def test_empty_file_becoming_nonempty_fails_without_checkpoint_progress(self):
        ftp = FTP()
        state = initial()
        state['todo'] = [{'path': 'public_html/empty.txt', 'type': 'file', 'size': 0}]
        old = copy.deepcopy(state)
        ftp.data['public_html/empty.txt'] = b'changed'
        with self.assertRaisesRegex(RuntimeError, 'SOURCE_SIZE_CHANGED'):
            backup.collect_chunk(ftp, state)
        self.assertEqual(state, old)

    def test_unsafe_names_unsupported_entries_and_forged_checkpoints_fail(self):
        for name in ['../outside', '/absolute', 'file\r\nDELE index.html', 'a/b', 'a\\b']:
            with self.assertRaises(ValueError):
                backup.safe_name(name)
        for mutate in [lambda s: s.update(roots=['../public_html']),
                       lambda s: s.update(todo=[{'path': 'mail/inbox', 'type': 'dir'}]),
                       lambda s: s.update(files=1),
                       lambda s: s.update(state='complete'),
                       lambda s: s.update(chunks=[{'path': '/public_html/copy.tar.gz'}])]:
            state = initial()
            mutate(state)
            with self.assertRaises(ValueError):
                backup.validate_state(state)
        ftp = FTP()
        ftp.mlsd = lambda *a, **k: iter([('link', {'type': 'OS.unix=slink'})])
        with self.assertRaisesRegex(RuntimeError, 'UNSUPPORTED_ENTRY_TYPE'):
            backup.expand(ftp, {'path': 'public_html'})

    def test_existing_destinations_and_counter_limits_fail_closed(self):
        ftp = FTP()
        path = backup.private_path(initial()['run'], 'checkpoint-000001-abcdef123456.json')
        ftp.data[path] = b'prior'
        with self.assertRaisesRegex(RuntimeError, 'DESTINATION_ALREADY_EXISTS'):
            backup.upload_verified(ftp, path, io.BytesIO(b'new'))
        self.assertEqual(ftp.data[path], b'prior')
        state = initial()
        state['todo'] = [{'path': 'public_html/index.html', 'type': 'file', 'size': backup.weekly.MAX_BYTES + 1}]
        with self.assertRaisesRegex(RuntimeError, 'BACKUP_LIMIT_EXCEEDED'):
            backup.collect_chunk(ftp, state)
        self.assertEqual(state['files'], 0)


if __name__ == '__main__':
    unittest.main()
