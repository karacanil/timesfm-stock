# TimesFM 3.0 forward test

Frozen forecast origins: **9**. Pending ticker/date outcomes: **3168**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 792 | 2.529 | 2.460 | -2.83 | 44.4 | 73.0 |
| multivariate | 1 | 176 | 1.514 | 1.495 | -1.29 | 44.3 | 71.0 |
| multivariate | 5 | 88 | 2.998 | 2.809 | -6.76 | 37.5 | 78.4 |
| univariate | all | 792 | 2.545 | 2.460 | -3.47 | 44.2 | 73.5 |
| univariate | 1 | 176 | 1.530 | 1.495 | -2.32 | 42.6 | 73.9 |
| univariate | 5 | 88 | 2.953 | 2.809 | -5.13 | 46.6 | 76.1 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 8 | -10.02 |
| multivariate | Consumer Discretionary | 8 | -2.12 |
| multivariate | Consumer Staples | 8 | -4.61 |
| multivariate | Energy | 8 | -7.90 |
| multivariate | Financials | 8 | -3.33 |
| multivariate | Health Care | 8 | 22.46 |
| multivariate | Industrials | 8 | -30.79 |
| multivariate | Information Technology | 8 | -28.86 |
| multivariate | Materials | 8 | -0.63 |
| multivariate | Real Estate | 8 | -10.11 |
| multivariate | Utilities | 8 | 8.13 |
| univariate | Communication Services | 8 | -4.76 |
| univariate | Consumer Discretionary | 8 | 4.01 |
| univariate | Consumer Staples | 8 | -21.82 |
| univariate | Energy | 8 | -9.38 |
| univariate | Financials | 8 | 3.18 |
| univariate | Health Care | 8 | 29.74 |
| univariate | Industrials | 8 | -28.45 |
| univariate | Information Technology | 8 | -9.34 |
| univariate | Materials | 8 | 0.43 |
| univariate | Real Estate | 8 | -4.43 |
| univariate | Utilities | 8 | 3.97 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 4 | -5.13 | -6.30 |
| multivariate | INCONCLUSIVE | 4 | -6.76 | -7.95 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 4. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 4. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
