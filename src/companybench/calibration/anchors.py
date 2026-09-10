"""Anchors loader (spec §28.7): frozen L/U per stratum, never model best/worst."""
from __future__ import annotations

import hashlib
import json
import pathlib

CAL_DIR = pathlib.Path(__file__).resolve().parents[3] / "calibration"
ANCHORS_PATH = CAL_DIR / "anchors_v1.0.json"
EXPECTED_SHA = "8f1d26fe2c6ec9017266aaa37541b25377519e85ccdf3695b2e0a2346b072068"

_REG = None

def load():
    global _REG
    if _REG is not None:
        return _REG
    if not ANCHORS_PATH.exists():
        raise RuntimeError(f"anchors not found: {ANCHORS_PATH} — run calibration/build_anchors.py")
    raw = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    check = raw.get("sha256")
    # verify hash (excluding sha field)
    blob = {k: v for k, v in raw.items() if k != "sha256"}
    calc = hashlib.sha256(json.dumps(blob, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if check != calc or calc != EXPECTED_SHA:
        raise RuntimeError(f"anchors hash mismatch: got {check}, calc {calc}, expected {EXPECTED_SHA}")
    if raw.get("params_sha256") != "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92":
        raise RuntimeError("anchors params sha mismatch — rebuild anchors after calibrate")
    _REG = raw
    return raw

def lookup(sector: str, family: str, metric: str = "cash") -> tuple[float, float]:
    reg = load()
    key = f"{sector}_{family}"
    entry = reg["strata"].get(key)
    if not entry:
        # fallback global
        entry = reg["global"]
    m = entry.get(metric, reg["global"].get(metric, {"L": 0, "U": 1}))
    return float(m["L"]), float(m["U"])

def normalize_stratum(value: float, sector: str, family: str, metric: str = "cash") -> tuple[float, float]:
    """Returns (clipped 0-100, unclipped)."""
    L, U = lookup(sector, family, metric)
    if U <= L:
        return 0.0, 0.0
    raw = 100 * (value - L) / (U - L)
    clipped = min(100, max(0, raw))
    return round(clipped, 2), round(raw, 2)
