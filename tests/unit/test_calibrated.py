"""Calibrated params + anchors enforcement (spec §36, §28.7)."""
import hashlib
import json
import pathlib
from companybench.calibration.registry import get, meta
from companybench.calibration.anchors import load, normalize_stratum

def test_calibrated_params_frozen():
    m = meta()
    assert m["sha256"] == "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92"
    assert m["status"] == "calibrated_frozen"
    assert get("score.obligations_k") == 65.0
    assert get("labor.ramp_general_weeks") == 5

def test_calibrated_churn_logit():
    import math
    # smb p=0.035 => logit -3.317
    v = get("saas.smb_churn_base")
    assert abs(v - (-3.317)) < 0.01
    assert abs(1/(1+math.exp(-v)) - 0.035) < 0.001

def test_anchors_frozen():
    a = load()
    assert a["sha256"] == "8f1d26fe2c6ec9017266aaa37541b25377519e85ccdf3695b2e0a2346b072068"
    assert a["params_sha256"] == "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92"
    # per-stratum L<U for at least cash
    for k, v in a["strata"].items():
        assert v["cash"]["U"] > v["cash"]["L"], f"{k} cash anchors degenerate"

def test_normalize_uses_anchors():
    clip, raw = normalize_stratum(700000, "saas", "build_discover", "cash")
    assert 0 <= clip <= 100
    assert raw != 0

def test_scoring_k_calibrated():
    from companybench.evaluation.scoring import K_OBLIGATIONS
    assert K_OBLIGATIONS == 65.0
    from companybench.evaluation.scoring import obligations_score
    # 1 material/12mo should be ~53 not 0.5 (BUG-01)
    r = obligations_score([{"category": "customer", "severity": "material", "resolved": True}],
                          {"customer": 12, "workforce": 12, "financing": 12, "controls": 12})
    assert r["categories"]["customer"] > 40, f"got {r}"
