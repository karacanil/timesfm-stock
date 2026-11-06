# TimesFM 3.0 forward test

Frozen forecast origins: **18**. Pending ticker/date outcomes: **4554**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 3366 | 4.471 | 4.335 | -3.14 | 45.5 | 68.6 |
| multivariate | 1 | 374 | 1.824 | 1.773 | -2.88 | 46.5 | 70.9 |
| multivariate | 5 | 286 | 3.942 | 3.790 | -4.04 | 43.7 | 71.3 |
| univariate | all | 3366 | 4.467 | 4.335 | -3.04 | 48.0 | 65.7 |
| univariate | 1 | 374 | 1.821 | 1.773 | -2.68 | 44.9 | 70.6 |
| univariate | 5 | 286 | 3.970 | 3.790 | -4.76 | 49.3 | 67.1 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 26 | -13.01 |
| multivariate | Consumer Discretionary | 26 | -2.65 |
| multivariate | Consumer Staples | 26 | -4.28 |
| multivariate | Energy | 26 | -1.86 |
| multivariate | Financials | 26 | 0.32 |
| multivariate | Health Care | 26 | 8.63 |
| multivariate | Industrials | 26 | -10.73 |
| multivariate | Information Technology | 26 | -8.00 |
| multivariate | Materials | 26 | -0.27 |
| multivariate | Real Estate | 26 | 2.71 |
| multivariate | Utilities | 26 | 3.19 |
| univariate | Communication Services | 26 | -15.93 |
| univariate | Consumer Discretionary | 26 | 4.88 |
| univariate | Consumer Staples | 26 | -20.46 |
| univariate | Energy | 26 | -7.42 |
| univariate | Financials | 26 | 5.68 |
| univariate | Health Care | 26 | 10.25 |
| univariate | Industrials | 26 | -6.63 |
| univariate | Information Technology | 26 | -8.49 |
| univariate | Materials | 26 | -0.96 |
| univariate | Real Estate | 26 | 1.41 |
| univariate | Utilities | 26 | -4.18 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 13 | -4.76 | -4.76 |
| multivariate | INCONCLUSIVE | 13 | -4.04 | -4.04 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 13. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 13. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
