#!/usr/bin/env bash
set -euo pipefail
echo "[1/5] Create venv"
python -m venv .venv
# Windows Git Bash uses Scripts/
# shellcheck disable=SC1091
source .venv/Scripts/activate || { echo "Failed to activate venv"; exit 1; }
echo "[2/5] Install deps"
python -m pip install -U pip pytest pyyaml jsonschema
echo "[3/5] Validate flows & toggles"
python scripts/validate_flows.py
echo "[4/5] Validate agents doc"
python scripts/validate_agents_doc.py
echo "[5/5] Run tests"
python -m pytest -q
echo "All good ✅"
