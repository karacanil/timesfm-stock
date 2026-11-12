# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **4620**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 5060 | 4.959 | 4.813 | -3.02 | 46.1 | 68.3 |
| multivariate | 1 | 462 | 1.734 | 1.678 | -3.30 | 47.2 | 72.9 |
| multivariate | 5 | 374 | 3.843 | 3.701 | -3.84 | 44.4 | 72.7 |
| multivariate | 20 | 44 | 9.441 | 9.210 | -2.51 | 45.5 | 54.5 |
| univariate | all | 5060 | 4.966 | 4.813 | -3.18 | 50.2 | 64.7 |
| univariate | 1 | 462 | 1.725 | 1.678 | -2.79 | 46.3 | 72.7 |
| univariate | 5 | 374 | 3.878 | 3.701 | -4.78 | 51.3 | 68.2 |
| univariate | 20 | 44 | 9.321 | 9.210 | -1.21 | 52.3 | 52.3 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 34 | -9.28 |
| multivariate | Consumer Discretionary | 34 | -2.57 |
| multivariate | Consumer Staples | 34 | -9.36 |
| multivariate | Energy | 34 | 0.54 |
| multivariate | Financials | 34 | -2.90 |
| multivariate | Health Care | 34 | 6.39 |
| multivariate | Industrials | 34 | -13.70 |
| multivariate | Information Technology | 34 | -6.48 |
| multivariate | Materials | 34 | 0.88 |
| multivariate | Real Estate | 34 | 2.62 |
| multivariate | Utilities | 34 | 2.70 |
| univariate | Communication Services | 34 | -13.00 |
| univariate | Consumer Discretionary | 34 | 3.66 |
| univariate | Consumer Staples | 34 | -27.83 |
| univariate | Energy | 34 | -4.18 |
| univariate | Financials | 34 | 2.14 |
| univariate | Health Care | 34 | 9.49 |
| univariate | Industrials | 34 | -8.72 |
| univariate | Information Technology | 34 | -3.96 |
| univariate | Materials | 34 | -0.79 |
| univariate | Real Estate | 34 | 0.80 |
| univariate | Utilities | 34 | -8.56 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 17 | -4.78 | -4.90 |
| multivariate | INCONCLUSIVE | 17 | -3.84 | -3.96 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 17. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 17. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
