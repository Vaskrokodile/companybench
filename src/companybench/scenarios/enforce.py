"""Loader enforcement: rejects uncalibrated manifests (spec §41.1)."""
from __future__ import annotations

import json
import pathlib

MANIFEST_DIR = pathlib.Path("scenarios/public")
FROZEN_PARAMS_SHA = "9558ac4baaee1b3b4a3fb95790e5546f944996963b1b586a6172b896f9451e92"
FROZEN_ANCHORS_SHA = "8f1d26fe2c6ec9017266aaa37541b25377519e85ccdf3695b2e0a2346b072068"


def check_manifest(path: pathlib.Path) -> list[str]:
    errs = []
    txt = path.read_text(encoding="utf-8")
    if "illustrative_uncalibrated" in txt:
        errs.append(f"{path.name}: manifest_status illustrative_uncalibrated — ranked runs rejected (see calibration/params_v1.0.json)")
    if "prerelease_requires_calibration" in txt:
        errs.append(f"{path.name}: missing frozen anchor set")
    return errs


def enforce_calibrated() -> None:
    # verify frozen artifacts exist and hash
    import hashlib
    for p, expect in [
        (pathlib.Path("calibration/params_v1.0.json"), FROZEN_PARAMS_SHA),
        (pathlib.Path("calibration/anchors_v1.0.json"), FROZEN_ANCHORS_SHA),
    ]:
        if not p.exists():
            raise RuntimeError(f"missing frozen artifact {p}")
        raw = json.loads(p.read_text(encoding="utf-8"))
        blob = {k: v for k, v in raw.items() if k != "sha256"}
        calc = hashlib.sha256(json.dumps(blob, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if calc != expect or raw.get("sha256") != expect:
            raise RuntimeError(f"{p.name} hash mismatch: calc {calc} vs {expect}")


if __name__ == "__main__":
    enforce_calibrated()
    print("calibration artifacts frozen and valid")
