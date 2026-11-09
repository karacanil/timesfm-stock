# Plan: from forecasting research to a paper-trading system

Drafted November 9, 2026. This is a development plan, not investment advice. Nothing here places real-money orders until the go-live gate in Phase 4 is passed and you decide to cross it.

## Goal

Build a small automated system that trades a **simple, well-documented trend strategy** with paper money first, runs reliably without hand-holding, controls risk, and is measured honestly against **buying and holding SPY**.

Success for the first six months means a system that runs reliably and honestly measures one strategy. Beating the market is not required. A strategy that loses to SPY but runs correctly is still a useful result, and it tells us to change the strategy, not the measuring.

## What carries over from the TimesFM study

- Never-overwritten logs (`write_new`), plus config and policy that are fixed in advance and protected by a stored hash.
- Exchange calendar handling and refusing to run on stale data.
- Scheduled GitHub Actions runs that commit their own results.
- Fixing the decision rules *before* seeing the outcomes.

The TimesFM pilot keeps running untouched until its verdict (5-session outcomes around Nov 19, 20-session outcomes around Dec 11).

## Architecture decision: one pipeline, not agents

The stages (data → signal → portfolio → risk → execution → monitoring) look like separate agents, but each is a **plain, deterministic function** with a clear input and output:

```
prices        = data.load(universe, asof)                  # adjusted daily bars
scores        = signal.trend(prices)                       # per asset
targets       = portfolio.weights(scores, prices)          # vol-scaled target weights
orders        = risk.check(targets, positions, account)    # limits, sanity, kill switch
fills         = broker.submit(orders)                      # backtest | paper | live adapter
ledger.append(asof, prices, scores, targets, orders, fills)
monitor.report(ledger)                                     # vs SPY, alerts
```

### Comparing the options

| | Single deterministic pipeline (recommended) | Multi-agent / sub-agent LLM pipeline |
|---|---|---|
| Same input → same decision | Yes, so backtest and live behave the same | No; LLM output varies between runs and model versions |
| Testable | Unit tests per stage, full replay of history | Hard; can't backtest 20 years of LLM decisions cheaply or honestly (the model has seen that history) |
| Auditable | Every number traceable in the ledger | Reasoning text, not reproducible logic |
| Cost and latency | Free, seconds | API cost every run, more failure points |
| Failure modes | Bugs (testable) | Bugs plus hallucination, prompt injection from news/web data, agents disagreeing |
| Development speed | Fast: about 500–1,000 lines of Python | Slower: orchestration, prompts, evals, guardrails |
| Where it adds value | — | Unstructured inputs (news, filings), operations review |

