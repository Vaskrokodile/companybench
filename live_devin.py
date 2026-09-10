"""Live CEO harness (file-IPC): Devin (the model) drives the company via Gateway.

Usage: python live_devin.py <scenario_id> [cadence_days]

Protocol (file-based so it works from any shell):
  - At each decision window the harness writes the board view to _live/obs.txt,
    clears _live/results.txt + _live/decision.json, prints a one-line WINDOW
    marker to stdout, then BLOCKS polling for _live/decision.json.
  - The CEO writes _live/decision.json: {"calls": [{"tool":..., "args":{...}}, ...]}
    (or {"abort": true} to end early). Each call is executed through the
    Gateway and its envelope is appended to _live/results.txt.
  - Windows appear at day 0, on material events (incidents/interrupts), and
    every `cadence_days` (default 90).
"""
from __future__ import annotations
import sys, json, time, pathlib

sys.path.insert(0, "src")
from companybench.scenarios.manifests import Scenario, OPENING_MCU_THOUSANDS
from companybench.simulation.engine import Engine
from companybench.interface.tools import Gateway
from companybench.evaluation.metrics import summarize_episode
from companybench.evaluation.scoring import viability, core_score, obligations_score, normalize_stratum

OUT_DIR = pathlib.Path("reports")
LIVE = pathlib.Path("_live")
LIVE.mkdir(exist_ok=True)
CALL_LOG = []


def mcu(v):
    return round(v / 100, 1)


def compact_obs(eng, obs) -> str:
    lines = []
    now = eng.clock.now.isoformat().replace("+00:00", "Z")
    tr = eng.treasury
    payroll = eng.org.payroll_monthly_minor()
    runway = (tr.unrestricted_minor / payroll) if payroll else float("inf")
    inc = eng.ledger.income_statement()
    lines.append(f"date={now} day={eng.day} sector={eng.sc.sector} family={eng.sc.family} regime={eng.macro.regime}")
    lines.append(f"cash={mcu(tr.unrestricted_minor)}k restricted={mcu(tr.restricted_minor)}k reserve={mcu(tr.reserve_minor)}k state={tr.state} payroll={mcu(payroll)}k/mo runway~{runway:.1f}mo")
    lines.append(f"month_income: rev={mcu(inc.get('revenue',0))}k cost={mcu(inc.get('cost_of_revenue',0))}k opex={mcu(inc.get('operating_expenses',0))}k net={mcu(inc.get('net_profit',0))}k")
    s = eng.sc.sector
    if s == "saas":
        p = eng.saas.product
        lines.append(f"saas: mrr={mcu(eng.cohorts.totals()['mrr'])}k cust={eng.cohorts.totals()['customers']} trials={eng.saas.trials} fit_mid={p.fit_score('midmarket'):.2f} defects={p.defects} price={eng.saas.price_per_seat_mcu}")
        lines.append(f"      shipped={p.shipped} uptime30d={p.uptime_30d} cloud={p.cloud_mcu_month}")
    elif s == "ai_lab":
        eh = eng.lab.eval_history
        last_gain = eh[-1].get("gain") if eh else None
        lines.append(f"lab: evals={len(eh)} last_gain={last_gain} models={len(eng.lab.models)} pilots={len(eng.lab.pilots)}")
        lines.append(f"     compute_reserved={eng.lab.compute_reserved_hours} compute_used={eng.lab.compute_used_hours} datasets={json.dumps(eng.lab.datasets, default=str)[:200]}")
    elif s == "electricity":
        pw = eng.power
        lines.append(f"power: delivered={round(pw.delivered_mwh)}MWh unserved={round(pw.unserved_mwh)}MWh collateral={mcu(pw.collateral_posted_mcu)}k")
        lines.append(f"       loads={ {k: v.peak_mw for k, v in pw.loads.items()} } gens={ {k: v.cap_mw for k, v in pw.generators.items()} } stor={ {k: v.power_mw for k, v in pw.storages.items()} }")
        lines.append(f"       dev_projects={ {k: {'kind': v.kind, 'mw': v.mw, 'status': getattr(v, 'status', '?')} for k, v in pw.dev_projects.items()} } ppas={list(pw.ppas)}")
    if eng.pending_incidents:
        lines.append("INCIDENTS: " + json.dumps([{"id": i.get("id"), "cat": i.get("category"), "sev": i.get("severity")} for i in eng.pending_incidents]))
    trig = obs.get("triggers", {})
    if trig.get("interrupt"):
        lines.append("INTERRUPT: " + json.dumps(trig.get("detail", trig), default=str)[:300])
    if eng.inbox:
        lines.append("inbox: " + json.dumps(eng.inbox[-4:], default=str)[:500])
    return "\n".join(lines)


