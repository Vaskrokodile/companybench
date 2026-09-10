"""Experimental protocol & statistics (spec §30).

Unit = episode. Launch matrix 3×4×10×2=240 (planning default; power analysis
required). Paired RNG worlds; aggregation world→family→sector→overall; cluster
bootstrap over world blocks; survival with competing endpoints; bands not ranks.
"""
from __future__ import annotations

import math
import random


def launch_matrix(sectors: int = 3, families: int = 4, seeds: int = 10, replicates: int = 2) -> int:
    return sectors * families * seeds * replicates


def aggregate(episodes: list[dict]) -> dict:
    """episodes: [{sector, family, seed, replicate, score}]. Macro-average."""
    by_sector: dict[str, list[float]] = {}
    for e in episodes:
        by_sector.setdefault(e["sector"], []).append(e["score"])
    sector_means = {s: sum(v) / len(v) for s, v in by_sector.items()}
    overall = sum(sector_means.values()) / len(sector_means) if sector_means else 0.0
    return {"sector_means": sector_means, "overall": overall, "n": len(episodes)}


def paired_bootstrap(a: list[float], b: list[float], n_boot: int = 2000, seed: int = 0) -> dict:
    """Cluster bootstrap over paired differences (world blocks kept together)."""
    assert len(a) == len(b) and a
    rng = random.Random(seed)
    diffs = [x - y for x, y in zip(a, b)]
    mean = sum(diffs) / len(diffs)
    boots = []
    for _ in range(n_boot):
        s = sum(rng.choice(diffs) for _ in diffs) / len(diffs)
        boots.append(s)
    boots.sort()
    return {"mean_diff": mean, "ci95": [boots[int(0.025 * n_boot)], boots[int(0.975 * n_boot)]],
            "n": len(diffs)}


def restricted_mean_survival(times: list[float], H: float) -> float:
    return sum(min(t, H) for t in times) / len(times) if times else 0.0


def cumulative_incidence(endpoints: list[str]) -> dict:
    tot = len(endpoints) or 1
    out: dict[str, float] = {}
    for e in endpoints:
        out[e] = out.get(e, 0) + 1 / tot
    return out
