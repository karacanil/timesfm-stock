# TimesFM 3.0 forward test

Frozen forecast origins: **20**. Pending ticker/date outcomes: **4620**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 4180 | 4.764 | 4.624 | -3.04 | 46.3 | 67.8 |
| multivariate | 1 | 418 | 1.805 | 1.757 | -2.72 | 47.6 | 70.8 |
| multivariate | 5 | 330 | 3.984 | 3.829 | -4.05 | 43.6 | 71.5 |
| univariate | all | 4180 | 4.770 | 4.624 | -3.16 | 49.4 | 64.5 |
| univariate | 1 | 418 | 1.798 | 1.757 | -2.35 | 45.7 | 70.8 |
| univariate | 5 | 330 | 4.000 | 3.829 | -4.48 | 51.5 | 67.0 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 30 | -11.08 |
| multivariate | Consumer Discretionary | 30 | -2.53 |
| multivariate | Consumer Staples | 30 | -6.85 |
| multivariate | Energy | 30 | -0.22 |
| multivariate | Financials | 30 | -1.80 |
| multivariate | Health Care | 30 | 7.72 |
| multivariate | Industrials | 30 | -13.63 |
| multivariate | Information Technology | 30 | -6.64 |
| multivariate | Materials | 30 | 0.47 |
| multivariate | Real Estate | 30 | 2.32 |
| multivariate | Utilities | 30 | 2.09 |
| univariate | Communication Services | 30 | -14.09 |
| univariate | Consumer Discretionary | 30 | 5.32 |
| univariate | Consumer Staples | 30 | -25.16 |
| univariate | Energy | 30 | -4.58 |
| univariate | Financials | 30 | 3.36 |
| univariate | Health Care | 30 | 10.29 |
| univariate | Industrials | 30 | -7.94 |
| univariate | Information Technology | 30 | -6.18 |
| univariate | Materials | 30 | -0.89 |
| univariate | Real Estate | 30 | 1.61 |
| univariate | Utilities | 30 | -7.04 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 15 | -4.48 | -4.43 |
| multivariate | INCONCLUSIVE | 15 | -4.05 | -4.00 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 15. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 15. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
