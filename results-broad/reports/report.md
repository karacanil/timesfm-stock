# TimesFM 3.0 forward test

Frozen forecast origins: **21**. Pending ticker/date outcomes: **4620**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 4620 | 4.896 | 4.752 | -3.03 | 46.2 | 67.9 |
| multivariate | 1 | 440 | 1.768 | 1.709 | -3.42 | 47.0 | 71.8 |
| multivariate | 5 | 352 | 3.970 | 3.826 | -3.77 | 44.6 | 71.3 |
| multivariate | 20 | 22 | 9.502 | 9.335 | -1.78 | 50.0 | 54.5 |
| univariate | all | 4620 | 4.904 | 4.752 | -3.20 | 49.7 | 64.4 |
| univariate | 1 | 440 | 1.760 | 1.709 | -2.96 | 45.2 | 71.8 |
| univariate | 5 | 352 | 3.982 | 3.826 | -4.10 | 52.3 | 66.5 |
| univariate | 20 | 22 | 9.366 | 9.335 | -0.33 | 50.0 | 50.0 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 32 | -10.61 |
| multivariate | Consumer Discretionary | 32 | -2.58 |
| multivariate | Consumer Staples | 32 | -7.36 |
| multivariate | Energy | 32 | 0.60 |
| multivariate | Financials | 32 | -1.40 |
| multivariate | Health Care | 32 | 7.68 |
| multivariate | Industrials | 32 | -13.93 |
| multivariate | Information Technology | 32 | -6.12 |
| multivariate | Materials | 32 | 1.17 |
| multivariate | Real Estate | 32 | 2.93 |
| multivariate | Utilities | 32 | 1.60 |
| univariate | Communication Services | 32 | -13.56 |
| univariate | Consumer Discretionary | 32 | 5.45 |
| univariate | Consumer Staples | 32 | -24.92 |
| univariate | Energy | 32 | -4.50 |
| univariate | Financials | 32 | 4.23 |
| univariate | Health Care | 32 | 11.60 |
| univariate | Industrials | 32 | -8.86 |
| univariate | Information Technology | 32 | -4.38 |
| univariate | Materials | 32 | 0.29 |
| univariate | Real Estate | 32 | 1.61 |
| univariate | Utilities | 32 | -7.44 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 16 | -4.10 | -4.13 |
| multivariate | INCONCLUSIVE | 16 | -3.77 | -3.81 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 16. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 16. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
