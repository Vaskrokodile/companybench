"""Parameter registry (spec §36.1): versioned, frozen, audited.

v1.0 is calibrated_frozen (sha256 9558ac4b...). Loader validates hash and
rejects uncalibrated manifests. All engine modules MUST import via `get()`.
Fictional Meridian game rules grounded in cited public aggregates; uncertainty
published; hard-to-calibrate areas labeled.

Seeds: calibration 1000-1999, eval 0-999, held-out 2000+ — no peeking.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

CAL_DIR = pathlib.Path(__file__).resolve().parents[3] / "calibration"
FROZEN_PATH = CAL_DIR / "params_v1.0.json"
EXPECTED_SHA = "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92"

_REG: dict | None = None


def _load() -> dict:
    global _REG
    if _REG is not None:
        return _REG
    if not FROZEN_PATH.exists():
        raise RuntimeError(f"frozen params not found: {FROZEN_PATH} — run calibration/calibrate.py")
    raw = json.loads(FROZEN_PATH.read_text(encoding="utf-8"))
    # verify sha over params blob (without sha field)
    blob = {k: v for k, v in raw.items() if k != "sha256"}
    check = hashlib.sha256(json.dumps(blob, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if raw.get("sha256") != check or check != EXPECTED_SHA:
        raise RuntimeError(f"params hash mismatch: got {raw.get('sha256')}, expected {EXPECTED_SHA} (calc {check})")
    if raw.get("status") != "calibrated_frozen":
        raise RuntimeError(f"params not frozen: status={raw.get('status')}")
    _REG = raw
    return raw


def get(name: str):
    """Typed accessor for calibrated value."""
    reg = _load()
    try:
        return reg["params"][name]["value"]
    except KeyError:
        raise KeyError(f"unknown param {name}; known={sorted(reg['params'])[:8]}...") from None


def meta() -> dict:
    return _load()


def require_frozen() -> None:
    _load()


# Back-compat: expose frozen version string
REGISTRY_VERSION = "params_v1.0"
# For tooling that inspects PARAMS dict, keep a view
try:
    _tmp = _load()
    PARAMS = _tmp["params"]
except Exception:
    PARAMS = {}
