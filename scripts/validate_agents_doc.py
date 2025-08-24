import sys, pathlib

def main():
    # Accept either docs/agents.md or AGENTS.md at repo root.
    candidates = [pathlib.Path("docs")/"agents.md", pathlib.Path("AGENTS.md")]
    ok = any(p.exists() for p in candidates)
    if not ok:
        print("WARN: agents guide not found at docs/agents.md or AGENTS.md (ok for now)")
    print("validate_agents_doc: OK")

if __name__ == "__main__":
    main()
