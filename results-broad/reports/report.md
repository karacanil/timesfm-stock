# TimesFM 3.0 forward test

Frozen forecast origins: **17**. Pending ticker/date outcomes: **4488**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2992 | 4.242 | 4.110 | -3.22 | 45.1 | 69.9 |
| multivariate | 1 | 352 | 1.776 | 1.721 | -3.16 | 45.2 | 70.5 |
| multivariate | 5 | 264 | 3.779 | 3.656 | -3.37 | 43.6 | 72.7 |
| univariate | all | 2992 | 4.226 | 4.110 | -2.83 | 47.5 | 67.2 |
| univariate | 1 | 352 | 1.773 | 1.721 | -3.00 | 43.8 | 70.7 |
| univariate | 5 | 264 | 3.792 | 3.656 | -3.73 | 49.6 | 69.3 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 24 | -8.75 |
| multivariate | Consumer Discretionary | 24 | -2.93 |
| multivariate | Consumer Staples | 24 | -2.82 |
| multivariate | Energy | 24 | -3.90 |
| multivariate | Financials | 24 | 2.59 |
| multivariate | Health Care | 24 | 8.15 |
| multivariate | Industrials | 24 | -8.57 |
| multivariate | Information Technology | 24 | -9.67 |
| multivariate | Materials | 24 | -1.73 |
| multivariate | Real Estate | 24 | 2.03 |
| multivariate | Utilities | 24 | 3.70 |
| univariate | Communication Services | 24 | -11.43 |
| univariate | Consumer Discretionary | 24 | 5.04 |
| univariate | Consumer Staples | 24 | -20.34 |
| univariate | Energy | 24 | -9.99 |
| univariate | Financials | 24 | 7.76 |
| univariate | Health Care | 24 | 12.49 |
| univariate | Industrials | 24 | -4.89 |
| univariate | Information Technology | 24 | -10.19 |
| univariate | Materials | 24 | -0.87 |
| univariate | Real Estate | 24 | 1.68 |
| univariate | Utilities | 24 | -3.01 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 12 | -3.73 | -3.98 |
| multivariate | INCONCLUSIVE | 12 | -3.37 | -3.62 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 12. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 12. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
