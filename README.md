| <img width="1280" height="640" alt="PQS" src="https://github.com/user-attachments/assets/4e17ea71-5ba9-44a0-9ec0-e696733e7a44" /> |
|---|

> [!IMPORTANT]
> **COMING SOON**
>
> BylickiLabs Quantum Security is currently under active development. Source code, documentation, releases, and further technical details will be published progressively.

| The project focuses on **modern Post Quantum Security** and the secure processing of sensitive data. |
|--|

> Its core principles include:
  - 🔐 **Local Security Architecture**
  - 🛡️ **Strong Cryptographic Mechanisms**
  - ⚛️ **Post Quantum Key Technologies**
  - 🔑 **Secure Key Management**
  - ✍️ **Digital Signatures**
  - 📁 **Secure Text and File Encryption**

> The development aims to combine **established security mechanisms** with **future-oriented Post Quantum Cryptography** within a standalone application.

```yarn
BylickiLabs Quantum Security is built for secure, future-ready Post Quantum Cryptography.
```

<br>

## 🔐 Cryptographic Architecture Comparison

| Security Area | Traditional OpenPGP / RSA / ECC | BylickiLabs Post Quantum Security | Purpose |
|---|---|---|---|
| **Security Model** | Classical public-key cryptography | Post-Quantum oriented hybrid security architecture | Protect data against current and future cryptographic threats |
| **Key Establishment** | RSA, ECDH or comparable classical mechanisms | **ML-KEM** | Establish a shared secret between sender and recipient |
| **Post-Quantum KEM** | Not part of traditional RSA/ECC key exchange | **ML-KEM-768** | Selected ML-KEM parameter set for quantum-resistant key establishment |
| **Data Encryption** | Usually hybrid encryption with a symmetric cipher | **AES-256-GCM** | Encrypt the actual text and file payload efficiently |
| **Digital Signatures** | RSA, ECDSA, EdDSA or other classical signature algorithms | **ML-DSA** | Create and verify quantum-resistant digital signatures |
| **Signature Profile** | Depends on the selected OpenPGP key type | **ML-DSA-65** | Post-Quantum signature generation and verification |
| **Public Keys** | Used for encryption, key establishment or signature verification | ML-KEM and ML-DSA public keys | Can be distributed without exposing private key material |
| **Private Keys** | Required for decryption or signing | Protected ML-KEM and ML-DSA private keys | Remain secret and are protected before local storage |
| **Private-Key Protection** | Implementation dependent | **Argon2id + AES-256-GCM** | Protect private key material with a password-derived encryption key |
| **Key Management** | Usually external keyrings or dedicated PGP applications | Integrated key generation, storage, loading and export | Centralize cryptographic key management inside the application |
| **Local Key Vault** | Depends on the implementation | Integrated **SQLite Key Vault** | Store key records, fingerprints, configuration and protected key containers |
| **File Encryption** | Supported by OpenPGP implementations | Integrated `.qsec` container | Encrypt files using the application's hybrid security architecture |
| **Text Encryption** | Supported by many OpenPGP implementations | Integrated text encryption | Encrypt and decrypt text directly inside the application |
| **Integrity Protection** | Cryptographic signatures and authenticated encryption depending on implementation | AES-256-GCM authentication + ML-DSA signatures | Detect unauthorized modification of protected data |
| **Quantum Resistance** | Traditional RSA/ECC algorithms are not designed to resist cryptographically relevant quantum computers | ML-KEM and ML-DSA are designed as Post-Quantum algorithms | Prepare cryptographic systems for the Post-Quantum era |

---

## ⚛️ Post-Quantum Algorithms

| Algorithm | Type | Used For | Role in Post Quantum Security |
|---|---|---|---|
| **ML-KEM** | Key Encapsulation Mechanism | Secure establishment of shared secrets | Provides the Post-Quantum foundation for secure key establishment |
| **ML-KEM-768** | ML-KEM parameter set | Quantum-resistant key encapsulation | Used by the application to establish cryptographic key material |
| **ML-DSA** | Digital Signature Algorithm | Signing and signature verification | Provides Post-Quantum authenticity and integrity protection |
| **ML-DSA-65** | ML-DSA parameter set | Application signatures | Used for generating and verifying Post-Quantum digital signatures |
| **AES-256-GCM** | Symmetric authenticated encryption | Text and file encryption | Encrypts the actual payload after the required key material has been established |
| **Argon2id** | Password-based Key Derivation Function | Private-key protection | Derives strong encryption keys from passwords for protecting private key material |

<br>

## ⚙️ Technology Stack

| Component | Technology |
|---|---|
| **Application** | Python |
| **Desktop Interface** | PySide6 |
| **Post-Quantum Cryptography** | ML-KEM-768 / ML-DSA-65 |
| **Post-Quantum Library** | liboqs / Open Quantum Safe |
| **Payload Encryption** | AES-256-GCM |
| **Key Derivation** | Argon2id / HKDF-SHA-256 |
| **Local Storage** | SQLite |
| **Encrypted Container** | `.qsec` |

---

> [!NOTE]
> ## 🛡️ Security Notice
>
> BylickiLabs Quantum Security is currently under active development.
>
> The cryptographic architecture is based on established and standardized algorithms. Security-sensitive components, container formats and key-management mechanisms may continue to evolve during development.

---

## 🔑 Key & File Formats

| Format | Type | Purpose |
|---|---|---|
| **`.qpub`** | Public ML-KEM Key | Used for Post-Quantum key encapsulation and encryption workflows |
| **`.qkey`** | Protected Private ML-KEM Key | Used to recover the shared secret required for decryption |
| **`.qsigpub`** | Public ML-DSA Key | Used to verify Post-Quantum digital signatures |
| **`.qsigkey`** | Protected Private ML-DSA Key | Used to create Post-Quantum digital signatures |
| **`.qsig`** | Digital Signature | Stores an ML-DSA-65 signature for verification |
| **`.qsec`** | Encrypted Security Container | Stores encrypted text or file payloads and required cryptographic parameters |
| **SQLite Database** | Local Key Vault | Stores key records, fingerprints, settings and protected key containers |

<br>

```yarn
flowchart TB
    subgraph Encryption["🔐 Encryption"]
        A[Text / File] --> B[ML-KEM-768]
        B --> C[Shared Secret]
        C --> D[HKDF-SHA-256]
        D --> E[AES-256-GCM]
        E --> F[Encrypted .qsec Container]
    end

    subgraph Signatures["✍️ Digital Signatures"]
        G[Text / File] --> H[ML-DSA-65]
        H --> I[Digital Signature .qsig]
        I --> J[Signature Verification]
    end
```

## 🚀 Development Status

| Status | Information |
|---|---|
| **Development** | Active |
| **Release** | Coming Soon |
| **Platform** | Windows Desktop |
| **Language** | German / English |
| **Architecture** | Local / Offline |
