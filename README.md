# Security Suite — 8×12 Architecture (Repo-ready)

這個壓縮檔解壓後即可作為 GitHub Repo 使用，內含：
- 架構圖（v1/v2/v3）、風險對策、模組分工、RACI、API 合約、Flow/Toggle Schemas
- Orchestrator / Registry / Agents 骨架與測試
- CI 工作流程：驗證 flows/toggles 與 agents 契約一致性

## 快速開始（Git Bash）
```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -U pip pytest pyyaml jsonschema
python scripts/validate_flows.py
python scripts/validate_agents_doc.py
python -m pytest -q
```

或直接執行：
```bash
bash bash-quickstart.sh
```

## 推上 GitHub（範例，需先在 GitHub 建立空 repo 或使用 gh）
```bash
git init
git add .
git commit -m "chore: initial import"
git branch -M main
# 其一：使用 GitHub CLI（推薦）
# gh auth login
# gh repo create <your-username>/security-suite-merged --public --source . --remote origin --push
# 其二：HTTP 遠端（先於 GitHub 建立空 repo 並複製 URL）
git remote add origin https://github.com/<your-username>/security-suite-merged.git
git push -u origin main
```

> 上傳後請到 **Actions** 確認工作流程 **Validate Agents & Flows** 全綠。
> 貢獻流程與 PR 標題格式請見 `CONTRIBUTING.md`。

_Updated: 2025-08-21_


## Quickstart (Minimal Demo)

```bash
bash bash-quickstart.sh
```

This will:
1. Validate the demo flow (JSON content stored in `impl/flows/scan_and_report.yaml`).
2. Execute the orchestrator to generate artifacts under `artifacts/<run_id>/`.
3. Validate the artifacts (schema-level, minimal).
```
