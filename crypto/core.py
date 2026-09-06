import os
import base64
import hashlib
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

ARGON_TIME = 3
ARGON_MEMORY = 65536
ARGON_PARALLELISM = 4

def b64e(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")

def b64d(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"), validate=True)

def derive_password_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Password must not be empty.")
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON_TIME,
        memory_cost=ARGON_MEMORY,
        parallelism=ARGON_PARALLELISM,
        hash_len=32,
        type=Type.ID,
    )

def derive_shared_key(shared_secret: bytes, salt: bytes, info: bytes) -> bytes:
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info).derive(shared_secret)

def aes_encrypt(key: bytes, plaintext: bytes, aad: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return nonce, ciphertext

def aes_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> bytes:
    return AESGCM(key).decrypt(nonce, ciphertext, aad)

def fingerprint(data: bytes) -> str:
    digest = hashlib.sha256(data).hexdigest().upper()
    return ":".join(digest[i:i+4] for i in range(0, len(digest), 4))
