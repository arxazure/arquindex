import os
import unittest
from unittest.mock import patch

from scripts.seo_recovery import main, safe_remote_path


class SeoRecoverySafetyTests(unittest.TestCase):
    def test_apply_is_blocked_before_credentials_or_network(self):
        with patch.dict(os.environ, {"APPLY_CHANGES": "true"}, clear=True):
            with self.assertRaisesRegex(SystemExit, "Publicacao bloqueada"):
                main()

    def test_ftp_tls_host_is_required(self):
        with patch.dict(os.environ, {"FTP_PASSWORD": "test", "FTP_USERNAME": "test"}, clear=True):
            with self.assertRaisesRegex(SystemExit, "FTP_TLS_HOST ausente"):
                main()

    def test_sitemap_paths_must_be_safe_relative_paths(self):
        self.assertTrue(safe_remote_path("sitemaps/part.xml"))
        for path in ("../outside.xml", "/absolute.xml", "a//b.xml", "a\\b.xml", "a\nb.xml"):
            with self.subTest(path=path):
                self.assertFalse(safe_remote_path(path))


if __name__ == "__main__":
    unittest.main()
