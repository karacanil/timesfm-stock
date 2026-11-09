"""python -m trader.cli backtest --policy trader_policy_vN.json  -> trader-results/vN/backtest/report.md"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from . import data
from .backtest import fixed_mix, pass_bar, statistics, trend_strategy


def freeze_policy(policy_path, output):
    policy = json.loads(Path(policy_path).read_text())
    saved = Path(output) / "policy.json"
    if saved.exists():
        if json.loads(saved.read_text()) != policy:
            raise ValueError("Policy file changed after it was frozen; use a new version and output directory")
    else:
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text(json.dumps(policy, indent=2) + "\n")
    return policy


def run_backtest(policy, output, cache, refresh=False, fetch=data.yahoo_adjusted):
    symbols = policy["universe"] + [policy["cash_rate_symbol"]]
    frames = data.load(symbols, policy["data_start"], cache, refresh, fetch)
    opens, closes, filled = data.panel(frames, policy["universe"])
    cash_daily = data.cash_rate(frames, policy["cash_rate_symbol"], closes.index)

    equity, trades, decisions = trend_strategy(opens, closes, cash_daily, policy)
    doubled_equity, doubled_trades, _ = trend_strategy(opens, closes, cash_daily, policy, cost_multiplier=2.0)
    spy_equity, spy_trades = fixed_mix(opens, closes, cash_daily, policy, policy["benchmarks"]["spy_buy_hold"], monthly=False)
    mix_equity, mix_trades = fixed_mix(opens, closes, cash_daily, policy, policy["benchmarks"]["sixty_forty_monthly"], monthly=True)

    results = {
        "trend_strategy": statistics(equity, cash_daily, trades),
        "trend_strategy_doubled_costs": statistics(doubled_equity, cash_daily, doubled_trades),
        "spy_buy_hold": statistics(spy_equity, cash_daily, spy_trades),
        "sixty_forty_monthly": statistics(mix_equity, cash_daily, mix_trades),
    }
    gate = pass_bar(results["trend_strategy"], results["spy_buy_hold"], results["sixty_forty_monthly"],
                    results["trend_strategy_doubled_costs"], policy)
    exposure = decisions.sum(axis=1)
    summary = {
        "policy_sha256": hashlib.sha256(json.dumps(policy, sort_keys=True).encode()).hexdigest(),
        "data_sha256": data.fingerprint(frames),
        "forward_filled_sessions": filled,
        "average_gross_exposure_pct": 100 * float(exposure.mean()),
        "time_fully_in_cash_pct": 100 * float((exposure == 0).mean()),
        "results": results, "pass_bar": gate,
    }
    out = Path(output) / "backtest"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    curves = equity.to_frame("trend_strategy").join(spy_equity.rename("spy_buy_hold")).join(mix_equity.rename("sixty_forty_monthly"))
    curves.round(6).to_csv(out / "equity.csv")
    decisions.round(4).to_csv(out / "weekly_targets.csv")
    trades.to_csv(out / "trades.csv", index=False)
    (out / "report.md").write_text(markdown(summary))
    return summary


def markdown(summary):
    names = {"trend_strategy": "Trend strategy", "trend_strategy_doubled_costs": "Trend, 2x costs",
             "spy_buy_hold": "SPY buy & hold", "sixty_forty_monthly": "60/40 SPY/IEF"}
    results = summary["results"]
    first = results["trend_strategy"]
    lines = ["# Trend strategy backtest (policy v1)", "",
             f"Period {first['start']} to {first['end']}. Decided at each week's last close, filled at the next open, "
             "10 bps per trade (20 bps in the stress row). Dividend-adjusted Yahoo prices; cash earns the 13-week T-bill rate.", "",
             f"## Verdict: **{summary['pass_bar']['verdict']}**", "",
             "| Check | Result |", "|---|---|"]
    lines += [f"| {name.replace('_', ' ')} | {'pass' if ok else 'FAIL'} |" for name, ok in summary["pass_bar"]["checks"].items()]
    lines += ["", f"Sharpe floor (SPY Sharpe minus tolerance): {summary['pass_bar']['sharpe_floor']:.2f}", "",
              "## Results", "",
              "| Portfolio | CAGR % | Volatility % | Sharpe | Max drawdown % | Worst year | Turnover %/yr | Cost drag %/yr |",
              "|---|---:|---:|---:|---:|---|---:|---:|"]
    for key, label in names.items():
        r = results[key]
        lines.append(f"| {label} | {r['cagr_pct']:.2f} | {r['volatility_pct']:.2f} | {r['sharpe']:.2f} | "
                     f"{r['max_drawdown_pct']:.1f} ({r['max_drawdown_date']}) | {r['worst_year']}: {r['worst_year_pct']:.1f}% | "
                     f"{r.get('annual_turnover_pct', 0):.0f} | {r.get('annual_cost_drag_pct', 0):.2f} |")
    lines += ["", "## Stress years (calendar-year return %)", "", "| Portfolio | 2008 | 2020 | 2022 |", "|---|---:|---:|---:|"]
    for key, label in names.items():
        years = results[key]["calendar_year_pct"]
        lines.append(f"| {label} | " + " | ".join(f"{years.get(y, float('nan')):.1f}" for y in (2008, 2020, 2022)) + " |")
    lines += ["", "## CAGR by third of the period (%)", "", "| Portfolio | First | Second | Third |", "|---|---:|---:|---:|"]
    for key, label in names.items():
        lines.append(f"| {label} | " + " | ".join(f"{x:.2f}" for x in results[key]["cagr_by_third_pct"]) + " |")
    lines += ["", f"Average gross exposure: {summary['average_gross_exposure_pct']:.1f}%. "
              f"Weeks fully in cash: {summary['time_fully_in_cash_pct']:.1f}%.", "",
              "This is a sanity check of a published idea, not proof of future returns. The rules were fixed in "
              "the policy file before this backtest ran; a RETHINK verdict means changing the strategy in a new policy "
              "version, not tuning parameters until this period looks good. Yahoo adjusted prices can be revised; "
              "fractional shares are assumed; taxes are ignored.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rule-based trend strategy tools")
    parser.add_argument("command", choices=["backtest"])
    parser.add_argument("--policy", type=Path, default=Path("trader_policy_v1.json"))
    parser.add_argument("--output", type=Path, help="default: trader-results/v<policy version>")
    parser.add_argument("--cache", type=Path, default=Path(".cache/trader"))
    parser.add_argument("--refresh", action="store_true", help="re-download prices instead of using the cache")
    args = parser.parse_args()
    output = args.output or Path("trader-results") / f"v{json.loads(args.policy.read_text())['version']}"
    policy = freeze_policy(args.policy, output)
    summary = run_backtest(policy, output, args.cache, args.refresh)
    print(f"Verdict: {summary['pass_bar']['verdict']}. Report: {output / 'backtest' / 'report.md'}")


if __name__ == "__main__":
    main()
