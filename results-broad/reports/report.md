# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **4180**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 5500 | 4.953 | 4.811 | -2.95 | 46.2 | 69.1 |
| multivariate | 1 | 484 | 1.712 | 1.660 | -3.13 | 47.9 | 73.8 |
| multivariate | 5 | 396 | 3.802 | 3.674 | -3.50 | 44.9 | 73.7 |
| multivariate | 20 | 66 | 8.915 | 8.590 | -3.77 | 40.9 | 53.0 |
| univariate | all | 5500 | 4.966 | 4.811 | -3.21 | 50.5 | 65.3 |
| univariate | 1 | 484 | 1.701 | 1.660 | -2.43 | 47.3 | 73.3 |
| univariate | 5 | 396 | 3.838 | 3.674 | -4.46 | 51.5 | 69.2 |
| univariate | 20 | 66 | 8.745 | 8.590 | -1.80 | 53.0 | 54.5 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 36 | -7.31 |
| multivariate | Consumer Discretionary | 36 | -3.09 |
| multivariate | Consumer Staples | 36 | -9.20 |
| multivariate | Energy | 36 | -1.47 |
| multivariate | Financials | 36 | -2.80 |
| multivariate | Health Care | 36 | 6.37 |
| multivariate | Industrials | 36 | -11.04 |
| multivariate | Information Technology | 36 | -6.43 |
| multivariate | Materials | 36 | 1.02 |
| multivariate | Real Estate | 36 | 2.62 |
| multivariate | Utilities | 36 | 3.05 |
| univariate | Communication Services | 36 | -10.85 |
| univariate | Consumer Discretionary | 36 | 2.44 |
| univariate | Consumer Staples | 36 | -27.58 |
| univariate | Energy | 36 | -4.57 |
| univariate | Financials | 36 | 3.08 |
| univariate | Health Care | 36 | 9.22 |
| univariate | Industrials | 36 | -7.86 |
| univariate | Information Technology | 36 | -2.22 |
| univariate | Materials | 36 | -0.60 |
| univariate | Real Estate | 36 | -0.29 |
| univariate | Utilities | 36 | -9.37 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 18 | -4.46 | -4.79 |
| multivariate | INCONCLUSIVE | 18 | -3.50 | -3.82 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 18. Too many missing or excluded primary observations.
**multivariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 18. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
