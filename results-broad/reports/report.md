# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **3762**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 5918 | 4.957 | 4.816 | -2.94 | 46.3 | 69.8 |
| multivariate | 1 | 484 | 1.712 | 1.660 | -3.13 | 47.9 | 73.8 |
| multivariate | 5 | 418 | 3.782 | 3.657 | -3.41 | 44.7 | 74.6 |
| multivariate | 20 | 88 | 8.714 | 8.412 | -3.59 | 40.9 | 55.7 |
| univariate | all | 5918 | 4.972 | 4.816 | -3.25 | 50.8 | 65.9 |
| univariate | 1 | 484 | 1.701 | 1.660 | -2.43 | 47.3 | 73.3 |
| univariate | 5 | 418 | 3.813 | 3.657 | -4.26 | 52.2 | 69.6 |
| univariate | 20 | 88 | 8.581 | 8.412 | -2.01 | 52.3 | 55.7 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 38 | -6.85 |
| multivariate | Consumer Discretionary | 38 | -3.20 |
| multivariate | Consumer Staples | 38 | -10.38 |
| multivariate | Energy | 38 | -2.13 |
| multivariate | Financials | 38 | -2.61 |
| multivariate | Health Care | 38 | 6.18 |
| multivariate | Industrials | 38 | -9.46 |
| multivariate | Information Technology | 38 | -6.49 |
| multivariate | Materials | 38 | 1.31 |
| multivariate | Real Estate | 38 | 2.20 |
| multivariate | Utilities | 38 | 3.37 |
| univariate | Communication Services | 38 | -9.71 |
| univariate | Consumer Discretionary | 38 | 1.43 |
| univariate | Consumer Staples | 38 | -28.28 |
| univariate | Energy | 38 | -4.04 |
| univariate | Financials | 38 | 4.05 |
| univariate | Health Care | 38 | 8.66 |
| univariate | Industrials | 38 | -7.48 |
| univariate | Information Technology | 38 | -0.99 |
| univariate | Materials | 38 | 0.09 |
| univariate | Real Estate | 38 | 0.43 |
| univariate | Utilities | 38 | -10.73 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 19 | -4.26 | -4.82 |
| multivariate | INCONCLUSIVE | 19 | -3.41 | -3.97 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 19. Too many missing or excluded primary observations.
**multivariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 19. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
