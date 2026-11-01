#!/usr/bin/env python3
"""Testes offline do bloqueio de postagens sem imagem."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("image_validator", Path(__file__).with_name("validar-postagem-com-imagem.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestMediaGate(unittest.TestCase):
    def setUp(self):
        self.post = {
            "channel": "instagram",
            "title": "Dossies RH",
            "body": "Documentos organizados com seguranca.",
            "media": "https://midia.arquindex-capture.stream/r2/arte-rh.jpg",
        }

    def test_valid_image(self):
        self.assertEqual(module.validate(self.post), [])

    def test_missing_image(self):
        self.post.pop("media")
        self.assertIn("MISSING_IMAGE", module.validate(self.post))

    def test_http_not_allowed(self):
        self.post["media"] = "http://example.com/arte.jpg"
        self.assertIn("INVALID_IMAGE_URL", module.validate(self.post))

    def test_unsupported_format(self):
        self.post["media"] = "https://example.com/arte.pdf"
        self.assertIn("UNSUPPORTED_IMAGE_FORMAT", module.validate(self.post))

    def test_unknown_status_not_retried(self):
        self.post["state"] = "unknown"
        self.assertIn("REQUIRES_REMOTE_STATUS_RECONCILIATION", module.validate(self.post))

    def test_accepted_not_retried(self):
        self.post["state"] = "accepted"
        self.assertIn("REQUIRES_REMOTE_STATUS_RECONCILIATION", module.validate(self.post))

if __name__ == "__main__":
    unittest.main()
