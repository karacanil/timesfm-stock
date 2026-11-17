# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **3366**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 6314 | 4.978 | 4.821 | -3.27 | 46.1 | 70.4 |
| multivariate | 1 | 484 | 1.712 | 1.660 | -3.13 | 47.9 | 73.8 |
| multivariate | 5 | 440 | 3.720 | 3.581 | -3.89 | 44.1 | 75.9 |
| multivariate | 20 | 110 | 8.759 | 8.480 | -3.28 | 43.6 | 56.4 |
| univariate | all | 6314 | 4.994 | 4.821 | -3.59 | 50.8 | 66.3 |
| univariate | 1 | 484 | 1.701 | 1.660 | -2.43 | 47.3 | 73.3 |
| univariate | 5 | 440 | 3.757 | 3.581 | -4.91 | 51.1 | 70.9 |
| univariate | 20 | 110 | 8.633 | 8.480 | -1.80 | 52.7 | 55.5 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 40 | -8.02 |
| multivariate | Consumer Discretionary | 40 | -1.89 |
| multivariate | Consumer Staples | 40 | -11.50 |
| multivariate | Energy | 40 | -3.45 |
| multivariate | Financials | 40 | -4.17 |
| multivariate | Health Care | 40 | 5.83 |
| multivariate | Industrials | 40 | -10.46 |
| multivariate | Information Technology | 40 | -6.75 |
| multivariate | Materials | 40 | 1.14 |
| multivariate | Real Estate | 40 | 2.48 |
| multivariate | Utilities | 40 | 3.84 |
| univariate | Communication Services | 40 | -10.56 |
| univariate | Consumer Discretionary | 40 | 2.10 |
| univariate | Consumer Staples | 40 | -29.11 |
| univariate | Energy | 40 | -3.88 |
| univariate | Financials | 40 | 2.32 |
| univariate | Health Care | 40 | 7.24 |
| univariate | Industrials | 40 | -8.79 |
| univariate | Information Technology | 40 | -1.36 |
| univariate | Materials | 40 | 0.31 |
| univariate | Real Estate | 40 | 0.50 |
| univariate | Utilities | 40 | -12.84 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 20 | -4.91 | -5.52 |
| multivariate | INCONCLUSIVE | 20 | -3.89 | -4.49 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending.
**multivariate:** Primary-horizon outcomes remain pending.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
