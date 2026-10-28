# TimesFM 3.0 forward test

Frozen forecast origins: **11**. Pending ticker/date outcomes: **3630**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1210 | 2.737 | 2.620 | -4.45 | 43.4 | 75.5 |
| multivariate | 1 | 220 | 1.430 | 1.411 | -1.37 | 46.4 | 75.5 |
| multivariate | 5 | 132 | 3.105 | 2.940 | -5.63 | 40.2 | 78.0 |
| univariate | all | 1210 | 2.726 | 2.620 | -4.05 | 45.0 | 75.0 |
| univariate | 1 | 220 | 1.436 | 1.411 | -1.77 | 45.9 | 77.7 |
| univariate | 5 | 132 | 3.067 | 2.940 | -4.33 | 46.2 | 75.0 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 12 | -10.82 |
| multivariate | Consumer Discretionary | 12 | -0.45 |
| multivariate | Consumer Staples | 12 | -4.47 |
| multivariate | Energy | 12 | -10.72 |
| multivariate | Financials | 12 | -9.83 |
| multivariate | Health Care | 12 | 18.27 |
| multivariate | Industrials | 12 | -22.03 |
| multivariate | Information Technology | 12 | -17.17 |
| multivariate | Materials | 12 | -2.50 |
| multivariate | Real Estate | 12 | -2.64 |
| multivariate | Utilities | 12 | 6.47 |
| univariate | Communication Services | 12 | -7.55 |
| univariate | Consumer Discretionary | 12 | 7.55 |
| univariate | Consumer Staples | 12 | -22.48 |
| univariate | Energy | 12 | -17.91 |
| univariate | Financials | 12 | -7.74 |
| univariate | Health Care | 12 | 22.39 |
| univariate | Industrials | 12 | -15.62 |
| univariate | Information Technology | 12 | -8.00 |
| univariate | Materials | 12 | -1.43 |
| univariate | Real Estate | 12 | 0.37 |
| univariate | Utilities | 12 | 5.77 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 6 | -4.33 | -4.99 |
| multivariate | INCONCLUSIVE | 6 | -5.63 | -6.29 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 6. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 6. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
