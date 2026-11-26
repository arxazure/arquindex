import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from prepare_ahrefs_canonical_patch import corrected


class CanonicalPatchTest(unittest.TestCase):
    def record(self, raw):
        return {'url': 'https://site.arquindex.com.br/cidade.html',
                'old_canonical': 'https://www.arquindex.com.br/site.arquindex.com.br/cidade.html',
                'new_canonical': 'https://site.arquindex.com.br/cidade.html',
                'original_sha256': hashlib.sha256(raw).hexdigest()}

    def test_preserves_content_line_endings_and_other_links(self):
        old = self.record(b'')['old_canonical'].encode()
        raw = b'<head>\r\n<link href="' + old + b'" rel="canonical"></head><a href="' + old + b'">Conteudo</a>'
        result = corrected(raw, self.record(raw))
        self.assertEqual(result, raw.replace(old, self.record(raw)['new_canonical'].encode(), 1))

    def test_refuses_changed_source(self):
        with self.assertRaisesRegex(ValueError, 'Source changed'):
            corrected(b'changed', self.record(b'original'))

    def test_refuses_multiple_canonicals(self):
        old = self.record(b'')['old_canonical'].encode()
        raw = (b'<link rel="canonical" href="' + old + b'">') * 2
        with self.assertRaisesRegex(ValueError, 'Ambiguous'):
            corrected(raw, self.record(raw))


if __name__ == '__main__':
    unittest.main()
