#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo ">>> Running minimal flow validation"
python3 scripts/validate_flows.py

echo ">>> Running orchestrator demo run"
python3 -c "import sys; sys.path.insert(0,''); from impl.core.orchestrator import run; print(run('.'))" | tee /tmp/orch.out

RUN_DIR=$(python3 - <<'PY'
import json, sys, re
import os
# naive parse from previous print
s=open('/tmp/orch.out').read()
m=re.search(r"'run_dir':\s*'([^']+)'", s)
print(m.group(1) if m else '')
PY
)

if [ -n "$RUN_DIR" ]; then
  echo ">>> Validating artifacts in $RUN_DIR"
  python3 scripts/validate_artifacts.py "$RUN_DIR"
  echo "Artifacts OK"
else
  echo "Could not detect run_dir"
fi

echo "All done."