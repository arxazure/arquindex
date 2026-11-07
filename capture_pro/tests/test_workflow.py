import unittest
from capture_pro.workflow import Status, Evidence, validate_transition

H="a"*64
class WorkflowTests(unittest.TestCase):
    def test_cannot_sign_without_qa(self):
        with self.assertRaises(ValueError):
            validate_transition(Status.APPROVED,Status.SIGNING,Evidence(H,H,True,False,True))
    def test_cannot_bypass_ocr(self):
        with self.assertRaises(ValueError):
            validate_transition(Status.UPLOADED,Status.APPROVED,Evidence(H,H,True,True,True))
    def test_valid_signing(self):
        validate_transition(Status.APPROVED,Status.SIGNING,Evidence(H,H,True,True,True))
    def test_signed_needs_verification(self):
        with self.assertRaises(ValueError):
            validate_transition(Status.SIGNING,Status.SIGNED,Evidence(H,H,True,True,True,False,""))
    def test_signed_and_verified(self):
        validate_transition(Status.SIGNING,Status.SIGNED,Evidence(H,H,True,True,True,True,H))
    def test_cannot_deliver_unapproved(self):
        with self.assertRaises(ValueError):
            validate_transition(Status.SIGNED,Status.DELIVERED,Evidence(H,H,True,False,True,True,H))

if __name__=="__main__":
    unittest.main()
