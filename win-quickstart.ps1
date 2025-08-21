# PowerShell quickstart
$ErrorActionPreference = "Stop"
Write-Host "[1/5] Create venv"
py -3 -m venv .venv
Write-Host "[1/5] Activate venv"
.\.venv\Scripts\Activate.ps1
Write-Host "[2/5] Install deps"
py -3 -m pip install -U pip pytest pyyaml jsonschema
Write-Host "[3/5] Validate flows & toggles"
py -3 scripts\validate_flows.py
Write-Host "[4/5] Validate agents doc"
py -3 scripts\validate_agents_doc.py
Write-Host "[5/5] Run tests"
py -3 -m pytest -q
Write-Host "All good ✅"
