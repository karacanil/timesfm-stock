# TimesFM 3.0 forward test

Frozen forecast origins: **13**. Pending ticker/date outcomes: **4004**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1716 | 3.075 | 2.957 | -4.00 | 44.5 | 76.2 |
| multivariate | 1 | 264 | 1.523 | 1.502 | -1.40 | 46.6 | 75.0 |
| multivariate | 5 | 176 | 3.233 | 3.078 | -5.06 | 39.8 | 78.4 |
| univariate | all | 1716 | 3.044 | 2.957 | -2.93 | 46.1 | 74.7 |
| univariate | 1 | 264 | 1.530 | 1.502 | -1.87 | 45.5 | 76.5 |
| univariate | 5 | 176 | 3.181 | 3.078 | -3.36 | 46.6 | 75.6 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 16 | -9.22 |
| multivariate | Consumer Discretionary | 16 | -4.44 |
| multivariate | Consumer Staples | 16 | 3.65 |
| multivariate | Energy | 16 | -12.06 |
| multivariate | Financials | 16 | -3.31 |
| multivariate | Health Care | 16 | 12.40 |
| multivariate | Industrials | 16 | -17.04 |
| multivariate | Information Technology | 16 | -12.80 |
| multivariate | Materials | 16 | -2.08 |
| multivariate | Real Estate | 16 | -3.14 |
| multivariate | Utilities | 16 | 2.46 |
| univariate | Communication Services | 16 | -9.92 |
| univariate | Consumer Discretionary | 16 | 5.76 |
| univariate | Consumer Staples | 16 | -7.41 |
| univariate | Energy | 16 | -18.89 |
| univariate | Financials | 16 | 0.33 |
| univariate | Health Care | 16 | 16.04 |
| univariate | Industrials | 16 | -11.16 |
| univariate | Information Technology | 16 | -7.34 |
| univariate | Materials | 16 | -0.36 |
| univariate | Real Estate | 16 | 1.78 |
| univariate | Utilities | 16 | 1.64 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 8 | -3.36 | -3.91 |
| multivariate | INCONCLUSIVE | 8 | -5.06 | -5.62 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 8. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 8. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