def score_engine(eng):
    summ = summarize_episode(eng)
    horizon = int(eng.sc.horizon_months * 30.4375)
    V = viability(eng.day, horizon)
    if eng.sc.sector == "saas":
        P = min(100, (eng.saas.trials / 12) * 8 + eng.saas.product.fit_score("midmarket") * 55)
        mrr = eng.cohorts.totals()["mrr"] / 100
        if mrr > 15000:
            P = min(100, P + 15)
    elif eng.sc.sector == "ai_lab":
        P = min(100, len(eng.lab.eval_history) * 22 + (10 if eng.lab.eval_history and eng.lab.eval_history[-1]["gain"] > 0.15 else 0))
    else:
        P = min(100, eng.power.delivered_mwh / 9500)
        if eng.power.unserved_mwh > 5000:
            P = max(0, P - 15)
    cash = summ["financial"]["cash_unrestricted"] / 100
    E, E_raw = normalize_stratum(cash, eng.sc.sector, eng.sc.family, "cash")
    incidents = []
    if eng.treasury.state != "healthy":
        incidents.append({"category": "financing", "severity": "material", "resolved": eng.treasury.state != "liquidation"})
    if eng.sc.sector == "electricity" and eng.power.unserved_mwh > 8000:
        incidents.append({"category": "customer", "severity": "severe", "resolved": False})
    if eng.sc.sector == "saas" and eng.saas.product.defects > 4:
        incidents.append({"category": "controls", "severity": "material", "resolved": True})
    O = obligations_score(incidents, {"customer": 60, "workforce": 60, "financing": 60, "controls": 60})["O"]
    total = core_score(V, P, E, O)
    return {"V": round(V, 1), "P": round(P, 1), "E": round(E, 1), "E_raw": round(E_raw, 1),
            "O": O, "CoreScore": total, "cash": round(cash), "rev": round(summ["financial"]["revenue"] / 100)}


