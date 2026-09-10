"""Evidence registry loader (spec §36.2 hierarchy)."""
from __future__ import annotations

import csv
import json
import pathlib

CAL_DIR = pathlib.Path(__file__).resolve().parents[3] / "calibration"
# src/companybench/calibration/*.py -> parents[3] = E:/companybench
TIERS = {"T1-official-stats": 1, "T1-official-system": 1, "T2-primary-research": 2,
         "T2-vendor-measurement": 2, "T3-anonymized-ops": 3, "T4-expert-survey": 4,
         "T5-expert-elicitation": 5}


def load_sources() -> list[dict]:
    with open(CAL_DIR / "sources.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_dataset(name: str) -> dict:
    with open(CAL_DIR / "datasets" / name, encoding="utf-8") as f:
        return json.load(f)
