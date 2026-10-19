import importlib.util
from pathlib import Path
import ssl
import unittest
from unittest.mock import patch, MagicMock

spec = importlib.util.spec_from_file_location(
    "existing_first", Path(__file__).with_name("existing-first-20261018.py"))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class GuardTests(unittest.TestCase):
    def test_connection_requires_verified_certificate_and_encrypted_data(self):
        fake = MagicMock()
        with patch.object(guard, "FTP_HOST", "ftp.example.test"), \
             patch.object(guard, "FTP_USER", "test-user"), \
             patch.object(guard, "FTP_PASSWORD", "placeholder-not-a-secret"), \
             patch.object(guard.ftplib, "FTP_TLS", return_value=fake) as ctor:
            guard.connect()
        ctx = ctor.call_args.kwargs["context"]
        self.assertTrue(ctx.check_hostname)
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
        fake.prot_p.assert_called_once_with()

    def test_missing_credentials_stop_before_connection(self):
        with patch.object(guard, "FTP_PASSWORD", ""), \
             patch.object(guard.ftplib, "FTP_TLS") as ctor:
            with self.assertRaises(RuntimeError):
                guard.connect()
            ctor.assert_not_called()

    def test_valid_patch_is_idempotent(self):
        original = '<html><body><h2>Escolha o serviço para sua necessidade</h2></body></html>'.encode()
        for name in guard.CONTENT:
            modified, changed = guard.patch(name, original)
            self.assertTrue(changed)
            self.assertEqual(guard.patch(name, modified), (modified, False))

    def test_missing_anchor_and_incomplete_html_are_rejected(self):
        for original in [b'<html><body></body></html>', b'<p>not a complete page</p>']:
            with self.assertRaises(RuntimeError):
                guard.patch('guarda_de_documentos.html', original)


if __name__ == '__main__':
    unittest.main()
