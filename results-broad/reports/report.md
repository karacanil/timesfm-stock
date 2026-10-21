# TimesFM 3.0 forward test

Frozen forecast origins: **6**. Pending ticker/date outcomes: **2310**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 330 | 1.912 | 1.904 | -0.44 | 47.0 | 77.6 |
| multivariate | 1 | 110 | 1.336 | 1.318 | -1.37 | 46.4 | 74.5 |
| multivariate | 5 | 22 | 3.055 | 3.169 | 3.59 | 50.0 | 68.2 |
| univariate | all | 330 | 1.978 | 1.904 | -3.92 | 39.1 | 77.6 |
| univariate | 1 | 110 | 1.372 | 1.318 | -4.06 | 36.4 | 76.4 |
| univariate | 5 | 22 | 3.214 | 3.169 | -1.42 | 54.5 | 68.2 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 2 | -6.53 |
| multivariate | Consumer Discretionary | 2 | 10.82 |
| multivariate | Consumer Staples | 2 | -2.10 |
| multivariate | Energy | 2 | 3.48 |
| multivariate | Financials | 2 | 18.42 |
| multivariate | Health Care | 2 | 23.25 |
| multivariate | Industrials | 2 | -15.21 |
| multivariate | Information Technology | 2 | 44.08 |
| multivariate | Materials | 2 | -0.36 |
| multivariate | Real Estate | 2 | -4.07 |
| multivariate | Utilities | 2 | 21.12 |
| univariate | Communication Services | 2 | -1.87 |
| univariate | Consumer Discretionary | 2 | 16.90 |
| univariate | Consumer Staples | 2 | -12.87 |
| univariate | Energy | 2 | -18.09 |
| univariate | Financials | 2 | 32.14 |
| univariate | Health Care | 2 | 15.00 |
| univariate | Industrials | 2 | -16.98 |
| univariate | Information Technology | 2 | 16.83 |
| univariate | Materials | 2 | -4.30 |
| univariate | Real Estate | 2 | 2.45 |
| univariate | Utilities | 2 | -9.36 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 1 | -1.42 | -3.43 |
| multivariate | INCONCLUSIVE | 1 | 3.59 | 1.67 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 1. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 1. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
