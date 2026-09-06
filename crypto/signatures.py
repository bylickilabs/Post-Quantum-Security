import json
from pathlib import Path
from typing import TypedDict, cast

from app.constants import SIGNATURE_ALGORITHM
from crypto.core import b64e, b64d
from crypto.keys import load_public_key, load_private_key
from crypto import pq


class SignaturePayload(TypedDict):
    format: str
    version: int
    algorithm: str
    file: str
    signature: str


def sign_file(input_path: str, private_key_path: str, password: str, signature_path: str) -> None:
    data = Path(input_path).read_bytes()
    secret_key = load_private_key(private_key_path, password, "SIGNATURE", SIGNATURE_ALGORITHM)
    signature = pq.sign(secret_key, data)
    payload: SignaturePayload = {
        "format": "QSEC-SIGNATURE",
        "version": 1,
        "algorithm": SIGNATURE_ALGORITHM,
        "file": Path(input_path).name,
        "signature": b64e(signature),
    }
    Path(signature_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def verify_file(input_path: str, public_key_path: str, signature_path: str) -> bool:
    data = Path(input_path).read_bytes()
    public_key = load_public_key(public_key_path, "SIGNATURE", SIGNATURE_ALGORITHM)
    raw_payload = json.loads(Path(signature_path).read_text(encoding="utf-8"))
    if not isinstance(raw_payload, dict):
        raise ValueError("Unsupported signature format.")
    payload = cast(dict[str, object], raw_payload)
    if payload.get("format") != "QSEC-SIGNATURE" or payload.get("algorithm") != SIGNATURE_ALGORITHM:
        raise ValueError("Unsupported signature format.")
    signature = payload.get("signature")
    if not isinstance(signature, str):
        raise ValueError("Invalid signature payload.")
    return pq.verify(public_key, data, b64d(signature))
