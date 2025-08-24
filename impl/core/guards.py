from typing import Any, Dict, List, Tuple

SeverityWeight = {"low": 0.25, "medium": 0.5, "high": 0.75, "critical": 1.0}

def _has_required_fields(f: Dict[str, Any], required: List[str]) -> tuple[bool, list[str]]:
    missing = [k for k in required if k not in f or f[k] in (None, "", [])]
    return (len(missing) == 0, missing)

def usefulness_score(f: Dict[str, Any], weights: Dict[str, float], accepted_severity: List[str]) -> float:
    sev = (f.get("severity") or "").lower()
    sev_w = SeverityWeight.get(sev, 0.0) if sev in accepted_severity else 0.0
    conf = float(f.get("confidence") or 0.0)
    ev = f.get("evidence") or ""
    evidence_quality = 1.0 if isinstance(ev, str) and len(ev) >= 8 else 0.0
    return (weights.get("severity", 0.5) * sev_w
            + weights.get("confidence", 0.3) * conf
            + weights.get("evidence_quality", 0.2) * evidence_quality)

def filter_findings(findings: List[Dict[str, Any]], guards_cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    kept, dropped = [], []
    req = guards_cfg.get("required_fields", ["id","target_id","rule_id","severity","confidence","location","scanner","ts"])
    accepted_sev = [s.lower() for s in guards_cfg.get("accepted_severity", ["low","medium","high","critical"])]
    min_conf = float(guards_cfg.get("min_confidence", 0.6))
    ucfg = guards_cfg.get("usefulness", {})
    min_us = float(ucfg.get("min_usefulness_score", 0.5))
    weights = ucfg.get("weights", {"severity": 0.5, "confidence": 0.3, "evidence_quality": 0.2})

    for f in findings or []:
        ok, missing = _has_required_fields(f, req)
        if not ok:
            f["_dropped_reason"] = f"missing_fields:{','.join(missing)}"
            dropped.append(f); continue
        if (f.get("severity") or "").lower() not in accepted_sev:
            f["_dropped_reason"] = "invalid_severity"; dropped.append(f); continue
        if (f.get("confidence") or 0.0) < min_conf:
            f["_dropped_reason"] = "low_confidence"; dropped.append(f); continue
        score = usefulness_score(f, weights, accepted_sev)
        f["_usefulness_score"] = score
        if score < min_us:
            f["_dropped_reason"] = f"low_usefulness:{score:.2f}"; dropped.append(f); continue
        kept.append(f)
    return kept, dropped