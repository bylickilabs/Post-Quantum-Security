from __future__ import annotations

import argparse
import re
from pathlib import Path


COMPANY_NAME = "BylickiLabs"
FILE_DESCRIPTION = "BylickiLabs Post Quantum Security"
PRODUCT_NAME = "Post Quantum Security"
INTERNAL_NAME = "PostQuantumSecurity"
COPYRIGHT = "Copyright © 2026 Thorsten Bylicki / BylickiLabs"
COMMENTS = (
    "BylickiLabs Post Quantum Security is a Windows desktop application for "
    "post-quantum encryption, digital signatures, secure key management and "
    "local encrypted storage."
)
LANGUAGE_LABEL = "German / English"


def parse_version(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value.strip())
    if not match:
        raise ValueError(f"Unsupported semantic version: {value}")
    return tuple(int(part) for part in match.groups())


def make_string_table(language_code: str, version: str, original_filename: str) -> str:
    return f"""StringTable(
        '{language_code}04B0',
        [
          StringStruct('CompanyName', '{COMPANY_NAME}'),
          StringStruct('FileDescription', '{FILE_DESCRIPTION}'),
          StringStruct('FileVersion', '{version}.0'),
          StringStruct('InternalName', '{INTERNAL_NAME}'),
          StringStruct('LegalCopyright', '{COPYRIGHT}'),
          StringStruct('OriginalFilename', '{original_filename}'),
          StringStruct('ProductName', '{PRODUCT_NAME}'),
          StringStruct('ProductVersion', '{version}'),
          StringStruct('Comments', '{COMMENTS}'),
          StringStruct('Language', '{LANGUAGE_LABEL}')
        ]
      )"""


def build_version_resource(version: str) -> str:
    major, minor, patch = parse_version(version)
    numeric = f"({major}, {minor}, {patch}, 0)"
    original_filename = f"Post-Quantum-Security-v{version}.exe"
    german_table = make_string_table("0407", version, original_filename)
    english_table = make_string_table("0409", version, original_filename)

    return f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={numeric},
    prodvers={numeric},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        {german_table},
        {english_table}
      ]
    ),
    VarFileInfo(
      [
        VarStruct('Translation', [1031, 1200, 1033, 1200])
      ]
    )
  ]
)
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PyInstaller Windows version metadata.")
    parser.add_argument("--version", required=True, help="Semantic version, for example 1.0.0")
    parser.add_argument("--output", required=True, help="Output version-info file")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_version_resource(args.version), encoding="utf-8")
    print(f"Windows version resource written to {output}")


if __name__ == "__main__":
    main()