**Decision:** trading decisions come from code and fixed rules only. An LLM is allowed in one optional, **read-only** role later: a weekly operations reviewer that reads the ledger and logs, flags anomalies (missing data, positions that don't match the broker, drift from the backtest), and writes a summary. It cannot place or change orders.

Separately, *development* can use Claude sub-agents (for example, one writing tests while another builds the backtester). That's a choice about how we build, not part of the running system, and it adds no runtime complexity.

## Strategy v1 (to be fixed before any backtest is run)

Start with assets where trend-following is best documented and single-company risk is low: a **small universe of liquid ETFs** across asset classes. Proposed:

- US stocks (SPY), Nasdaq-100 (QQQ), US small caps (IWM), developed markets outside the US (EFA), emerging markets (EEM)
- Long-term Treasuries (TLT), intermediate Treasuries (IEF)
- Gold (GLD), US real estate (VNQ)

Rules (standard values from the published literature, not tuned on our data):

1. **Signal:** an asset is "on" if its 12-month total return excluding the latest month (12-1 momentum) is positive **and** its price is above its 200-day moving average. Otherwise "off".
2. **Sizing:** "on" assets get weights proportional to 1 / (60-day volatility), scaled so the portfolio targets about 10% annualized volatility. No leverage: gross exposure ≤ 100%. Whatever isn't invested stays in cash, or in a T-bill ETF such as BIL.
3. **Limits:** at most 25% in any one asset; long only; no shorting.
4. **Rebalance:** weekly, decided on Friday's close and executed at Monday's open. Skip any trade under 2% of equity to reduce churn.

Why weekly and end-of-day: it uses no intraday data, avoids US day-trading rules, keeps costs low, and orders can be queued overnight to execute at the open. That means GitHub Actions' multi-hour schedule delays don't matter.

v2 candidates (only after v1 has run in paper): momentum ranking across individual stocks (e.g. buy the top 20% of S&P 500 stocks by 12-1 momentum), and TimesFM *volatility* forecasts replacing the 60-day volatility in step 2.

## Phases

### Phase 1: backtester and strategy (about 1–2 weeks)

**Status (Nov 9, 2026): built; policy v1 verdict RETHINK.** See [trader-results/v1/backtest/report.md](trader-results/v1/backtest/report.md). Drawdowns were far smaller than SPY's and 60/40's (−15% vs −55% and −33%), but the Sharpe ratio was 0.48 against 0.61 for 60/40, and costs failed the bar: turnover was 636%/yr, about 70% of it from weekly signal flips (whipsaw), so cost drag was 0.64%/yr against the 0.5% limit. Any v2 is designed after seeing this period, so its backtest is weaker evidence; paper trading becomes the real test.

**Policy v2 (monthly rebalance, the only change; rules committed before it ran): PROCEED.** See [trader-results/v2/backtest/report.md](trader-results/v2/backtest/report.md). 6.45% CAGR, Sharpe 0.58, max drawdown −12%, turnover 301%/yr, cost drag 0.30%/yr; still passes with doubled costs. It still trails 60/40 on return (8.06%) and Sharpe (0.61); its value over these years was drawdown protection (2008: +5.8% vs −17.9%; 2022: −8.9% vs −16.6%), not extra return. v2 is the candidate for Phase 2 paper trading.

- New package `src/trader/` in this repo, with modules `data`, `signal`, `portfolio`, `risk`, `broker`, `ledger`, `backtest`, `cli`. Separate from `timesfm_stock`, and none of its files are touched.
- Daily, dividend-adjusted bars. Use adjusted closes for signals, which differs from the TimesFM study's raw closes on purpose.
- Backtest decision on day t's close, fill at day t+1's open, with 5 bps commission plus 5 bps slippage per trade. Tests that look for look-ahead bias (using data that wasn't available yet).
- Report: annual growth rate (CAGR), volatility, Sharpe, max drawdown, worst year, turnover, and total cost, each next to SPY buy-and-hold and a 60/40 stock/bond mix, over 2005–present and on sub-periods (2008, 2020, 2022).
- **Before running it:** record the exact rules and a pass bar in `trader_policy_v1.json`, stored with a hash just like `decision_policy.json`. The backtest is a sanity check (does it behave like the published research?), not a search for the best settings.

### Phase 2: paper-trading automation (about 1 week)

**Status (Nov 9, 2026): Phase 2a built with a simulated broker.** `python -m trader.cli paper` (config in `paper_config.json`, ledger in `paper/v2/`) settles fills, dividends and splits; reconciles the broker against the ledger; records a daily snapshot; and at each month end decides with the same code as the backtest and submits whole-share market-on-open orders. Safeguards: idempotent order IDs, all-or-nothing order checks (size, count, suspicious price moves), stale-data refusal, a `HALT` file or `TRADER_HALT` repository variable, and up to 5 sessions of catch-up if a month-end run is late. The `Paper trading` workflow runs it after each session once merged to main. A dry run replaying the Oct 30 month end on real data matched the backtest's targets exactly. Phase 2b (a real broker's paper account) waits on the broker choice.

- Broker adapter with three modes behind one interface: `backtest`, `paper`, `live`. Start with a local simulated broker, then connect a broker's paper (simulated money) API. Candidates: **Alpaca** (simple REST API, free paper accounts) or **Interactive Brokers** (wide international access, more complex API). Whether each will open an account for your country of residence must be checked before choosing.
- Orders are idempotent: a deterministic `client_order_id` per rebalance date and symbol, so a re-run can never double-submit.
- Before every run, compare broker positions with the ledger. Any mismatch halts trading and alerts.
- Kill switch: a `HALT` file in the repo or a GitHub variable, checked before any order.
- Hard sanity checks: a maximum order value, a limit price within X% of the last close, a maximum number of orders per run, and no trading if data is stale or incomplete.
- Broker API keys stored as GitHub Actions secrets. Paper keys only in this phase.

### Phase 3: paper trading (3–6 months, fixed in advance)

- Runs weekly by itself. The daily job only monitors: the ledger, equity versus SPY, drawdown, and how far realized trades drift from what the backtest would have done on the same days.
- Pre-registered review at 3 months and 6 months. Criteria: the system ran without manual fixes, paper fills match backtest assumptions within tolerance, and risk limits were never breached. Returns are reported against SPY, but **3–6 months is far too short to prove an edge**. This phase validates the machine, not the strategy.

### Phase 4: go-live gate (your decision)

- Only after Phase 3 passes. Start with an amount you can afford to lose entirely, under the same limits plus a maximum account drawdown that halts everything (e.g. −15%).
- Move scheduling from GitHub Actions to a reliable always-on host (a small VPS or your Raspberry Pi) with alerting.
- Check before funding: your country's tax treatment, the broker's rules for your account type, and the current US trading rules for small accounts.

## Open decisions for you

1. Broker: depends on what accepts your country of residence (Alpaca vs IBKR).
2. Universe: the diversified ETFs above (recommended for v1) or US stocks only.
3. Repo: a new package in this repo (recommended; reuses CI and existing tooling) or a separate repo.

## Licensing note

TimesFM 3.0 weights restrict commercial and production decision-making. The v1 strategy does not use TimesFM. Any later use of TimesFM forecasts in a real-money system needs a license check first.
