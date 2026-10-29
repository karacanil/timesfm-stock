# TimesFM 3.0 forward test

Frozen forecast origins: **12**. Pending ticker/date outcomes: **3828**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1452 | 2.765 | 2.649 | -4.38 | 44.6 | 77.5 |
| multivariate | 1 | 242 | 1.380 | 1.363 | -1.31 | 47.1 | 77.3 |
| multivariate | 5 | 154 | 3.106 | 2.949 | -5.33 | 39.6 | 78.6 |
| univariate | all | 1452 | 2.745 | 2.649 | -3.63 | 45.8 | 76.4 |
| univariate | 1 | 242 | 1.381 | 1.363 | -1.35 | 47.5 | 79.3 |
| univariate | 5 | 154 | 3.073 | 2.949 | -4.21 | 44.8 | 75.3 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 14 | -11.78 |
| multivariate | Consumer Discretionary | 14 | -0.08 |
| multivariate | Consumer Staples | 14 | -2.78 |
| multivariate | Energy | 14 | -11.44 |
| multivariate | Financials | 14 | -6.42 |
| multivariate | Health Care | 14 | 15.11 |
| multivariate | Industrials | 14 | -19.25 |
| multivariate | Information Technology | 14 | -14.57 |
| multivariate | Materials | 14 | -3.15 |
| multivariate | Real Estate | 14 | -3.96 |
| multivariate | Utilities | 14 | 5.35 |
| univariate | Communication Services | 14 | -9.74 |
| univariate | Consumer Discretionary | 14 | 7.48 |
| univariate | Consumer Staples | 14 | -19.54 |
| univariate | Energy | 14 | -18.78 |
| univariate | Financials | 14 | -2.50 |
| univariate | Health Care | 14 | 18.35 |
| univariate | Industrials | 14 | -14.65 |
| univariate | Information Technology | 14 | -8.27 |
| univariate | Materials | 14 | -1.45 |
| univariate | Real Estate | 14 | -0.03 |
| univariate | Utilities | 14 | 4.71 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 7 | -4.21 | -4.62 |
| multivariate | INCONCLUSIVE | 7 | -5.33 | -5.73 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 7. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 7. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
