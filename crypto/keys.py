import json
import os
from pathlib import Path
from typing import Mapping, cast

from app.constants import CIPHER_ALGORITHM, KDF_ALGORITHM, KEM_ALGORITHM, SIGNATURE_ALGORITHM
from crypto import pq
from crypto.core import aes_decrypt, aes_encrypt, b64d, b64e, derive_password_key, fingerprint

KEY_AAD = b"QSEC-PRIVATE-KEY-V1"
KeyPayload = dict[str, object]


def _legacy_file_encryption_key() -> bytes:
    key_b64 = os.environ.get("QSEC_FILE_KEY", "")
    if not key_b64:
        raise ValueError("Missing QSEC_FILE_KEY required to read this legacy encrypted key file.")
    key = b64d(key_b64)
    if len(key) != 32:
        raise ValueError("QSEC_FILE_KEY must decode to 32 bytes.")
    return key


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    serialized = json.dumps(payload, indent=2, ensure_ascii=False)
    path.write_text(serialized, encoding="utf-8")


def _read_json(path: str | Path) -> KeyPayload:
    text = Path(path).read_text(encoding="utf-8")
    raw: object = json.loads(text)
    if not isinstance(raw, dict):
        raise ValueError("Invalid key file format.")
    if raw.get("format") == "QSEC-ENCRYPTED-FILE" and raw.get("version") == 1:
        nonce = b64d(_require_str(cast(Mapping[str, object], raw), "nonce"))
        ciphertext = b64d(_require_str(cast(Mapping[str, object], raw), "ciphertext"))
        file_key = _legacy_file_encryption_key()
        plaintext = aes_decrypt(file_key, nonce, ciphertext, KEY_AAD)
        inner: object = json.loads(plaintext.decode("utf-8"))
        if not isinstance(inner, dict):
            raise ValueError("Invalid decrypted key file format.")
        return cast(KeyPayload, inner)
    return cast(KeyPayload, raw)


def _require_str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Invalid or missing key field: {key}")
    return value


def protect_secret(secret_key: bytes, password: str, key_type: str, algorithm: str) -> KeyPayload:
    salt = os.urandom(16)
    key = derive_password_key(password, salt)
    nonce, ciphertext = aes_encrypt(key, secret_key, KEY_AAD)
    return {
        "format": "QSEC-PRIVATE-KEY",
        "version": 1,
        "type": key_type,
        "algorithm": algorithm,
        "cipher": CIPHER_ALGORITHM,
        "kdf": KDF_ALGORITHM,
        "argon2id": {
            "time_cost": 3,
            "memory_cost_kib": 65536,
            "parallelism": 4,
        },
        "salt": b64e(salt),
        "nonce": b64e(nonce),
        "encrypted_key": b64e(ciphertext),
    }


def unprotect_secret(payload: Mapping[str, object], password: str) -> bytes:
    if payload.get("format") != "QSEC-PRIVATE-KEY" or payload.get("version") != 1:
        raise ValueError("Unsupported private key format.")

    salt = b64d(_require_str(payload, "salt"))
    nonce = b64d(_require_str(payload, "nonce"))
    encrypted_key = b64d(_require_str(payload, "encrypted_key"))
    key = derive_password_key(password, salt)
    return aes_decrypt(key, nonce, encrypted_key, KEY_AAD)


def create_kem_keypair(folder: str, name: str, password: str) -> tuple[Path, Path, str]:
    public_key, secret_key = pq.generate_kem_keypair()
    target = Path(folder)
    target.mkdir(parents=True, exist_ok=True)
    pub_path = target / f"{name}.qpub"
    priv_path = target / f"{name}.qkey"
    fp = fingerprint(public_key)
    _write_json(pub_path, {
        "format": "QSEC-PUBLIC-KEY",
        "version": 1,
        "type": "KEM",
        "algorithm": KEM_ALGORITHM,
        "fingerprint": fp,
        "public_key": b64e(public_key),
    })
    _write_json(priv_path, protect_secret(secret_key, password, "KEM", KEM_ALGORITHM))
    return pub_path, priv_path, fp


def create_signature_keypair(folder: str, name: str, password: str) -> tuple[Path, Path, str]:
    public_key, secret_key = pq.generate_signature_keypair()
    target = Path(folder)
    target.mkdir(parents=True, exist_ok=True)
    pub_path = target / f"{name}.qsigpub"
    priv_path = target / f"{name}.qsigkey"
    fp = fingerprint(public_key)
    _write_json(pub_path, {
        "format": "QSEC-PUBLIC-KEY",
        "version": 1,
        "type": "SIGNATURE",
        "algorithm": SIGNATURE_ALGORITHM,
        "fingerprint": fp,
        "public_key": b64e(public_key),
    })
    _write_json(priv_path, protect_secret(secret_key, password, "SIGNATURE", SIGNATURE_ALGORITHM))
    return pub_path, priv_path, fp


def load_public_key(path: str | Path, expected_type: str, expected_algorithm: str) -> bytes:
    payload = _read_json(path)
    if payload.get("format") != "QSEC-PUBLIC-KEY":
        raise ValueError("Invalid public key file.")
    if payload.get("type") != expected_type or payload.get("algorithm") != expected_algorithm:
        raise ValueError("Wrong key type or algorithm.")
    return b64d(_require_str(payload, "public_key"))


def load_private_key(path: str | Path, password: str, expected_type: str, expected_algorithm: str) -> bytes:
    payload = _read_json(path)
    if payload.get("type") != expected_type or payload.get("algorithm") != expected_algorithm:
        raise ValueError("Wrong private key type or algorithm.")
    return unprotect_secret(payload, password)
