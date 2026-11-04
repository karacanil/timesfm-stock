# TimesFM 3.0 forward test

Frozen forecast origins: **16**. Pending ticker/date outcomes: **4400**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2640 | 3.810 | 3.681 | -3.49 | 45.2 | 73.2 |
| multivariate | 1 | 330 | 1.616 | 1.574 | -2.67 | 46.7 | 73.9 |
| multivariate | 5 | 242 | 3.472 | 3.341 | -3.90 | 43.0 | 76.9 |
| univariate | all | 2640 | 3.789 | 3.681 | -2.92 | 47.5 | 70.9 |
| univariate | 1 | 330 | 1.615 | 1.574 | -2.60 | 44.8 | 74.8 |
| univariate | 5 | 242 | 3.470 | 3.341 | -3.84 | 49.6 | 73.6 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 22 | -9.07 |
| multivariate | Consumer Discretionary | 22 | -3.34 |
| multivariate | Consumer Staples | 22 | -0.88 |
| multivariate | Energy | 22 | -6.74 |
| multivariate | Financials | 22 | 2.24 |
| multivariate | Health Care | 22 | 8.28 |
| multivariate | Industrials | 22 | -10.27 |
| multivariate | Information Technology | 22 | -10.28 |
| multivariate | Materials | 22 | -2.61 |
| multivariate | Real Estate | 22 | 2.90 |
| multivariate | Utilities | 22 | 4.07 |
| univariate | Communication Services | 22 | -11.48 |
| univariate | Consumer Discretionary | 22 | 6.23 |
| univariate | Consumer Staples | 22 | -20.29 |
| univariate | Energy | 22 | -13.38 |
| univariate | Financials | 22 | 7.69 |
| univariate | Health Care | 22 | 11.93 |
| univariate | Industrials | 22 | -5.48 |
| univariate | Information Technology | 22 | -9.89 |
| univariate | Materials | 22 | -0.84 |
| univariate | Real Estate | 22 | 2.62 |
| univariate | Utilities | 22 | -1.99 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 11 | -3.84 | -4.12 |
| multivariate | INCONCLUSIVE | 11 | -3.90 | -4.17 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 11. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 11. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