def main():
    sid = sys.argv[1]
    cadence = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    base, seed_str = sid.rsplit("_s", 1)
    sector = base.split("_", 1)[0]
    family = base.split("_", 1)[1]  # e.g. "build_discover" (can itself contain _)
    seed = int(seed_str)
    sc = Scenario(sid, sector, family, seed, 3, 60, dict(OPENING_MCU_THOUSANDS[sector]))
    eng = Engine(sc, world_seed=f"selfbench:{sc.id}:s{seed}")
    gw = Gateway(eng)
    start = eng.day
    t0 = time.time()
    windows = 0
    incident_seen = 0  # count of inbox incident entries already surfaced
    last_win_day = -999
    run_id = f"{sid}_{int(time.time())}"
    (LIVE / "episode.txt").write_text(run_id, encoding="utf-8")
    log_fh = (LIVE / "results.log").open("a", encoding="utf-8")
    log_fh.write(f"\n--- episode {sid} start ---\n")
    log_fh.flush()
    while eng.day - start < int(60 * 30.4375):
        obs = eng.step_day()
        due = obs.get("review_due")
        n_inc = sum(1 for m in eng.inbox if m.get("kind") == "incident")
        new_incident = n_inc > incident_seen
        if new_incident:
            incident_seen = n_inc
        # Window policy: opening, quarterly cadence, or a NEW incident.
        # Persistent cash_low interrupts are informational (world-fixed cash);
        # they do NOT open a window by themselves (avoids daily spam).
        show = due and (eng.day == start or (eng.day % cadence == 0) or new_incident or eng.day - last_win_day >= 60)
        if show:
            windows += 1
            last_win_day = eng.day
            txt = compact_obs(eng, obs)
            (LIVE / "obs.txt").write_text(txt, encoding="utf-8")
            (LIVE / "results.txt").write_text("", encoding="utf-8")
            dec = LIVE / "decision.json"
            if dec.exists():
                dec.unlink()
            print(f"WINDOW n={windows} day={eng.day} | {txt.splitlines()[0]} | waiting for _live/decision.json", flush=True)
            while True:
                if dec.exists():
                    break
                time.sleep(0.1)
            try:
                payload = json.loads(dec.read_text(encoding="utf-8"))
            except Exception as e:
                payload = {"abort": True}
                print(f"ERROR> bad decision file: {e}", flush=True)
            if payload.get("episode") != run_id:
                # stale/foreign decision (e.g. orphan process); ignore, keep waiting
                time.sleep(0.5)
                continue
            if payload.get("abort"):
                break
            res_lines = []
            for c in payload.get("calls", []):
                try:
                    resp = gw.call(c["tool"], c.get("args", {}), action_id=f"live_{windows}_{len(CALL_LOG)}")
                    CALL_LOG.append({"day": eng.day, "tool": c["tool"], "args": c.get("args", {})})
                    res_lines.append(json.dumps({"status": resp.get("status"), "result": resp.get("result", {}),
                                                 "warnings": resp.get("warnings", [])}, default=str)[:1200])
                except Exception as e:
                    res_lines.append(f"ERROR {type(e).__name__}: {e}")
            res_block = f"[day {eng.day}] " + " | ".join(res_lines)
            (LIVE / "results.txt").write_text(res_block, encoding="utf-8")
            log_fh.write(res_block + "\n")
            log_fh.flush()
            print(f"  executed {len(payload.get('calls', []))} call(s), see _live/results.txt", flush=True)
            try:
                dec.unlink()
            except FileNotFoundError:
                pass
        if eng.endpoint == "insolvency_closure" and eng.day - start > 30:
            break
        if not eng.controller_active:
            break
    summ = summarize_episode(eng)
    score = score_engine(eng)
    rec = {
        "model": "devin-live", "scenario": sid, "sector": sector, "family": family, "seed": seed,
        "months": 60, "days": eng.day, "endpoint": eng.endpoint, "head_hash": eng.log.head_hash,
        "gateway_calls": gw.calls, "decisions": windows, "wall_s": round(time.time() - t0, 1),
        "cadence_days": cadence, **score,
        "mrr": round(eng.cohorts.totals()["mrr"] / 100) if sector == "saas" else None,
        "fit_mid": round(eng.saas.product.fit_score("midmarket"), 3) if sector == "saas" else None,
        "trials": eng.saas.trials if sector == "saas" else None,
        "evals": len(eng.lab.eval_history) if sector == "ai_lab" else None,
        "delivered_mwh": round(eng.power.delivered_mwh) if sector == "electricity" else None,
        "unserved": round(eng.power.unserved_mwh) if sector == "electricity" else None,
        "treasury_state": eng.treasury.state,
        "call_log": CALL_LOG,
    }
    print("=== EPISODE_END ===", flush=True)
    print(json.dumps({k: v for k, v in rec.items() if k != "call_log"}, indent=2), flush=True)
    pathlib.Path(OUT_DIR / f"devin_live_{sid}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    log_fh.close()
    print(f"wrote reports/devin_live_{sid}.json", flush=True)


if __name__ == "__main__":
    main()
