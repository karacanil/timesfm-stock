# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **2992**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 6688 | 4.981 | 4.806 | -3.65 | 45.9 | 71.0 |
| multivariate | 1 | 484 | 1.712 | 1.660 | -3.13 | 47.9 | 73.8 |
| multivariate | 5 | 462 | 3.642 | 3.504 | -3.95 | 44.2 | 76.6 |
| multivariate | 20 | 132 | 8.680 | 8.369 | -3.71 | 42.4 | 57.6 |
| univariate | all | 6688 | 5.001 | 4.806 | -4.05 | 50.7 | 66.9 |
| univariate | 1 | 484 | 1.701 | 1.660 | -2.43 | 47.3 | 73.3 |
| univariate | 5 | 462 | 3.685 | 3.504 | -5.17 | 50.6 | 71.9 |
| univariate | 20 | 132 | 8.571 | 8.369 | -2.41 | 51.5 | 57.6 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 42 | -8.41 |
| multivariate | Consumer Discretionary | 42 | -1.04 |
| multivariate | Consumer Staples | 42 | -11.76 |
| multivariate | Energy | 42 | -3.91 |
| multivariate | Financials | 42 | -5.32 |
| multivariate | Health Care | 42 | 5.68 |
| multivariate | Industrials | 42 | -11.10 |
| multivariate | Information Technology | 42 | -6.23 |
| multivariate | Materials | 42 | 1.85 |
| multivariate | Real Estate | 42 | 2.01 |
| multivariate | Utilities | 42 | 4.38 |
| univariate | Communication Services | 42 | -10.71 |
| univariate | Consumer Discretionary | 42 | 2.44 |
| univariate | Consumer Staples | 42 | -30.40 |
| univariate | Energy | 42 | -3.15 |
| univariate | Financials | 42 | 1.32 |
| univariate | Health Care | 42 | 6.06 |
| univariate | Industrials | 42 | -9.33 |
| univariate | Information Technology | 42 | -1.43 |
| univariate | Materials | 42 | 0.61 |
| univariate | Real Estate | 42 | 0.43 |
| univariate | Utilities | 42 | -14.55 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 21 | -5.17 | -5.62 |
| multivariate | INCONCLUSIVE | 21 | -3.95 | -4.39 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending.
**multivariate:** Primary-horizon outcomes remain pending.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
