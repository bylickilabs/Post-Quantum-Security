$ErrorActionPreference = "Stop"

Write-Host "BylickiLabs Quantum Security v1.0.0 - Windows Setup" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found in PATH."
}

python -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host ""
Write-Host "Installation completed." -ForegroundColor Green
Write-Host "Start with: .\.venv\Scripts\python.exe main.py"
Write-Host ""
Write-Host "Note: liboqs-python may require Git, CMake and Visual Studio Build Tools (Desktop development with C++) on Windows."
