import importlib.util
import pathlib
import ssl
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts/publicar-alfresco-automacao.py"
spec = importlib.util.spec_from_file_location("alfresco_safe", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeFTP:
    def __init__(self, **kwargs):
        assert kwargs["context"].verify_mode == ssl.CERT_REQUIRED
        self.calls = []
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def connect(self, host, port): self.calls.append("connect")
    def login(self, user, password): self.calls.append("login")
    def prot_p(self): self.calls.append("prot_p")
    def pwd(self): return "/"
    def cwd(self, path): self.calls.append("cwd")


class TLSFailure(FakeFTP):
    def login(self, user, password):
        raise ssl.SSLCertVerificationError("hostname mismatch")


class LoginFailure(FakeFTP):
    def login(self, user, password):
        raise module.ftplib.error_perm("530 Login authentication failed")


class Denied(FakeFTP):
    def cwd(self, path):
        raise module.ftplib.error_perm("550 Permission denied")


class TestSafePreflight(unittest.TestCase):
    def test_valid_read_only(self):
        result = module.preflight("example.test", "user", "pass", "/public_html", FakeFTP)
        self.assertTrue(result["tls_verified"])
        self.assertFalse(result["backup_restoration_verified"])
    def test_hostname_mismatch(self):
        with self.assertRaises(ssl.SSLCertVerificationError):
            module.preflight("example.test", "user", "pass", "/public_html", TLSFailure)
    def test_auth_530(self):
        with self.assertRaises(module.ftplib.error_perm):
            module.preflight("example.test", "user", "pass", "/public_html", LoginFailure)
    def test_permissions(self):
        with self.assertRaises(module.ftplib.error_perm):
            module.preflight("example.test", "user", "pass", "/public_html", Denied)
    def test_missing_secret(self):
        with self.assertRaises(ValueError):
            module.validate_config("example.test", "user", "", "/public_html")
    def test_unsafe_path(self):
        for path in ("../secret", "/etc/passwd", "x/../../y"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                module.safe_path(path)
    def test_no_deploy_commands(self):
        import inspect
        source = inspect.getsource(module.preflight)
        for token in (".storbinary(", ".mkd(", ".delete(", ".rename("):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
