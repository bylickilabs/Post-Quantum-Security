import base64
import json
import os
from pathlib import Path
from typing import TypeAlias, cast

from app.constants import CIPHER_ALGORITHM, KEM_ALGORITHM, QSEC_MAGIC, QSEC_VERSION
from crypto import pq
from crypto.core import aes_decrypt, aes_encrypt, b64d, b64e, derive_password_key, derive_shared_key
from crypto.keys import load_private_key, load_public_key

Metadata: TypeAlias = dict[str, str]
EnvelopeValue: TypeAlias = str | int | Metadata
Envelope: TypeAlias = dict[str, EnvelopeValue]

AAD_PASSWORD = b"QSEC1|PASSWORD|AES-256-GCM"
AAD_PQ = b"QSEC1|ML-KEM-768|AES-256-GCM"
TEXT_PREFIX = "QSEC1:"


def _pack(envelope: Envelope) -> bytes:
    return json.dumps(envelope, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _unpack(data: bytes) -> Envelope:
    raw = cast(object, json.loads(data.decode("utf-8")))
    if not isinstance(raw, dict):
        raise ValueError("Invalid QSEC container.")

    obj = cast(Envelope, raw)
    if obj.get("magic") != QSEC_MAGIC or obj.get("version") != QSEC_VERSION:
        raise ValueError("Unsupported or invalid QSEC container.")
    return obj


def _require_str(obj: Envelope, key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str):
        raise ValueError(f"Invalid QSEC container field: {key}.")
    return value


def _metadata(obj: Envelope) -> Metadata:
    value = obj.get("metadata")
    if not isinstance(value, dict):
        return {}
    if not all(isinstance(key, str) and isinstance(item, str) for key, item in value.items()):
        raise ValueError("Invalid QSEC container metadata.")
    return value


def encrypt_password(data: bytes, password: str, metadata: Metadata | None = None) -> bytes:
    salt = os.urandom(16)
    key = derive_password_key(password, salt)
    nonce, ciphertext = aes_encrypt(key, data, AAD_PASSWORD)
    return _pack({
        "magic": QSEC_MAGIC,
        "version": QSEC_VERSION,
        "mode": "password",
        "cipher": CIPHER_ALGORITHM,
        "kdf": "Argon2id",
        "salt": b64e(salt),
        "nonce": b64e(nonce),
        "payload": b64e(ciphertext),
        "metadata": metadata or {},
    })


def decrypt_password(container: bytes, password: str) -> tuple[bytes, Metadata]:
    obj = _unpack(container)
    if obj.get("mode") != "password":
        raise ValueError("This QSEC container requires Post-Quantum decryption.")

    salt = b64d(_require_str(obj, "salt"))
    nonce = b64d(_require_str(obj, "nonce"))
    payload = b64d(_require_str(obj, "payload"))
    key = derive_password_key(password, salt)
    data = aes_decrypt(key, nonce, payload, AAD_PASSWORD)
    return data, _metadata(obj)


def encrypt_pq(data: bytes, public_key_path: str, metadata: Metadata | None = None) -> bytes:
    public_key = load_public_key(public_key_path, "KEM", KEM_ALGORITHM)
    kem_ciphertext, shared_secret = pq.encapsulate(public_key)
    salt = os.urandom(16)
    key = derive_shared_key(shared_secret, salt, b"QSEC1/ML-KEM-768")
    nonce, ciphertext = aes_encrypt(key, data, AAD_PQ)
    return _pack({
        "magic": QSEC_MAGIC,
        "version": QSEC_VERSION,
        "mode": "post-quantum",
        "cipher": CIPHER_ALGORITHM,
        "kem": KEM_ALGORITHM,
        "kdf": "HKDF-SHA256",
        "salt": b64e(salt),
        "nonce": b64e(nonce),
        "kem_ciphertext": b64e(kem_ciphertext),
        "payload": b64e(ciphertext),
        "metadata": metadata or {},
    })


def decrypt_pq(container: bytes, private_key_path: str, password: str) -> tuple[bytes, Metadata]:
    obj = _unpack(container)
    if obj.get("mode") != "post-quantum" or obj.get("kem") != KEM_ALGORITHM:
        raise ValueError("This is not a supported ML-KEM QSEC container.")

    secret_key = load_private_key(private_key_path, password, "KEM", KEM_ALGORITHM)
    kem_ciphertext = b64d(_require_str(obj, "kem_ciphertext"))
    salt = b64d(_require_str(obj, "salt"))
    nonce = b64d(_require_str(obj, "nonce"))
    payload = b64d(_require_str(obj, "payload"))
    shared_secret = pq.decapsulate(secret_key, kem_ciphertext)
    key = derive_shared_key(shared_secret, salt, b"QSEC1/ML-KEM-768")
    data = aes_decrypt(key, nonce, payload, AAD_PQ)
    return data, _metadata(obj)


def encode_text(container: bytes) -> str:
    return TEXT_PREFIX + base64.urlsafe_b64encode(container).decode("ascii")


def decode_text(text: str) -> bytes:
    clean = text.strip()
    if not clean.startswith(TEXT_PREFIX):
        raise ValueError("Encrypted text must start with QSEC1:.")
    return base64.urlsafe_b64decode(clean[len(TEXT_PREFIX):].encode("ascii"))


def encrypt_text_password(text: str, password: str) -> str:
    metadata: Metadata = {"content": "text", "encoding": "utf-8"}
    return encode_text(encrypt_password(text.encode("utf-8"), password, metadata))


def decrypt_text_password(text: str, password: str) -> str:
    raw, _metadata_value = decrypt_password(decode_text(text), password)
    return raw.decode("utf-8")


def encrypt_text_pq(text: str, public_key_path: str) -> str:
    metadata: Metadata = {"content": "text", "encoding": "utf-8"}
    return encode_text(encrypt_pq(text.encode("utf-8"), public_key_path, metadata))


def decrypt_text_pq(text: str, private_key_path: str, password: str) -> str:
    raw, _metadata_value = decrypt_pq(decode_text(text), private_key_path, password)
    return raw.decode("utf-8")


def encrypt_file_password(input_path: str, output_path: str, password: str) -> None:
    source = Path(input_path)
    payload = source.read_bytes()
    container = encrypt_password(payload, password, {"content": "file"})
    Path(output_path).write_bytes(container)


def decrypt_file_password(input_path: str, output_path: str, password: str) -> None:
    payload, _metadata_value = decrypt_password(Path(input_path).read_bytes(), password)
    Path(output_path).write_bytes(payload)


def encrypt_file_pq(input_path: str, output_path: str, public_key_path: str) -> None:
    source = Path(input_path)
    payload = source.read_bytes()
    container = encrypt_pq(payload, public_key_path, {"content": "file"})
    Path(output_path).write_bytes(container)


def decrypt_file_pq(input_path: str, output_path: str, private_key_path: str, password: str) -> None:
    payload, _metadata_value = decrypt_pq(Path(input_path).read_bytes(), private_key_path, password)
    Path(output_path).write_bytes(payload)
