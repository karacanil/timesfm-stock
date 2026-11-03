# TimesFM 3.0 forward test

Frozen forecast origins: **15**. Pending ticker/date outcomes: **4290**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2310 | 3.651 | 3.522 | -3.67 | 44.5 | 73.3 |
| multivariate | 1 | 308 | 1.593 | 1.548 | -2.87 | 45.8 | 74.0 |
| multivariate | 5 | 220 | 3.426 | 3.295 | -3.98 | 42.7 | 77.3 |
| univariate | all | 2310 | 3.621 | 3.522 | -2.83 | 46.6 | 71.2 |
| univariate | 1 | 308 | 1.596 | 1.548 | -3.09 | 43.5 | 75.0 |
| univariate | 5 | 220 | 3.415 | 3.295 | -3.64 | 48.2 | 73.6 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 20 | -8.66 |
| multivariate | Consumer Discretionary | 20 | -3.83 |
| multivariate | Consumer Staples | 20 | 1.51 |
| multivariate | Energy | 20 | -9.96 |
| multivariate | Financials | 20 | 1.70 |
| multivariate | Health Care | 20 | 9.79 |
| multivariate | Industrials | 20 | -11.61 |
| multivariate | Information Technology | 20 | -11.62 |
| multivariate | Materials | 20 | -2.38 |
| multivariate | Real Estate | 20 | 2.95 |
| multivariate | Utilities | 20 | 3.24 |
| univariate | Communication Services | 20 | -11.01 |
| univariate | Consumer Discretionary | 20 | 6.14 |
| univariate | Consumer Staples | 20 | -16.70 |
| univariate | Energy | 20 | -16.61 |
| univariate | Financials | 20 | 6.39 |
| univariate | Health Care | 20 | 13.42 |
| univariate | Industrials | 20 | -6.08 |
| univariate | Information Technology | 20 | -9.53 |
| univariate | Materials | 20 | -1.11 |
| univariate | Real Estate | 20 | 2.63 |
| univariate | Utilities | 20 | -1.04 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 10 | -3.64 | -4.14 |
| multivariate | INCONCLUSIVE | 10 | -3.98 | -4.48 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 10. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 10. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
