from importlib import import_module
from typing import Any, cast

from app.constants import KEM_ALGORITHM, SIGNATURE_ALGORITHM


def _oqs() -> Any:
    try:
        return cast(Any, import_module("oqs"))
    except Exception as exc:
        raise RuntimeError(
            "liboqs-python could not be loaded. Install liboqs-python and its build prerequisites."
        ) from exc


def kem_available() -> bool:
    try:
        oqs = _oqs()
        return KEM_ALGORITHM in oqs.get_enabled_kem_mechanisms()
    except Exception:
        return False


def signature_available() -> bool:
    try:
        oqs = _oqs()
        return SIGNATURE_ALGORITHM in oqs.get_enabled_sig_mechanisms()
    except Exception:
        return False


def generate_kem_keypair() -> tuple[bytes, bytes]:
    oqs = _oqs()
    if KEM_ALGORITHM not in oqs.get_enabled_kem_mechanisms():
        raise RuntimeError(f"{KEM_ALGORITHM} is not enabled in liboqs.")
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
        return public_key, secret_key


def encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
    oqs = _oqs()
    with oqs.KeyEncapsulation(KEM_ALGORITHM) as kem:
        ciphertext, shared_secret = kem.encap_secret(public_key)
        return ciphertext, shared_secret


def decapsulate(secret_key: bytes, ciphertext: bytes) -> bytes:
    oqs = _oqs()
    with oqs.KeyEncapsulation(KEM_ALGORITHM, secret_key) as kem:
        return kem.decap_secret(ciphertext)


def generate_signature_keypair() -> tuple[bytes, bytes]:
    oqs = _oqs()
    if SIGNATURE_ALGORITHM not in oqs.get_enabled_sig_mechanisms():
        raise RuntimeError(f"{SIGNATURE_ALGORITHM} is not enabled in liboqs.")
    with oqs.Signature(SIGNATURE_ALGORITHM) as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
        return public_key, secret_key


def sign(secret_key: bytes, data: bytes) -> bytes:
    oqs = _oqs()
    with oqs.Signature(SIGNATURE_ALGORITHM, secret_key) as signer:
        return signer.sign(data)


def verify(public_key: bytes, data: bytes, signature: bytes) -> bool:
    oqs = _oqs()
    with oqs.Signature(SIGNATURE_ALGORITHM) as verifier:
        return bool(verifier.verify(data, signature, public_key))