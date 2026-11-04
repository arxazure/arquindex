import unittest
from uuid import uuid4
from capture_pro.storage import object_key

class StorageKeyTests(unittest.TestCase):
    def test_namespaced(self):
        doc=str(uuid4())
        self.assertEqual(object_key("cliente_1",doc,2,"ocr"),f"tenants/cliente_1/documents/{doc}/v2/ocr.pdf")
    def test_reject_path_escape(self):
        with self.assertRaises(ValueError):
            object_key("../another",str(uuid4()),1,"original")
    def test_reject_type(self):
        with self.assertRaises(ValueError):
            object_key("cliente_1",str(uuid4()),1,"../../signed")
if __name__=="__main__":
    unittest.main()
