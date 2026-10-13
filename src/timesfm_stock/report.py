"""Descriptive forecast scores; no trading or investment recommendations."""
from pathlib import Path
import csv
import json

import numpy as np

from .decision import assess, decision_markdown, freeze_policy
from .experiment import read
from .model import QUANTILES


def metrics(frame):
    actual = np.array([row["actual"] for row in frame])
    point = np.array([row["prediction"] for row in frame])
    anchor = np.array([row["anchor"] for row in frame])
    error = (point - actual) / anchor
    naive_error = (anchor - actual) / anchor
    mae, baseline_mae = float(np.mean(abs(error))), float(np.mean(abs(naive_error)))
    drift = np.array([row.get("drift_prediction", row["anchor"]) for row in frame])
    drift_error = (drift - actual) / anchor
    return {
        "n": len(frame), "mae_pct": 100 * mae,
        "rmse_pct": 100 * float(np.sqrt(np.mean(error ** 2))),
        "baseline_mae_pct": 100 * baseline_mae,
        "baseline_rmse_pct": 100 * float(np.sqrt(np.mean(naive_error ** 2))),
        "drift_mae_pct": 100 * float(np.mean(abs(drift_error))),
        "always_up_accuracy_pct": 100 * float(np.mean(np.sign(actual-anchor) == 1)),
        "always_down_accuracy_pct": 100 * float(np.mean(np.sign(actual-anchor) == -1)),
        "history_direction_accuracy_pct": 100 * float(np.mean([
            r.get("history_direction", 1) == np.sign(r["actual"]-r["anchor"]) for r in frame])),
        "skill_pct": 100 * (1 - mae / baseline_mae) if baseline_mae > 0 else None,
        "direction_accuracy_pct": 100 * float(np.mean(np.sign(point-anchor) == np.sign(actual-anchor))),
        "coverage_80_pct": 100 * float(np.mean([r["q10"] <= r["actual"] <= r["q90"] for r in frame])),
        "mean_interval_width_pct": float(np.mean([100 * (r["q90"]-r["q10"])/r["anchor"] for r in frame])),
        "pinball_pct": float(np.mean([r["pinball_pct"] for r in frame])),
    }


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def report(root, policy=None):
    root = Path(root)
    destination = root / "reports"
    destination.mkdir(parents=True, exist_ok=True)
    if policy is None:
        policy = read(root / 'decision_policy.json') if (root / 'decision_policy.json').exists() else read('decision_policy.json')
    policy = freeze_policy(root, policy)
    pending_primary = 0
    rows, counts = [], {"pending": 0, "excluded_split": 0}
    runs = sorted((root / "runs").glob("*.json"))
    for path in runs:
        run = read(path)
        for i, symbol in enumerate(run["symbols"]):
            anchor = run["last_price"][i]
            history = np.array([r["close"] for r in run["history"][symbol]])
            drift_per_session = (history[-1] - history[0]) / (len(history) - 1)
            for h, date in enumerate(run["target_dates"], 1):
                observation_path = root / "observations" / path.stem / symbol / f"{date}.json"
                if not observation_path.exists():
                    counts["pending"] += 1
                    if h == policy['primary_horizon']:
                        pending_primary += 1
                    continue
                observation = read(observation_path)
                if observation["status"] != "observed":
                    counts[observation["status"]] += 1
                    continue
                actual = observation["actual"]
                historical_signs = np.sign(history[h:] / history[:-h] - 1)
                # Fixed tie rule; fitted entirely from the frozen historical input.
                history_direction = 1 if np.sum(historical_signs == 1) >= np.sum(historical_signs == -1) else -1
                for mode, forecast in run["predictions"].items():
                    quantiles = np.asarray(forecast["quantiles"][i][h-1])
                    residual = actual - quantiles
                    pinball = np.maximum(np.asarray(QUANTILES)*residual,
                                         (np.asarray(QUANTILES)-1)*residual).mean()
                    rows.append({"origin": run["origin"], "issued_at": run["issued_at"],
                                 "symbol": symbol, "mode": mode, "horizon": h, "target_date": date,
                                 "anchor": anchor, "actual": actual,
                                 "prediction": forecast["point"][i][h-1],
                                 "baseline": anchor, "drift_prediction": float(anchor + h * drift_per_session),
                                 "history_direction": history_direction, "q10": float(quantiles[0]), "q90": float(quantiles[-1]),
                                 "pinball_pct": float(100*pinball/anchor)})
    write_csv(destination / "predictions.csv", rows)
    summary = []
    for mode in sorted({r["mode"] for r in rows}):
        for symbol in ["ALL", *sorted({r["symbol"] for r in rows})]:
            for horizon in ["all", "1", "5", "20"]:
                group = [r for r in rows if r["mode"] == mode and (symbol == "ALL" or r["symbol"] == symbol)
                         and (horizon == "all" or r["horizon"] == int(horizon))]
                if group:
                    summary.append({"mode": mode, "symbol": symbol, "horizon": horizon, **metrics(group)})
    write_csv(destination / "summary.csv", summary)
    sector_rows = []
    if (root / 'experiment.json').exists():
        sectors = read(root / 'experiment.json')['config'].get('sectors', {})
        for mode in sorted({r['mode'] for r in rows}):
            for sector in sorted(set(sectors.values())):
                for horizon in ['1', '5', '20']:
                    group = [r for r in rows if r['mode'] == mode and r['horizon'] == int(horizon)
                             and sectors.get(r['symbol']) == sector]
                    if group:
                        sector_rows.append({'mode': mode, 'sector': sector, 'horizon': horizon, **metrics(group)})
    write_csv(destination / 'sector_summary.csv', sector_rows)
    text = ["# TimesFM 3.0 forward test", "",
            f"Frozen forecast origins: **{len(runs)}**. Pending ticker/date outcomes: **{counts['pending']}**. "
            f"Split exclusions: **{counts['excluded_split']}**.", "",
            "Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. "
            "Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).", "",
            "| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for row in summary:
        if row["symbol"] == "ALL":
            skill = "n/a" if row["skill_pct"] is None else f"{row['skill_pct']:.2f}"
            text.append(f"| {row['mode']} | {row['horizon']} | {row['n']} | {row['mae_pct']:.3f} | "
                        f"{row['baseline_mae_pct']:.3f} | {skill} | {row['direction_accuracy_pct']:.1f} | {row['coverage_80_pct']:.1f} |")
    if sector_rows:
        text.extend(['', '## Sector diagnostics (5-session horizon)', '',
                     '| Mode | Sector | N | Skill vs last price % |', '|---|---|---:|---:|'])
        for row in sector_rows:
            if row['horizon'] == '5':
                value = 'n/a' if row['skill_pct'] is None else f"{row['skill_pct']:.2f}"
                text.append(f"| {row['mode']} | {row['sector']} | {row['n']} | {value} |")
        text.extend(['', 'Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.'])
    if not rows:
        text.extend(["", "No realized scores yet. Forecasts remain pending until their target sessions close."])
    text.extend(["", "N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; "
                 "one month provides descriptive evidence, not proof of a persistent trading advantage. "
                 "Direction compares movement from the origin, including exact zero-move ties. "
                 "Prices are Yahoo Close, not dividend-adjusted total returns. "
                 "First-observed actuals are frozen; provider corrections may differ later.", "",
                 "See summary.csv for per-symbol scores and predictions.csv for individual outcomes."])
    if (root / 'experiment.json').exists():
        decision = assess(rows, runs, read(root / 'experiment.json'), policy, pending_primary)
        (destination / 'decision.json').write_text(json.dumps(decision, indent=2, allow_nan=False) + '\n')
        text.extend(['', *decision_markdown(decision)])
    else:
        text.extend(['', 'No forecast has been issued for this study yet. Collection starts with the first successful prospective run.'])
    (destination / "report.md").write_text("\n".join(text) + "\n")
    print(f"Report: {destination / 'report.md'}")
