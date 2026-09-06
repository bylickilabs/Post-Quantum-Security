from __future__ import annotations

import tempfile
from pathlib import Path

from cryptography.exceptions import InvalidTag

from app.constants import KEM_ALGORITHM, SIGNATURE_ALGORITHM
from crypto import pq
from crypto.container import (
    decrypt_password,
    decrypt_pq,
    decrypt_text_password,
    decrypt_text_pq,
    encrypt_password,
    encrypt_pq,
    encrypt_text_password,
    encrypt_text_pq,
)
from crypto.core import aes_decrypt, aes_encrypt
from crypto.keys import (
    create_kem_keypair,
    create_signature_keypair,
    load_private_key,
)
from crypto.signatures import sign_file, verify_file


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_failure(function, *args) -> None:
    try:
        function(*args)
    except Exception:
        return
    raise AssertionError(f"Expected failure from {function.__name__}.")


def test_aes_gcm() -> None:
    key = bytes(range(32))
    plaintext = b"BylickiLabs PQS AES-256-GCM CI self-test"
    aad = b"PQS-CI"
    nonce, ciphertext = aes_encrypt(key, plaintext, aad)
    check(len(nonce) == 12, "AES-GCM nonce must be 12 bytes.")
    check(aes_decrypt(key, nonce, ciphertext, aad) == plaintext, "AES-GCM roundtrip failed.")

    tampered = bytearray(ciphertext)
    tampered[-1] ^= 0x01
    try:
        aes_decrypt(key, nonce, bytes(tampered), aad)
    except InvalidTag:
        pass
    else:
        raise AssertionError("Tampered AES-GCM ciphertext was accepted.")

    print("[PASS] AES-256-GCM roundtrip and tamper detection")


def test_password_qsec() -> None:
    password = "PQS-CI-Strong-Test-Password"
    payload = b"QSEC password container roundtrip"
    container = encrypt_password(payload, password, {"content": "ci-test"})
    decrypted, metadata = decrypt_password(container, password)
    check(decrypted == payload, "Password QSEC payload mismatch.")
    check(metadata.get("content") == "ci-test", "Password QSEC metadata mismatch.")
    expect_failure(decrypt_password, container, "wrong-password")

    text = "Post-Quantum Security – CI Unicode Test"
    encrypted_text = encrypt_text_password(text, password)
    check(decrypt_text_password(encrypted_text, password) == text, "Password text roundtrip failed.")

    print("[PASS] Argon2id + AES-256-GCM QSEC password workflows")


def test_post_quantum() -> None:
    check(pq.kem_available(), f"{KEM_ALGORITHM} is not available in liboqs.")
    check(pq.signature_available(), f"{SIGNATURE_ALGORITHM} is not available in liboqs.")

    public_key, secret_key = pq.generate_kem_keypair()
    kem_ciphertext, shared_secret_enc = pq.encapsulate(public_key)
    shared_secret_dec = pq.decapsulate(secret_key, kem_ciphertext)
    check(shared_secret_enc == shared_secret_dec, "ML-KEM shared secrets do not match.")

    sig_public, sig_secret = pq.generate_signature_keypair()
    message = b"ML-DSA-65 CI signature self-test"
    signature = pq.sign(sig_secret, message)
    check(pq.verify(sig_public, message, signature), "ML-DSA valid signature was rejected.")
    check(not pq.verify(sig_public, message + b"!", signature), "ML-DSA accepted modified data.")

    print(f"[PASS] {KEM_ALGORITHM} encapsulation / decapsulation")
    print(f"[PASS] {SIGNATURE_ALGORITHM} sign / verify and tamper rejection")


def test_full_file_and_key_workflows() -> None:
    password = "PQS-CI-Key-Protection-Password"

    with tempfile.TemporaryDirectory(prefix="pqs-ci-") as temp:
        root = Path(temp)

        kem_pub, kem_priv, _ = create_kem_keypair(str(root), "ci-kem", password)
        expect_failure(load_private_key, kem_priv, "wrong-password", "KEM", KEM_ALGORITHM)

        payload = b"Full ML-KEM + HKDF + AES-GCM QSEC integration test"
        container = encrypt_pq(payload, str(kem_pub), {"content": "ci-test"})
        decrypted, metadata = decrypt_pq(container, str(kem_priv), password)
        check(decrypted == payload, "Full PQ QSEC payload mismatch.")
        check(metadata.get("content") == "ci-test", "Full PQ QSEC metadata mismatch.")

        text = "ML-KEM text workflow"
        encrypted_text = encrypt_text_pq(text, str(kem_pub))
        check(decrypt_text_pq(encrypted_text, str(kem_priv), password) == text, "PQ text roundtrip failed.")

        sig_pub, sig_priv, _ = create_signature_keypair(str(root), "ci-signature", password)
        document = root / "document.bin"
        signature_file = root / "document.qsig"
        document.write_bytes(b"Signed PQS integration test content")

        sign_file(str(document), str(sig_priv), password, str(signature_file))
        check(verify_file(str(document), str(sig_pub), str(signature_file)), "Signature file verification failed.")

        document.write_bytes(b"Modified PQS integration test content")
        check(not verify_file(str(document), str(sig_pub), str(signature_file)), "Modified signed file was accepted.")

    print("[PASS] Protected key files, QSEC PQ workflows, and signature file workflows")


def main() -> None:
    print("BylickiLabs Post Quantum Security – GitHub Actions cryptographic self-test")
    test_aes_gcm()
    test_password_qsec()
    test_post_quantum()
    test_full_file_and_key_workflows()
    print("[PASS] All cryptographic self-tests completed successfully.")


if __name__ == "__main__":
    main()
