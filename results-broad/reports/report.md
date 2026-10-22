# TimesFM 3.0 forward test

Frozen forecast origins: **7**. Pending ticker/date outcomes: **2618**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 462 | 1.877 | 1.844 | -1.80 | 45.0 | 81.0 |
| multivariate | 1 | 132 | 1.278 | 1.252 | -2.13 | 43.9 | 76.5 |
| multivariate | 5 | 44 | 2.704 | 2.612 | -3.55 | 34.1 | 79.5 |
| univariate | all | 462 | 1.918 | 1.844 | -4.01 | 42.0 | 80.5 |
| univariate | 1 | 132 | 1.296 | 1.252 | -3.53 | 40.2 | 78.0 |
| univariate | 5 | 44 | 2.730 | 2.612 | -4.55 | 45.5 | 77.3 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 4 | -7.14 |
| multivariate | Consumer Discretionary | 4 | -7.86 |
| multivariate | Consumer Staples | 4 | -4.31 |
| multivariate | Energy | 4 | 1.19 |
| multivariate | Financials | 4 | 2.61 |
| multivariate | Health Care | 4 | 29.13 |
| multivariate | Industrials | 4 | -29.65 |
| multivariate | Information Technology | 4 | 0.71 |
| multivariate | Materials | 4 | 0.64 |
| multivariate | Real Estate | 4 | -8.39 |
| multivariate | Utilities | 4 | 4.25 |
| univariate | Communication Services | 4 | -2.86 |
| univariate | Consumer Discretionary | 4 | 0.25 |
| univariate | Consumer Staples | 4 | -17.28 |
| univariate | Energy | 4 | -14.95 |
| univariate | Financials | 4 | 15.89 |
| univariate | Health Care | 4 | 34.45 |
| univariate | Industrials | 4 | -31.29 |
| univariate | Information Technology | 4 | 6.63 |
| univariate | Materials | 4 | -0.54 |
| univariate | Real Estate | 4 | -4.65 |
| univariate | Utilities | 4 | -12.66 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 2 | -4.55 | -6.42 |
| multivariate | INCONCLUSIVE | 2 | -3.55 | -5.40 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 2. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 2. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
