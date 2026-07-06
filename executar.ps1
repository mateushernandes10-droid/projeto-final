$ErrorActionPreference = "Stop"

$pastaProjeto = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $pastaProjeto

if (-not (Test-Path -LiteralPath ".\.venv\Scripts\python.exe")) {
    python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
