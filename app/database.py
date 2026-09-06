import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, overload


class KeyPairSummary(TypedDict):
    id: int
    name: str
    key_type: str
    algorithm: str
    fingerprint: str
    created_at: str


class KeyPairRecord(KeyPairSummary):
    public_data: str
    private_data: str
    public_extension: str
    private_extension: str


def get_app_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        path = base / "BylickiLabs" / "QuantumSecurity"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        path = base / "bylickilabs" / "quantum-security"

    path.mkdir(parents=True, exist_ok=True)
    return path


class Database:
    def __init__(self) -> None:
        self.data_dir = get_app_data_dir()
        self.key_dir = self.data_dir / "loaded_keys"
        self.key_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "quantum_security.db"
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _initialize(self) -> None:
        with self.connect() as con:
            con.executescript(
                """
                CREATE TABLE IF NOT EXISTS keypairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    key_type TEXT NOT NULL,
                    algorithm TEXT NOT NULL,
                    fingerprint TEXT NOT NULL,
                    public_data TEXT NOT NULL,
                    private_data TEXT NOT NULL,
                    public_extension TEXT NOT NULL,
                    private_extension TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(key_type, fingerprint)
                );

                CREATE INDEX IF NOT EXISTS idx_keypairs_type
                ON keypairs(key_type);

                CREATE INDEX IF NOT EXISTS idx_keypairs_created
                ON keypairs(created_at DESC);

                CREATE TABLE IF NOT EXISTS settings (
                    setting_key TEXT PRIMARY KEY,
                    setting_value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )

    def save_setting(self, key: str, value: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as con:
            con.execute(
                """
                INSERT INTO settings(setting_key, setting_value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(setting_key) DO UPDATE SET
                    setting_value = excluded.setting_value,
                    updated_at = excluded.updated_at
                """,
                (key, value, now),
            )

    @overload
    def get_setting(self, key: str, default: str) -> str:
        ...

    @overload
    def get_setting(self, key: str, default: None = None) -> str | None:
        ...

    def get_setting(self, key: str, default: str | None = None) -> str | None:
        with self.connect() as con:
            row = con.execute(
                "SELECT setting_value FROM settings WHERE setting_key = ?", (key,)
            ).fetchone()

        if row is None:
            return default
        return str(row["setting_value"])

    def save_keypair(
        self,
        name: str,
        key_type: str,
        algorithm: str,
        fingerprint: str,
        public_data: str,
        private_data: str,
        public_extension: str,
        private_extension: str,
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as con:
            con.execute(
                """
                INSERT INTO keypairs(
                    name, key_type, algorithm, fingerprint, public_data, private_data,
                    public_extension, private_extension, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(key_type, fingerprint) DO UPDATE SET
                    name = excluded.name,
                    algorithm = excluded.algorithm,
                    public_data = excluded.public_data,
                    private_data = excluded.private_data,
                    public_extension = excluded.public_extension,
                    private_extension = excluded.private_extension
                """,
                (
                    name,
                    key_type,
                    algorithm,
                    fingerprint,
                    public_data,
                    private_data,
                    public_extension,
                    private_extension,
                    now,
                ),
            )
            row = con.execute(
                "SELECT id FROM keypairs WHERE key_type = ? AND fingerprint = ?",
                (key_type, fingerprint),
            ).fetchone()

        if row is None:
            raise RuntimeError("Key record could not be retrieved after saving.")
        return int(row["id"])

    def save_keypair_files(
        self,
        name: str,
        key_type: str,
        algorithm: str,
        fingerprint: str,
        public_path: str | Path,
        private_path: str | Path,
    ) -> int:
        public_file = Path(public_path)
        private_file = Path(private_path)
        return self.save_keypair(
            name=name,
            key_type=key_type,
            algorithm=algorithm,
            fingerprint=fingerprint,
            public_data=public_file.read_text(encoding="utf-8"),
            private_data=private_file.read_text(encoding="utf-8"),
            public_extension=public_file.suffix,
            private_extension=private_file.suffix,
        )

    def list_keypairs(self) -> list[KeyPairSummary]:
        with self.connect() as con:
            rows = con.execute(
                """
                SELECT id, name, key_type, algorithm, fingerprint, created_at
                FROM keypairs
                ORDER BY created_at DESC, id DESC
                """
            ).fetchall()

        return [
            {
                "id": int(row["id"]),
                "name": str(row["name"]),
                "key_type": str(row["key_type"]),
                "algorithm": str(row["algorithm"]),
                "fingerprint": str(row["fingerprint"]),
                "created_at": str(row["created_at"]),
            }
            for row in rows
        ]

    def get_keypair(self, key_id: int) -> KeyPairRecord | None:
        with self.connect() as con:
            row = con.execute(
                "SELECT * FROM keypairs WHERE id = ?", (key_id,)
            ).fetchone()

        if row is None:
            return None

        return {
            "id": int(row["id"]),
            "name": str(row["name"]),
            "key_type": str(row["key_type"]),
            "algorithm": str(row["algorithm"]),
            "fingerprint": str(row["fingerprint"]),
            "public_data": str(row["public_data"]),
            "private_data": str(row["private_data"]),
            "public_extension": str(row["public_extension"]),
            "private_extension": str(row["private_extension"]),
            "created_at": str(row["created_at"]),
        }

    def delete_keypair(self, key_id: int) -> None:
        with self.connect() as con:
            con.execute("DELETE FROM keypairs WHERE id = ?", (key_id,))

    @staticmethod
    def _safe_filename(name: str) -> str:
        valid = "".join(c for c in name if c.isalnum() or c in ("-", "_", "."))
        return valid or "quantum_key"

    def materialize_keypair(self, key_id: int) -> tuple[Path, Path, KeyPairRecord]:
        record = self.get_keypair(key_id)
        if record is None:
            raise ValueError("Key record not found.")

        stem = f"{record['id']}_{self._safe_filename(record['name'])}"
        public_path = self.key_dir / f"{stem}{record['public_extension']}"
        private_path = self.key_dir / f"{stem}{record['private_extension']}"
        public_path.write_text(record["public_data"], encoding="utf-8")
        private_path.write_text(record["private_data"], encoding="utf-8")
        return public_path, private_path, record

    def export_keypair(
        self, key_id: int, folder: str | Path
    ) -> tuple[Path, Path, KeyPairRecord]:
        record = self.get_keypair(key_id)
        if record is None:
            raise ValueError("Key record not found.")

        target = Path(folder)
        target.mkdir(parents=True, exist_ok=True)
        stem = self._safe_filename(record["name"])
        public_path = target / f"{stem}{record['public_extension']}"
        private_path = target / f"{stem}{record['private_extension']}"
        public_path.write_text(record["public_data"], encoding="utf-8")
        private_path.write_text(record["private_data"], encoding="utf-8")
        return public_path, private_path, record
