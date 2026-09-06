STRINGS = {
    "de": {
        "app_subtitle": "POST-QUANTUM SECURITY SUITE // ML-KEM-768 // ML-DSA-65 // AES-256-GCM",
        "text_tab": "TEXT SECURITY",
        "file_tab": "FILE SECURITY",
        "keys_tab": "KEY MANAGEMENT",
        "sign_tab": "SIGNATURES",
        "database_tab": "DATABASE",
        "github": "GITHUB",
        "info": "INFO",
        "lang": "LANG DE // EN",
        "mode": "Modus",
        "password_mode": "Passwort",
        "pq_mode": "Post-Quantum",
        "password": "Passwort / Private-Key-Passwort",
        "source_text": "Eingabetext",
        "result_text": "Ergebnis",
        "encrypt_text": "TEXT VERSCHLÜSSELN",
        "decrypt_text": "TEXT ENTSCHLÜSSELN",
        "clear": "LEEREN",
        "copy": "KOPIEREN",
        "public_key": "Öffentlicher ML-KEM-Schlüssel",
        "private_key": "Privater ML-KEM-Schlüssel",
        "browse": "AUSWÄHLEN",
        "input_file": "Eingabedatei",
        "output_file": "Ausgabedatei",
        "encrypt_file": "DATEI VERSCHLÜSSELN",
        "decrypt_file": "DATEI ENTSCHLÜSSELN",
        "drop_hint": "Datei hier ablegen oder auswählen",
        "key_title": "ML-KEM-768 Schlüsselverwaltung",
        "key_desc": "Erzeugt direkt in der Anwendung ein Post-Quantum-Schlüsselpaar für Verschlüsselung. Der private Schlüssel wird mit Argon2id und AES-256-GCM geschützt.",
        "key_folder": "Zielordner",
        "key_name": "Schlüsselname",
        "key_password": "Passwort für privaten Schlüssel",
        "generate_keys": "ML-KEM SCHLÜSSEL ERZEUGEN",
        "fingerprint": "Public-Key-Fingerprint",
        "generated_public": "Erzeugter öffentlicher Schlüssel",
        "generated_private": "Erzeugter privater Schlüssel",
        "sig_key_title": "ML-DSA-65 Schlüsselgenerator",
        "sig_key_desc": "Erzeugt direkt in der Anwendung einen öffentlichen und einen privaten ML-DSA-65-Schlüssel für digitale Signaturen. Der private Schlüssel wird verschlüsselt gespeichert.",
        "sig_folder": "Zielordner",
        "sig_name": "ML-DSA Schlüsselname",
        "generate_sig_keys": "ML-DSA SCHLÜSSEL ERZEUGEN",
        "sign_file": "Datei zum Signieren / Prüfen",
        "signature_file": "Signaturdatei",
        "sign_private_key": "Privater ML-DSA-Schlüssel",
        "sign_public_key": "Öffentlicher ML-DSA-Schlüssel",
        "sign": "DATEI SIGNIEREN",
        "verify": "SIGNATUR PRÜFEN",
        "database_title": "Lokaler Quantum Security Key Vault",
        "database_desc": "Die SQLite-Datenbank wird beim ersten Start automatisch erzeugt. Generierte ML-KEM- und ML-DSA-Schlüsselpaare werden automatisch gespeichert. Private Schlüssel liegen nur in ihrer bereits verschlüsselten Form in der Datenbank; Passwörter werden niemals gespeichert.",
        "database_path": "Datenbankpfad",
        "db_refresh": "AKTUALISIEREN",
        "db_load": "AUSWAHL LADEN",
        "db_export": "AUSWAHL EXPORTIEREN",
        "db_delete": "AUSWAHL LÖSCHEN",
        "db_id": "ID",
        "db_name": "Name",
        "db_type": "Typ",
        "db_algorithm": "Algorithmus",
        "db_fingerprint": "Fingerprint",
        "db_created": "Erstellt",
        "db_empty": "Keine Schlüssel in der Datenbank vorhanden.",
        "db_select": "Bitte zuerst einen Datenbankeintrag auswählen.",
        "db_loaded": "Schlüsselpaar wurde aus der Datenbank geladen und steht in der Anwendung bereit.",
        "db_exported": "Schlüsselpaar wurde erfolgreich exportiert.",
        "db_deleted": "Datenbankeintrag wurde gelöscht.",
        "db_delete_confirm": "Soll das ausgewählte Schlüsselpaar wirklich aus der Datenbank gelöscht werden? Exportierte Schlüsseldateien bleiben davon unberührt.",
        "db_saved": "Schlüsselpaar wurde zusätzlich im lokalen Key Vault gespeichert.",
        "status_ready": "SYSTEM READY",
        "success": "Erfolgreich",
        "error": "Fehler",
        "warning": "Hinweis",
        "confirm": "Bestätigen",
        "copied": "Ergebnis wurde in die Zwischenablage kopiert.",
        "need_password": "Bitte ein Passwort eingeben.",
        "need_text": "Bitte einen Text eingeben.",
        "need_public": "Bitte einen öffentlichen ML-KEM-Schlüssel auswählen.",
        "need_private": "Bitte einen privaten ML-KEM-Schlüssel auswählen.",
        "need_file": "Bitte eine Eingabedatei auswählen.",
        "need_output": "Bitte eine Ausgabedatei festlegen.",
        "need_folder": "Bitte einen Zielordner auswählen.",
        "need_name": "Bitte einen gültigen Schlüsselnamen eingeben.",
        "done_encrypt": "Verschlüsselung erfolgreich abgeschlossen.",
        "done_decrypt": "Entschlüsselung erfolgreich abgeschlossen.",
        "done_keys": "Schlüsselpaar erfolgreich erstellt und in der Datenbank registriert.",
        "done_sign": "Datei wurde erfolgreich signiert.",
        "valid_sig": "Die Signatur ist gültig.",
        "invalid_sig": "Die Signatur ist NICHT gültig.",
        "select_file": "Datei auswählen",
        "save_qsec": "QSEC-Datei speichern",
        "save_file": "Entschlüsselte Datei speichern",
        "select_folder": "Zielordner auswählen",
        "save_signature": "Signatur speichern",
        "info_title": "Über BylickiLabs Quantum Security",
        "info_text": """<h2>BylickiLabs Quantum Security</h2>
<p><b>Version:</b> 1.0.0<br><b>Autor:</b> Thorsten Bylicki / BylickiLabs</p>
<p>BylickiLabs Quantum Security ist eine bilinguale Desktop-Security-Suite für lokale Text- und Dateiverschlüsselung, Post-Quantum-Schlüsselverwaltung, digitale Signaturen und persistente Schlüsselverwaltung über SQLite.</p>
<h3>Sicherheitsarchitektur</h3>
<p><b>AES-256-GCM</b> verschlüsselt die eigentlichen Nutzdaten und liefert gleichzeitig Authentizitäts- und Manipulationsschutz. Für jeden Verschlüsselungsvorgang wird ein neuer kryptografisch zufälliger Nonce erzeugt.</p>
<p><b>Passwortmodus:</b> Argon2id leitet aus Passwort und zufälligem Salt einen 256-Bit-Schlüssel für AES-256-GCM ab.</p>
<p><b>Post-Quantum-Modus:</b> ML-KEM-768 kapselt ein gemeinsames Geheimnis mit dem öffentlichen Schlüssel des Empfängers. HKDF-SHA-256 leitet daraus den AES-256-Schlüssel ab.</p>
<h3>ML-KEM-768 Schlüsselgenerator</h3>
<p>Öffentliche und private ML-KEM-Schlüssel können direkt im Bereich KEY MANAGEMENT erzeugt werden. Öffentliche Schlüssel verwenden <b>.qpub</b>, private Schlüssel <b>.qkey</b>. Der private Schlüssel wird vor dem Speichern mit Argon2id und AES-256-GCM geschützt.</p>
<h3>ML-DSA-65 Schlüsselgenerator</h3>
<p>Die Anwendung erzeugt direkt einen <b>öffentlichen und privaten ML-DSA-65-Schlüssel</b>. Der öffentliche Schlüssel wird als <b>.qsigpub</b>, der passwortgeschützte private Schlüssel als <b>.qsigkey</b> gespeichert. Diese Schlüssel dienen zum Signieren und Verifizieren von Dateien.</p>
<h3>Lokale SQLite-Datenbank</h3>
<p>Beim ersten Start wird automatisch eine SQLite-Datenbank erzeugt. Jeder neu generierte ML-KEM- oder ML-DSA-Schlüsselsatz wird zusätzlich im lokalen Key Vault registriert. Gespeichert werden Name, Typ, Algorithmus, Fingerprint, Erstellungszeitpunkt, öffentlicher Schlüsselcontainer und der bereits verschlüsselte private Schlüsselcontainer.</p>
<p><b>Wichtig:</b> Private Schlüssel werden in der Datenbank niemals unverschlüsselt gespeichert. Das zugehörige Passwort wird weder in der Datenbank noch in einer Konfigurationsdatei abgelegt. Die Datenbank selbst enthält jedoch sichtbare Metadaten und öffentliche Schlüssel.</p>
<p>Im Bereich DATABASE können Schlüssel aufgelistet, geladen, erneut als Schlüsseldateien exportiert oder aus der Datenbank gelöscht werden. Beim Laden werden die geschützten Schlüsseldateien in den lokalen Anwendungsdatenbereich materialisiert und automatisch in die passenden Eingabefelder übernommen.</p>
<p><b>Datenbankpfad:</b><br>__DB_PATH__</p>
<h3>QSEC-Container</h3>
<p>Verschlüsselte Dateien werden als <b>.qsec</b> gespeichert. Der versionierte Container enthält nur die zur Entschlüsselung erforderlichen technischen Parameter, verschlüsselte Nutzdaten und im Post-Quantum-Modus das ML-KEM-Kapselungsobjekt. Passwörter und private Schlüssel werden nicht in QSEC-Dateien geschrieben.</p>
<h3>Datenschutz und Betrieb</h3>
<p>Alle kryptografischen Operationen und Datenbankzugriffe erfolgen lokal. Die Anwendung überträgt keine Dateien, Texte, Passwörter oder Schlüssel an externe Dienste. Die gewählte Sprache DE/EN wird lokal in SQLite gespeichert und beim nächsten Start wiederhergestellt.</p>
<h3>Technischer Hinweis</h3>
<p>Die Post-Quantum-Funktionen verwenden liboqs-python/Open Quantum Safe. ML-KEM-768 und ML-DSA-65 orientieren sich an NIST FIPS 203 beziehungsweise FIPS 204. Die Anwendung ersetzt kein zertifiziertes Hardware Security Module und kein unabhängiges Security-Audit.</p>"""
    },
    "en": {
        "app_subtitle": "POST-QUANTUM SECURITY SUITE // ML-KEM-768 // ML-DSA-65 // AES-256-GCM",
        "text_tab": "TEXT SECURITY",
        "file_tab": "FILE SECURITY",
        "keys_tab": "KEY MANAGEMENT",
        "sign_tab": "SIGNATURES",
        "database_tab": "DATABASE",
        "github": "GITHUB",
        "info": "INFO",
        "lang": "LANG DE // EN",
        "mode": "Mode",
        "password_mode": "Password",
        "pq_mode": "Post-Quantum",
        "password": "Password / Private-key password",
        "source_text": "Input text",
        "result_text": "Result",
        "encrypt_text": "ENCRYPT TEXT",
        "decrypt_text": "DECRYPT TEXT",
        "clear": "CLEAR",
        "copy": "COPY",
        "public_key": "Public ML-KEM key",
        "private_key": "Private ML-KEM key",
        "browse": "BROWSE",
        "input_file": "Input file",
        "output_file": "Output file",
        "encrypt_file": "ENCRYPT FILE",
        "decrypt_file": "DECRYPT FILE",
        "drop_hint": "Drop a file here or browse",
        "key_title": "ML-KEM-768 key management",
        "key_desc": "Generates a post-quantum encryption key pair directly in the application. The private key is protected with Argon2id and AES-256-GCM.",
        "key_folder": "Target folder",
        "key_name": "Key name",
        "key_password": "Private-key password",
        "generate_keys": "GENERATE ML-KEM KEYS",
        "fingerprint": "Public-key fingerprint",
        "generated_public": "Generated public key",
        "generated_private": "Generated private key",
        "sig_key_title": "ML-DSA-65 key generator",
        "sig_key_desc": "Generates a public and a private ML-DSA-65 key directly in the application for digital signatures. The private key is stored encrypted.",
        "sig_folder": "Target folder",
        "sig_name": "ML-DSA key name",
        "generate_sig_keys": "GENERATE ML-DSA KEYS",
        "sign_file": "File to sign / verify",
        "signature_file": "Signature file",
        "sign_private_key": "Private ML-DSA key",
        "sign_public_key": "Public ML-DSA key",
        "sign": "SIGN FILE",
        "verify": "VERIFY SIGNATURE",
        "database_title": "Local Quantum Security Key Vault",
        "database_desc": "The SQLite database is created automatically on first start. Generated ML-KEM and ML-DSA key pairs are stored automatically. Private keys are stored only in their already encrypted form; passwords are never stored.",
        "database_path": "Database path",
        "db_refresh": "REFRESH",
        "db_load": "LOAD SELECTED",
        "db_export": "EXPORT SELECTED",
        "db_delete": "DELETE SELECTED",
        "db_id": "ID",
        "db_name": "Name",
        "db_type": "Type",
        "db_algorithm": "Algorithm",
        "db_fingerprint": "Fingerprint",
        "db_created": "Created",
        "db_empty": "No keys are stored in the database.",
        "db_select": "Please select a database entry first.",
        "db_loaded": "The key pair was loaded from the database and is ready for use in the application.",
        "db_exported": "The key pair was exported successfully.",
        "db_deleted": "The database entry was deleted.",
        "db_delete_confirm": "Do you really want to delete the selected key pair from the database? Exported key files are not affected.",
        "db_saved": "The key pair was also stored in the local key vault.",
        "status_ready": "SYSTEM READY",
        "success": "Success",
        "error": "Error",
        "warning": "Notice",
        "confirm": "Confirm",
        "copied": "Result copied to clipboard.",
        "need_password": "Please enter a password.",
        "need_text": "Please enter text.",
        "need_public": "Please select a public ML-KEM key.",
        "need_private": "Please select a private ML-KEM key.",
        "need_file": "Please select an input file.",
        "need_output": "Please define an output file.",
        "need_folder": "Please select a target folder.",
        "need_name": "Please enter a valid key name.",
        "done_encrypt": "Encryption completed successfully.",
        "done_decrypt": "Decryption completed successfully.",
        "done_keys": "Key pair created successfully and registered in the database.",
        "done_sign": "File signed successfully.",
        "valid_sig": "The signature is valid.",
        "invalid_sig": "The signature is NOT valid.",
        "select_file": "Select file",
        "save_qsec": "Save QSEC file",
        "save_file": "Save decrypted file",
        "select_folder": "Select target folder",
        "save_signature": "Save signature",
        "info_title": "About BylickiLabs Quantum Security",
        "info_text": """<h2>BylickiLabs Quantum Security</h2>
<p><b>Version:</b> 1.0.0<br><b>Author:</b> Thorsten Bylicki / BylickiLabs</p>
<p>BylickiLabs Quantum Security is a bilingual desktop security suite for local text and file encryption, post-quantum key management, digital signatures and persistent key management through SQLite.</p>
<h3>Security architecture</h3>
<p><b>AES-256-GCM</b> encrypts payload data while providing authenticity and tamper detection. A new cryptographically random nonce is created for every encryption operation.</p>
<p><b>Password mode:</b> Argon2id derives a 256-bit key from the password and a random salt for AES-256-GCM.</p>
<p><b>Post-Quantum mode:</b> ML-KEM-768 encapsulates a shared secret with the recipient's public key. HKDF-SHA-256 derives the AES-256 key from this secret.</p>
<h3>ML-KEM-768 key generator</h3>
<p>Public and private ML-KEM keys can be generated directly in KEY MANAGEMENT. Public keys use <b>.qpub</b>; protected private keys use <b>.qkey</b>. The private key is protected with Argon2id and AES-256-GCM before storage.</p>
<h3>ML-DSA-65 key generator</h3>
<p>The application directly generates a <b>public and private ML-DSA-65 key</b>. The public key is stored as <b>.qsigpub</b> and the password-protected private key as <b>.qsigkey</b>. These keys are used to sign and verify files.</p>
<h3>Local SQLite database</h3>
<p>An SQLite database is created automatically on first start. Every newly generated ML-KEM or ML-DSA key pair is also registered in the local key vault. Stored data includes name, type, algorithm, fingerprint, creation time, public key container and the already encrypted private key container.</p>
<p><b>Important:</b> Private keys are never stored unencrypted in the database. Their password is not stored in the database or a configuration file. The database itself does contain visible metadata and public keys.</p>
<p>The DATABASE section can list, load, export or delete stored key pairs. Loading materializes the protected key files in the local application-data directory and automatically assigns them to the appropriate application fields.</p>
<p><b>Database path:</b><br>__DB_PATH__</p>
<h3>QSEC container</h3>
<p>Encrypted files use the <b>.qsec</b> format. The versioned container contains only technical parameters required for decryption, encrypted payload and, in post-quantum mode, the ML-KEM encapsulation object. Passwords and private keys are not written into QSEC files.</p>
<h3>Privacy and operation</h3>
<p>All cryptographic operations and database access are local. The application does not transmit files, text, passwords or keys to external services. The selected DE/EN language is stored locally in SQLite and restored on the next start.</p>
<h3>Technical note</h3>
<p>Post-quantum functionality uses liboqs-python/Open Quantum Safe. ML-KEM-768 and ML-DSA-65 follow NIST FIPS 203 and FIPS 204 respectively. The application is not a replacement for a certified hardware security module or an independent security audit.</p>"""
    }
}


class I18n:
    def __init__(self, lang: str = "de") -> None:
        self.lang: str = lang if lang in STRINGS else "de"

    def t(self, key: str) -> str:
        return STRINGS[self.lang].get(key, key)

    def toggle(self) -> str:
        self.lang = "en" if self.lang == "de" else "de"
        return self.lang