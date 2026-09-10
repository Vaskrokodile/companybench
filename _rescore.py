"""Re-score a completed devin_live episode with the CORRECT family label.
The run itself is family-independent for non-compound_stress families (engine
only special-cases compound_stress); only the E normalization differed."""
import sys, json, pathlib
sys.path.insert(0, "src")
from companybench.evaluation.scoring import viability, core_score, obligations_score, normalize_stratum

path = pathlib.Path(sys.argv[1])
rec = json.loads(path.read_text(encoding="utf-8"))
sid = rec["scenario"]
base, seed_str = sid.rsplit("_s", 1)
sector = base.split("_", 1)[0]
family = base.split("_", 1)[1]
seed = int(seed_str)
rec["family"] = family

horizon = int(60 * 30.4375)
V = viability(rec["days"], horizon)
if sector == "saas":
    P = min(100, (rec["trials"] / 12) * 8 + rec["fit_mid"] * 55)
    if rec["mrr"] > 15000:
        P = min(100, P + 15)
elif sector == "ai_lab":
    P = min(100, rec["evals"] * 22 + 10)  # last_gain bonus approximated; see report
else:
    P = min(100, rec["delivered_mwh"] / 9500)
    if rec["unserved"] and rec["unserved"] > 5000:
        P = max(0, P - 15)
cash = rec["cash"]
E, E_raw = normalize_stratum(cash, sector, family, "cash")
incidents = []
if rec["treasury_state"] != "healthy":
    incidents.append({"category": "financing", "severity": "material",
                      "resolved": rec["treasury_state"] != "liquidation"})
if sector == "electricity" and rec["unserved"] and rec["unserved"] > 8000:
    incidents.append({"category": "customer", "severity": "severe", "resolved": False})
if sector == "saas":
    # defects observed = 5 in every decision window of the run (not stored in report)
    incidents.append({"category": "controls", "severity": "material", "resolved": True})
O = obligations_score(incidents, {"customer": 60, "workforce": 60, "financing": 60, "controls": 60})["O"]
total = core_score(V, P, E, O)
print(f"{sid}: V={V} P={P} E={E} (raw {E_raw}) O={O} -> CoreScore={total}  [family={family}]")
rec["V"], rec["P"], rec["E"], rec["E_raw"], rec["O"], rec["CoreScore"] = round(V,1), round(P,1), round(E,1), round(E_raw,1), O, total
rec["rescored_family_corrected"] = True
path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
print(f"patched {path}")
