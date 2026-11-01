import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("media", Path(__file__).with_name("verificar-midia-social-http.py"))
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)

class FakeHeaders(dict):
    def get_content_type(self):
        return self["Content-Type"]

class FakeResponse:
    status = 200
    def __init__(self, data, mime):
        self.data = data
        self.headers = FakeHeaders({"Content-Type": mime})
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self, limit):
        return self.data[:limit]

class MediaTests(unittest.TestCase):
    def check(self, mime, data):
        with patch.object(media, "_public_host", return_value=True):
            with patch.object(media.urllib.request, "build_opener") as opener:
                opener.return_value.open.return_value = FakeResponse(data, mime)
                return media.verify_media("https://example.com/test.jpg")

    def test_jpeg(self):
        self.assertTrue(self.check("image/jpeg", bytes.fromhex("ffd8ff") + b"ok")["verified"])

    def test_png(self):
        self.assertTrue(self.check("image/png", bytes.fromhex("89504e470d0a1a0a") + b"ok")["verified"])

    def test_webp(self):
        self.assertTrue(self.check("image/webp", b"RIFF1234WEBPok")["verified"])

    def test_wrong_signature(self):
        with self.assertRaises(ValueError):
            self.check("image/jpeg", b"bad")

    def test_invalid_mime(self):
        with self.assertRaises(ValueError):
            self.check("text/html", b"html")

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.check("image/jpeg", b"")

    def test_insecure_url(self):
        with self.assertRaises(ValueError):
            media.verify_media("http://example.com/image.jpg")

    def test_private_host(self):
        with patch.object(media, "_public_host", return_value=False):
            with self.assertRaises(ValueError):
                media.verify_media("https://example.com/image.jpg")

if __name__ == "__main__":
    unittest.main()
