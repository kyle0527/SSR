from ..core.middlewares import guarded_step
import time, random

@guarded_step("scanner")
def scan(target: dict, flow: dict, toggles: dict):
    # Produce a couple of synthetic findings per target for demonstration.
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    addr = target.get("address", "unknown")
    tid = target.get("target_id", f"t-{random.randint(100,999)}")
    findings = [
        {
            "id": f"F-{tid}-001",
            "target_id": tid,
            "rule_id": "TLS.WEAK_CIPHER",
            "severity": "high",
            "confidence": 0.9,
            "evidence": "cipher suites: TLS_RSA_WITH_3DES_EDE_CBC_SHA",
            "location": f"{addr}:443",
            "scanner": "tls-checker@1.0.0",
            "ts": now
        },
        {
            "id": f"F-{tid}-002",
            "target_id": tid,
            "rule_id": "HEADERS.MISSING_SECURITY",
            "severity": "medium",
            "confidence": 0.55,
            "evidence": "missing: Content-Security-Policy",
            "location": addr,
            "scanner": "headers-checker@1.0.0",
            "ts": now
        }
    ]
    return findings