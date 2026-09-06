# Post Quantum Security

| Lokale Desktopanwendung für klassische Kryptografie und standardisierte Post-Quantum-Verfahren| 
|---|

| ![Python](https://img.shields.io/badge/Python-Desktop_Application-3776AB?logo=python&logoColor=white) | ![PySide6](https://img.shields.io/badge/GUI-PySide6-41CD52?logo=qt&logoColor=white) | ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white) | ![Post Quantum](https://img.shields.io/badge/Post--Quantum-ML--KEM--768_%7C_ML--DSA--65-6f42c1) | ![Status](https://img.shields.io/badge/Development-Completed-success) |
|---|---|---|---|---|

| <img width="1280" height="640" alt="PQS" src="https://github.com/user-attachments/assets/4e17ea71-5ba9-44a0-9ec0-e696733e7a44" /> |
|---|

> [!NOTE]
> **Deutsch:** Post Quantum Security ist eine lokal arbeitende Desktopanwendung mit:
  - klassischer Kryptografie
  - Post-Quantum-Key-Encapsulation
  - digitalen Post-Quantum-Signaturen
  - Schlüsselverwaltung
  - lokalem Key Vault
  - eigenem QSEC-Containerformat
  - einem gemeinsamen lokalen Sicherheitsworkflow

> [!NOTE]
> **English:** Post Quantum Security is a local desktop application with:
  - classical cryptography
  - post-quantum key encapsulation
  - digital post-quantum signatures
  - key management
  - a local key vault
  - a project-specific QSEC container format
  - one unified local security workflow

<br>

----

<br>

## Inhaltsverzeichnis / Table of Contents

### Deutsch

1. [Projektübersicht](#de-projektuebersicht)
2. [Funktionsumfang](#de-funktionsumfang)
3. [Kryptografische Architektur](#de-kryptografische-architektur)
4. [Mathematische Grundlage](#de-mathematische-grundlage)
5. [Eigene Entwicklungsleistung](#de-eigene-entwicklungsleistung)
6. [Dateiformate](#de-dateiformate)
7. [Lokale Datenbank und Key Vault](#de-key-vault)
8. [Projektstruktur](#de-projektstruktur)
9. [Voraussetzungen](#de-voraussetzungen)
10. [Installation](#de-installation)
11. [Anwendung starten](#de-start)
12. [Grundlegende Bedienung](#de-bedienung)
13. [Sicherheit](#de-sicherheit)
14. [Sicherheitskritische Schwachstellen](#de-schwachstellen)
15. [Entwicklungsstatus](#de-status)
16. [Lizenz](#de-lizenz)
17. [Autor](#de-autor)

### English

1. [Project Overview](#en-project-overview)
2. [Feature Set](#en-feature-set)
3. [Cryptographic Architecture](#en-cryptographic-architecture)
4. [Mathematical Foundation](#en-mathematical-foundation)
5. [Original Development Work](#en-original-development-work)
6. [File Formats](#en-file-formats)
7. [Local Database and Key Vault](#en-key-vault)
8. [Project Structure](#en-project-structure)
9. [Requirements](#en-requirements)
10. [Installation](#en-installation)
11. [Starting the Application](#en-start)
12. [Basic Usage](#en-usage)
13. [Security](#en-security)
14. [Security-Critical Vulnerabilities](#en-vulnerabilities)
15. [Development Status](#en-status)
16. [License](#en-license)
17. [Author](#en-author)

<br>

----

<br>

<a id="de-projektuebersicht"></a>

# Deutsch

## 1. Projektübersicht

**Post Quantum Security** ist eine Python-Desktopanwendung mit PySide6-Oberfläche für lokale kryptografische Workflows.

Ziel des Projekts ist die sinnvolle Verbindung etablierter klassischer Kryptografie mit standardisierten Post-Quantum-Verfahren innerhalb einer eigenständig entwickelten Anwendungs- und Sicherheitsarchitektur.

Die Anwendung verarbeitet Texte, Dateien, kryptografische Schlüssel und digitale Signaturen lokal auf dem eigenen System. Für die grundlegenden Sicherheitsfunktionen ist kein externer Verschlüsselungs- oder Cloud-Dienst erforderlich.

| Bereich | Umsetzung |
|---|---|
| Benutzeroberfläche | PySide6 |
| Sprachen | Deutsch / Englisch |
| Datenverschlüsselung | AES-256-GCM |
| Passwortbasierte Schlüsselableitung | Argon2id |
| Schlüsselableitung | HKDF-SHA-256 |
| Post-Quantum KEM | ML-KEM-768 |
| Post-Quantum Signaturen | ML-DSA-65 |
| Lokale Datenbank | SQLite |
| Containerformat | QSEC |
| Verarbeitung | Lokal / Local First |
| Entwicklungsstand | Aktueller Funktionsumfang abgeschlossen |

> [!IMPORTANT]
> Die in der Anwendung eingesetzten kryptografischen Algorithmen sind **keine von BYLICKILABS neu erfundenen Kryptografie-Verfahren**. AES-256-GCM, Argon2id, HKDF-SHA-256, ML-KEM-768 und ML-DSA-65 sind etablierte beziehungsweise standardisierte Verfahren.  
> Die eigene Entwicklungsleistung liegt in der Architektur, Integration, Benutzeroberfläche, Schlüsselverwaltung, Datenbankanbindung, dem QSEC-Workflow sowie der Verbindung der einzelnen Komponenten zu einer vollständigen Anwendung.

<br>

----

<br>

<a id="de-funktionsumfang"></a>

## 2. Funktionsumfang

### Textverschlüsselung

- lokale Verschlüsselung und Entschlüsselung von Text
- Passwortmodus
- Post-Quantum-Modus
- Ausgabe direkt innerhalb der Anwendung
- Kopieren des Ergebnisses in die Zwischenablage

### Dateiverschlüsselung

- Verschlüsselung beliebiger Dateien
- Entschlüsselung von QSEC-Dateien
- Passwortmodus
- Post-Quantum-Modus
- Auswahl von öffentlichen und privaten Schlüsseln
- Drag-and-Drop-Unterstützung für Eingabedateien

### Schlüsselgenerierung und Schlüsselverwaltung

- Erzeugung von ML-KEM-Schlüsselpaaren
- Erzeugung von ML-DSA-Signaturschlüsselpaaren
- passwortgeschützte Speicherung privater Schlüssel
- Fingerprint-Erzeugung
- Speicherung erzeugter Schlüssel im lokalen Key Vault
- Laden gespeicherter Schlüssel
- Export von Schlüsselpaaren
- Löschen von Datenbankeinträgen

### Digitale Signaturen

- Signieren von Dateien mit ML-DSA-65
- Verifikation bestehender Signaturen
- getrennte öffentliche und private Signaturschlüssel
- eigenes `.qsig`-Signaturformat

### Benutzeroberfläche

- vollständig bilinguale Oberfläche in Deutsch und Englisch
- direkter Sprachwechsel innerhalb der Anwendung
- Statusmeldungen und Dialoge
- integrierte Datenbankübersicht
- integrierter Info-Dialog
- direkter GitHub-Zugriff aus der Anwendung

<br>

----

<br>

<a id="de-kryptografische-architektur"></a>

## 3. Kryptografische Architektur

Die Anwendung verwendet mehrere kryptografische Komponenten mit klar getrennten Aufgaben.

| Verfahren | Aufgabe innerhalb der Anwendung |
|---|---|
| **AES-256-GCM** | Authentifizierte symmetrische Verschlüsselung der Nutzdaten |
| **Argon2id** | Passwortbasierte Ableitung kryptografischen Schlüsselmaterials |
| **HKDF-SHA-256** | Ableitung von Schlüsseln aus kryptografischen Geheimnissen |
| **ML-KEM-768** | Post-Quantum Key Encapsulation für gemeinsame kryptografische Geheimnisse |
| **ML-DSA-65** | Digitale Post-Quantum-Signaturen und Signaturprüfung |

### Passwortbasierter Workflow

```text
Passwort
   │
   ▼
Argon2id
   │
   ▼
AES-256-GCM Key
   │
   ▼
Verschlüsselung / Entschlüsselung
   │
   ▼
QSEC Container
```

### Post-Quantum-Workflow

```text
ML-KEM-768 Public Key
          │
          ▼
   Key Encapsulation
          │
          ▼
    Shared Secret
          │
          ▼
    HKDF-SHA-256
          │
          ▼
    AES-256-GCM Key
          │
          ▼
Verschlüsselung / Entschlüsselung
          │
          ▼
      QSEC Container
```

### Signatur-Workflow

```text
Datei
  │
  ▼
ML-DSA-65 Private Key
  │
  ▼
Digitale Signatur
  │
  ▼
.qsig
  │
  ▼
ML-DSA-65 Public Key
  │
  ▼
Verifikation
```

<br>

----

<br>

<a id="de-mathematische-grundlage"></a>

## 4. Mathematische Grundlage

Die eingesetzten Post-Quantum-Verfahren basieren auf gitterbasierter Kryptografie.

Zu den mathematischen Grundlagen gehören unter anderem:

- modulare Arithmetik
- Polynomringe
- Matrix- und Vektoroperationen
- Module-LWE-bezogene Strukturen
- Module-SIS-bezogene Strukturen
- gitterbasierte kryptografische Problemklassen

ML-KEM-768 und ML-DSA-65 nutzen diese mathematischen Strukturen für unterschiedliche Aufgaben: ML-KEM für die sichere Kapselung gemeinsamer Geheimnisse und ML-DSA für digitale Signaturen.

> [!NOTE]
> Die Anwendung implementiert nicht eigene mathematische Post-Quantum-Algorithmen, sondern integriert standardisierte Verfahren in einen eigenständig entwickelten lokalen Sicherheitsworkflow.

<br>

----

<br>

<a id="de-eigene-entwicklungsleistung"></a>

## 5. Eigene Entwicklungsleistung

Die Entwicklungsarbeit dieses Projekts liegt insbesondere in der technischen Konzeption und vollständigen Umsetzung der Anwendung.

Dazu gehören:

- Entwicklung der Desktopanwendung und PySide6-Benutzeroberfläche
- Konzeption der Anwendungs- und Sicherheitsarchitektur
- Integration klassischer und quantenresistenter Kryptografie
- Verbindung von AES-256-GCM, Argon2id, HKDF-SHA-256, ML-KEM-768 und ML-DSA-65
- Entwicklung des QSEC-Containerworkflows
- Definition der projektspezifischen Schlüssel-, Signatur- und Containerdateien
- Entwicklung der lokalen Schlüsselverwaltung
- Integration eines SQLite-basierten Key Vaults
- Fingerprint-Verwaltung
- Schlüsselimport und Schlüsselexport
- Verschlüsselungs- und Entschlüsselungsworkflows
- Signatur- und Verifikationsworkflows
- bilinguale Benutzeroberfläche
- lokale Status-, Fehler- und Informationslogik

Die Anwendung basiert damit auf etablierten kryptografischen Standards, während deren konkrete Integration, Strukturierung und technische Umsetzung Bestandteil der eigenen Softwareentwicklung ist.

<br>

----

<br>

<a id="de-dateiformate"></a>

## 6. Dateiformate

| Endung | Verwendung |
|---|---|
| `.qpub` | Öffentlicher ML-KEM-Schlüssel |
| `.qkey` | Passwortgeschützter privater ML-KEM-Schlüssel |
| `.qsigpub` | Öffentlicher ML-DSA-Signaturschlüssel |
| `.qsigkey` | Passwortgeschützter privater ML-DSA-Signaturschlüssel |
| `.qsig` | Digitale Signatur |
| `.qsec` | Verschlüsselter QSEC-Container |

### QSEC

Das QSEC-Containerformat dient der Speicherung verschlüsselter Dateiinhalte innerhalb des Anwendungsworkflows.

Abhängig vom gewählten Modus kann der zugrunde liegende kryptografische Schlüssel:

- passwortbasiert abgeleitet oder
- über einen ML-KEM-basierten Post-Quantum-Workflow erzeugt werden.

<br>

----

<br>

<a id="de-key-vault"></a>

## 7. Lokale Datenbank und Key Vault

Die Anwendung erzeugt automatisch eine lokale SQLite-Datenbank.

Sie verwaltet unter anderem:

- Schlüssel-ID
- Schlüsselname
- Schlüsseltyp
- verwendeten Algorithmus
- Fingerprint
- Zeitstempel
- Schlüsselreferenzen
- Anwendungseinstellungen
- ausgewählte Sprache

Die Datenbank ist direkt in die Benutzeroberfläche eingebunden. Gespeicherte Schlüssel können angezeigt, geladen, materialisiert, exportiert und aus der Datenbank entfernt werden.

> [!NOTE]
> Verwendete Passwörter werden nicht als Klartext in der lokalen Datenbank gespeichert.

<br>

----

<br>

<a id="de-projektstruktur"></a>

## 8. Projektstruktur

Kernstruktur der Anwendung:

```text
Post-Quantum-Security/
│
├── app/
│   ├── constants.py
│   ├── database.py
│   └── i18n.py
│
├── crypto/
│   ├── container.py
│   ├── keys.py
│   ├── pq.py
│   └── signatures.py
│
├── gui/
│   └── main_window.py
│
├── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

| Bereich | Aufgabe |
|---|---|
| `app/` | Anwendungskonstanten, Internationalisierung und Datenbank |
| `crypto/` | Container, Schlüssel, Post-Quantum-Verfahren und Signaturen |
| `gui/` | PySide6-Benutzeroberfläche |
| `main.py` | Einstiegspunkt der Anwendung |

<br>

----

<br>

<a id="de-voraussetzungen"></a>

## 9. Voraussetzungen

Für die Ausführung werden benötigt:

- Python 3
- PySide6
- `cryptography`
- `argon2-cffi`
- Open Quantum Safe / `liboqs`
- Python-Bindings für `oqs`
- SQLite-Unterstützung der Python-Standardbibliothek

> [!IMPORTANT]
> Die Post-Quantum-Funktionen setzen eine funktionsfähige
> Open-Quantum-Safe-/`liboqs`-Umgebung voraus.
>
> Unter Windows können für die lokale Erstellung beziehungsweise
> Kompilierung von `liboqs` zusätzlich die
> **Microsoft Visual Studio Build Tools** erforderlich sein.
>
> Benötigte Komponenten:
>
> - Visual Studio Build Tools (`vs_BuildTools.exe`)
> - Workload **Desktop development with C++**
> - MSVC C++ Toolchain
> - Windows SDK
> - CMake
>
> Die Build Tools werden insbesondere benötigt, wenn `liboqs`
> auf dem Windows-System selbst kompiliert werden muss.

<br>

----

<br>

<a id="de-installation"></a>

## 10. Installation

Repository klonen:

```bash
git clone https://github.com/bylickilabs/Post-Quantum-Security.git
cd Post-Quantum-Security
```

Virtuelle Umgebung erstellen:

```bash
python -m venv .venv
```

Unter Windows aktivieren:

```powershell
.venv\Scripts\Activate.ps1
```

`pip` aktualisieren und Abhängigkeiten installieren:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

<br>

----

<br>

<a id="de-start"></a>

## 11. Anwendung starten

Die Anwendung wird aus dem Hauptverzeichnis des Projekts gestartet:

```bash
python main.py
```

> [!IMPORTANT]
> `gui/main_window.py` sollte **nicht direkt** gestartet werden.  
> Der vorgesehene Einstiegspunkt ist `main.py`, damit die Projektmodule `app` und `crypto` korrekt über den Projekt-Root aufgelöst werden.

<br>

----

<br>

<a id="de-bedienung"></a>

## 12. Grundlegende Bedienung

### Texte

1. Registerkarte **Text** öffnen.
2. Passwort- oder Post-Quantum-Modus auswählen.
3. Text eingeben beziehungsweise verschlüsselten Text einfügen.
4. Passwort oder passenden Schlüssel angeben.
5. Verschlüsselung oder Entschlüsselung ausführen.

### Dateien

1. Datei auswählen oder per Drag-and-Drop übernehmen.
2. Zieldatei festlegen.
3. Passwort- oder Post-Quantum-Modus auswählen.
4. Passwort beziehungsweise Schlüssel angeben.
5. Verschlüsselung oder Entschlüsselung ausführen.

### Schlüssel

1. Registerkarte **Schlüssel** öffnen.
2. Zielordner und Namen festlegen.
3. Passwort für den privaten Schlüssel vergeben.
4. ML-KEM- oder ML-DSA-Schlüsselpaar erzeugen.

### Signaturen

1. Datei auswählen.
2. privaten ML-DSA-Schlüssel und Passwort angeben.
3. Signatur erzeugen.
4. Zur Prüfung Originaldatei, `.qsig` und öffentlichen ML-DSA-Schlüssel auswählen.
5. Verifikation starten.

<br>

----

<br>

<a id="de-sicherheit"></a>

## 13. Sicherheit

Die Anwendung verfolgt einen Local-First-Ansatz.

- grundlegende kryptografische Verarbeitung erfolgt lokal
- keine externe Verschlüsselungs-API erforderlich
- private Schlüssel werden passwortgeschützt gespeichert
- Passwörter werden nicht als Klartext in der SQLite-Datenbank gespeichert
- AES-256-GCM wird für authentifizierte Datenverschlüsselung eingesetzt
- ML-KEM-768 wird für Post-Quantum-Key-Encapsulation verwendet
- ML-DSA-65 wird für digitale Post-Quantum-Signaturen verwendet

> [!WARNING]
> Kryptografische Software sollte vor einem produktiven oder sicherheitskritischen Einsatz umfassend geprüft und unabhängig auditiert werden. Dieses Projekt stellt keine formale Sicherheitszertifizierung und keinen unabhängigen Security Audit dar.

> [!CAUTION]
> Der Verlust von Passwörtern oder privaten Schlüsseln kann dazu führen, dass verschlüsselte Daten nicht mehr wiederhergestellt werden können. Schlüsselmaterial sollte sicher gesichert werden.

<br>

----

<br>

<a id="de-schwachstellen"></a>

## 14. Sicherheitskritische Schwachstellen

Sicherheitskritische Schwachstellen sollten **nicht über einen öffentlichen GitHub-Issue veröffentlicht werden**.

Bitte sende entsprechende Hinweise direkt an:

**E-Mail:** [bylicki@mail.de](mailto:bylicki@mail.de)

Bitte gib – soweit möglich – folgende Informationen an:

- betroffene Komponente
- reproduzierbare Schritte
- technische Beschreibung
- mögliche Auswirkungen
- verwendete Version beziehungsweise Commit
- relevante Logausgaben ohne vertrauliche Schlüssel oder Passwörter

> [!IMPORTANT]
> Private Schlüssel, Passwörter, geheime Schlüssel oder andere vertrauliche Informationen dürfen nicht mit einem Schwachstellenbericht versendet werden.

<br>

----

<br>

<a id="de-status"></a>

## 15. Entwicklungsstatus

Der für die aktuelle Projektphase vorgesehene Funktionsumfang ist abgeschlossen.

| Funktion | Status |
|---|---|
| Textverschlüsselung / Entschlüsselung | ✅ Abgeschlossen |
| Dateiverschlüsselung / Entschlüsselung | ✅ Abgeschlossen |
| Passwortmodus | ✅ Abgeschlossen |
| ML-KEM-768 Integration | ✅ Abgeschlossen |
| ML-DSA-65 Integration | ✅ Abgeschlossen |
| Schlüsselgenerierung und -verwaltung | ✅ Abgeschlossen |
| SQLite Key Vault | ✅ Abgeschlossen |
| QSEC-Container | ✅ Abgeschlossen |
| Digitale Signaturen / Verifikation | ✅ Abgeschlossen |
| Deutsch / Englisch | ✅ Abgeschlossen |

Weiterführende Optimierungen, Tests und zukünftige Erweiterungen können auf der bestehenden Architektur aufbauen.

<br>

----

<br>

<a id="de-lizenz"></a>

## 16. Lizenz

Die Lizenzbedingungen dieses Projekts befinden sich in:

[LICENSE](LICENSE)

Die Nutzung, Veränderung und Weitergabe des Projekts richtet sich nach den dort festgelegten Bedingungen.

<br>

----


<br>

<a id="de-autor"></a>

## 17. Autor

**Thorsten Bylicki**  
**BYLICKILABS**

[GITHUB](https://github.com/bylickilabs)
[WEBSITE](https://bylickilabs.de)

<br>

----

---

<br>

<a id="en-project-overview"></a>

# English

## 1. Project Overview

**Post Quantum Security** is a Python desktop application developed by BYLICKILABS with a PySide6 user interface for local cryptographic workflows.

The project combines established classical cryptography with standardized post-quantum mechanisms within an independently developed application and security architecture.

The application processes text, files, cryptographic keys and digital signatures locally on the user's system. No external encryption or cloud service is required for the core security functions.

| Area | Implementation |
|---|---|
| User interface | PySide6 |
| Languages | German / English |
| Data encryption | AES-256-GCM |
| Password-based key derivation | Argon2id |
| Key derivation | HKDF-SHA-256 |
| Post-Quantum KEM | ML-KEM-768 |
| Post-Quantum signatures | ML-DSA-65 |
| Local database | SQLite |
| Container format | QSEC |
| Processing | Local / Local First |
| Development status | Current feature set completed |

> [!IMPORTANT]
> The cryptographic algorithms used by the application are **not newly invented cryptographic algorithms developed by BYLICKILABS**. AES-256-GCM, Argon2id, HKDF-SHA-256, ML-KEM-768 and ML-DSA-65 are established or standardized mechanisms.  
> The original development work lies in the architecture, integration, user interface, key management, database integration, QSEC workflow and the combination of these components into a complete application.

<br>

----

<br>

<a id="en-feature-set"></a>

## 2. Feature Set

### Text Encryption

- local text encryption and decryption
- password mode
- post-quantum mode
- result output directly inside the application
- clipboard copy function

### File Encryption

- encryption of arbitrary files
- decryption of QSEC files
- password mode
- post-quantum mode
- public and private key selection
- drag-and-drop support for input files

### Key Generation and Key Management

- generation of ML-KEM key pairs
- generation of ML-DSA signature key pairs
- password-protected storage of private keys
- fingerprint generation
- storage of generated keys in the local key vault
- loading stored keys
- exporting key pairs
- deleting database entries

### Digital Signatures

- signing files with ML-DSA-65
- verification of existing signatures
- separate public and private signature keys
- project-specific `.qsig` signature format

### User Interface

- fully bilingual German and English interface
- direct language switching inside the application
- status messages and dialogs
- integrated database overview
- integrated information dialog
- direct GitHub access from the application

<br>

----

<br>

<a id="en-cryptographic-architecture"></a>

## 3. Cryptographic Architecture

The application uses several cryptographic components with clearly separated responsibilities.

| Mechanism | Purpose within the application |
|---|---|
| **AES-256-GCM** | Authenticated symmetric encryption of payload data |
| **Argon2id** | Password-based derivation of cryptographic key material |
| **HKDF-SHA-256** | Derivation of keys from cryptographic secrets |
| **ML-KEM-768** | Post-quantum key encapsulation for shared cryptographic secrets |
| **ML-DSA-65** | Digital post-quantum signatures and signature verification |

### Password-Based Workflow

```text
Password
   │
   ▼
Argon2id
   │
   ▼
AES-256-GCM Key
   │
   ▼
Encryption / Decryption
   │
   ▼
QSEC Container
```

### Post-Quantum Workflow

```text
ML-KEM-768 Public Key
          │
          ▼
   Key Encapsulation
          │
          ▼
    Shared Secret
          │
          ▼
    HKDF-SHA-256
          │
          ▼
    AES-256-GCM Key
          │
          ▼
Encryption / Decryption
          │
          ▼
      QSEC Container
```

### Signature Workflow

```text
File
  │
  ▼
ML-DSA-65 Private Key
  │
  ▼
Digital Signature
  │
  ▼
.qsig
  │
  ▼
ML-DSA-65 Public Key
  │
  ▼
Verification
```

<br>

----

<br>

<a id="en-mathematical-foundation"></a>

## 4. Mathematical Foundation

The post-quantum mechanisms used by the application are based on lattice-based cryptography.

Their mathematical foundations include:

- modular arithmetic
- polynomial rings
- matrix and vector operations
- Module-LWE-related structures
- Module-SIS-related structures
- lattice-based cryptographic problem classes

ML-KEM-768 and ML-DSA-65 use these structures for different purposes: ML-KEM for secure encapsulation of shared secrets and ML-DSA for digital signatures.

> [!NOTE]
> The application does not implement newly invented mathematical post-quantum algorithms. It integrates standardized mechanisms into an independently developed local security workflow.

<br>

----

<br>

<a id="en-original-development-work"></a>

## 5. Original Development Work

The original development work of this project lies primarily in the technical design and complete implementation of the application.

This includes:

- development of the desktop application and PySide6 user interface
- design of the application and security architecture
- integration of classical and post-quantum cryptography
- combination of AES-256-GCM, Argon2id, HKDF-SHA-256, ML-KEM-768 and ML-DSA-65
- development of the QSEC container workflow
- definition of project-specific key, signature and container files
- development of local key management
- integration of a SQLite-based key vault
- fingerprint management
- key import and export
- encryption and decryption workflows
- signing and verification workflows
- bilingual user interface
- local status, error and information handling

The application therefore relies on established cryptographic standards, while their concrete integration, structure and technical implementation are part of the original software development.

<br>

----

<br>

<a id="en-file-formats"></a>

## 6. File Formats

| Extension | Purpose |
|---|---|
| `.qpub` | Public ML-KEM key |
| `.qkey` | Password-protected private ML-KEM key |
| `.qsigpub` | Public ML-DSA signature key |
| `.qsigkey` | Password-protected private ML-DSA signature key |
| `.qsig` | Digital signature |
| `.qsec` | Encrypted QSEC container |

### QSEC

The QSEC container format stores encrypted file content within the application workflow.

Depending on the selected mode, the underlying cryptographic key can be:

- derived from a password, or
- generated through an ML-KEM-based post-quantum workflow.

<br>

----

<br>

<a id="en-key-vault"></a>

## 7. Local Database and Key Vault

The application automatically creates a local SQLite database.

It manages information including:

- key ID
- key name
- key type
- algorithm
- fingerprint
- timestamp
- key references
- application settings
- selected language

The database is integrated directly into the user interface. Stored keys can be displayed, loaded, materialized, exported and removed from the database.

> [!NOTE]
> Passwords are not stored in plaintext inside the local database.

<br>

----

<br>

<a id="en-project-structure"></a>

## 8. Project Structure

Core application structure:

```text
Post-Quantum-Security/
│
├── app/
│   ├── constants.py
│   ├── database.py
│   └── i18n.py
│
├── crypto/
│   ├── container.py
│   ├── keys.py
│   ├── pq.py
│   └── signatures.py
│
├── gui/
│   └── main_window.py
│
├── main.py
├── requirements.txt
├── LICENSE
└── README.md
```

| Area | Responsibility |
|---|---|
| `app/` | Application constants, internationalization and database |
| `crypto/` | Container, keys, post-quantum mechanisms and signatures |
| `gui/` | PySide6 user interface |
| `main.py` | Application entry point |

<br>

----

<br>

<a id="en-requirements"></a>

## 9. Requirements

The following components are required to run the application:

- Python 3
- PySide6
- `cryptography`
- `argon2-cffi`
- Open Quantum Safe / `liboqs`
- Python bindings for `oqs`
- SQLite support provided by the Python standard library

> [!IMPORTANT]
> The post-quantum functions require a working
> Open Quantum Safe / `liboqs` environment.
>
> On Windows, the
> **Microsoft Visual Studio Build Tools**
> may additionally be required to build or compile `liboqs` locally.
>
> Required components:
>
> - Visual Studio Build Tools (`vs_BuildTools.exe`)
> - **Desktop development with C++** workload
> - MSVC C++ Toolchain
> - Windows SDK
> - CMake
>
> The Build Tools are particularly required when `liboqs`
> needs to be compiled locally on the Windows system.

<br>

----

<br>

<a id="en-installation"></a>

## 10. Installation

Clone the repository:

```bash
git clone https://github.com/bylickilabs/Post-Quantum-Security.git
cd Post-Quantum-Security
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Upgrade `pip` and install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

<br>

----

<br>

<a id="en-start"></a>

## 11. Starting the Application

Start the application from the project root:

```bash
python main.py
```

> [!IMPORTANT]
> Do **not** start `gui/main_window.py` directly.  
> The intended entry point is `main.py`, ensuring that the `app` and `crypto` project modules are resolved correctly from the project root.

<br>

----

<br>

<a id="en-usage"></a>

## 12. Basic Usage

### Text

1. Open the **Text** tab.
2. Select password or post-quantum mode.
3. Enter text or paste encrypted text.
4. Provide the password or appropriate key.
5. Run encryption or decryption.

### Files

1. Select a file or use drag and drop.
2. Define the output file.
3. Select password or post-quantum mode.
4. Provide the password or key.
5. Run encryption or decryption.

### Keys

1. Open the **Keys** tab.
2. Select the destination folder and key name.
3. Set a password for the private key.
4. Generate an ML-KEM or ML-DSA key pair.

### Signatures

1. Select a file.
2. Provide the private ML-DSA key and password.
3. Generate the signature.
4. For verification, select the original file, `.qsig` file and public ML-DSA key.
5. Start verification.

<br>

----

<br>

<a id="en-security"></a>

## 13. Security

The application follows a local-first approach.

- core cryptographic processing is performed locally
- no external encryption API is required
- private keys are stored in password-protected form
- passwords are not stored in plaintext inside the SQLite database
- AES-256-GCM is used for authenticated data encryption
- ML-KEM-768 is used for post-quantum key encapsulation
- ML-DSA-65 is used for digital post-quantum signatures

> [!WARNING]
> Cryptographic software should be thoroughly reviewed and independently audited before production or security-critical use. This project does not represent a formal security certification or an independent security audit.

> [!CAUTION]
> Losing passwords or private keys may make encrypted data unrecoverable. Cryptographic key material should be backed up securely.

<br>

----

<br>

<a id="en-vulnerabilities"></a>

## 14. Security-Critical Vulnerabilities

Security-critical vulnerabilities should **not be disclosed through a public GitHub issue**.

Please report them directly to:

**E-mail:** [bylicki@mail.de](mailto:bylicki@mail.de)

Where possible, include:

- affected component
- reproducible steps
- technical description
- potential impact
- affected version or commit
- relevant log output without confidential keys or passwords

> [!IMPORTANT]
> Never send private keys, passwords, secret keys or other confidential data with a vulnerability report.

<br>

----

<br>

<a id="en-status"></a>

## 15. Development Status

The feature set planned for the current project phase has been completed.

| Feature | Status |
|---|---|
| Text encryption / decryption | ✅ Completed |
| File encryption / decryption | ✅ Completed |
| Password mode | ✅ Completed |
| ML-KEM-768 integration | ✅ Completed |
| ML-DSA-65 integration | ✅ Completed |
| Key generation and management | ✅ Completed |
| SQLite key vault | ✅ Completed |
| QSEC container | ✅ Completed |
| Digital signatures / verification | ✅ Completed |
| German / English | ✅ Completed |

Further optimization, testing and future extensions can build on the existing architecture.

<br>

----

<br>

<a id="en-license"></a>

## 16. License

The license terms for this project are available in:

[LICENSE](LICENSE)

Use, modification and redistribution of this project are governed by the terms defined there.

<br>

----

<br>

<a id="en-author"></a>

## 17. Author

**Thorsten Bylicki**  
**BYLICKILABS**

[GITHUB](https://github.com/bylickilabs)
[WEBSITE](https://bylickilabs.de)
