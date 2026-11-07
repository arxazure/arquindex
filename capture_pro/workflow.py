"""Pure, auditable state machine for document production.

No signing code here. It only determines whether a transition is permitted.
The API must also enforce authorization and apply changes transactionally.
"""
from dataclasses import dataclass
from enum import Enum

class Status(str, Enum):
    UPLOADED="uploaded"
    OCR_RUNNING="ocr_running"
    OCR_REVIEW="ocr_review"
    CLASSIFICATION="classification"
    QA_PENDING="qa_pending"
    QA_REJECTED="qa_rejected"
    APPROVED="approved"
    SIGNING="signing"
    SIGNED="signed"
    DELIVERED="delivered"
    FAILED="failed"

TRANSITIONS={
    Status.UPLOADED: {Status.OCR_RUNNING, Status.FAILED},
    Status.OCR_RUNNING: {Status.OCR_REVIEW, Status.FAILED},
    Status.OCR_REVIEW: {Status.CLASSIFICATION, Status.QA_REJECTED},
    Status.CLASSIFICATION: {Status.QA_PENDING, Status.QA_REJECTED},
    Status.QA_PENDING: {Status.QA_REJECTED, Status.APPROVED},
    Status.QA_REJECTED: {Status.OCR_RUNNING, Status.CLASSIFICATION},
    Status.APPROVED: {Status.SIGNING},
    Status.SIGNING: {Status.SIGNED, Status.FAILED},
    Status.SIGNED: {Status.DELIVERED},
    Status.FAILED: {Status.OCR_RUNNING, Status.QA_REJECTED},
}

@dataclass(frozen=True)
class Evidence:
    original_sha256: str = ""
    ocr_sha256: str = ""
    pdfa_compliant: bool = False
    quality_approved: bool = False
    signer_authorized: bool = False
    signature_verified: bool = False
    signed_sha256: str = ""

def is_sha256(s: str) -> bool:
    return len(s)==64 and all(c in "0123456789abcdef" for c in s)

def validate_transition(before: Status, after: Status, evidence: Evidence) -> None:
    if after not in TRANSITIONS.get(before, set()):
        raise ValueError(f"Invalid state transition: {before} -> {after}")
    if after in {Status.OCR_REVIEW,Status.CLASSIFICATION,Status.QA_PENDING,Status.APPROVED,
                 Status.SIGNING,Status.SIGNED,Status.DELIVERED}:
        if not (is_sha256(evidence.original_sha256) and is_sha256(evidence.ocr_sha256)
                and evidence.pdfa_compliant):
            raise ValueError("Verified original, OCR hash and PDF/A required")
    if after in {Status.APPROVED,Status.SIGNING,Status.SIGNED,Status.DELIVERED}:
        if not evidence.quality_approved:
            raise ValueError("Human QA approval required")
    if after in {Status.SIGNING, Status.SIGNED, Status.DELIVERED}:
        if not evidence.signer_authorized:
            raise ValueError("Signer authorization required")
    if after in {Status.SIGNED,Status.DELIVERED}:
        if not (evidence.signature_verified and is_sha256(evidence.signed_sha256)):
            raise ValueError("Verified signed PDF and final SHA-256 required")
