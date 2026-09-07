from __future__ import annotations

import os
import sys

_DLL_DIRECTORY_HANDLE = None

if getattr(sys, "frozen", False):
    bundle_root = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    oqs_root = os.path.join(bundle_root, "oqs-runtime")
    oqs_bin = os.path.join(oqs_root, "bin")

    os.environ["OQS_INSTALL_PATH"] = oqs_root
    os.environ["PATH"] = oqs_bin + os.pathsep + os.environ.get("PATH", "")

    if hasattr(os, "add_dll_directory"):
        try:
            _DLL_DIRECTORY_HANDLE = os.add_dll_directory(oqs_bin)
        except OSError:
            _DLL_DIRECTORY_HANDLE = None
