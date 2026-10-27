# TimesFM 3.0 forward test

Frozen forecast origins: **10**. Pending ticker/date outcomes: **3410**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 990 | 2.676 | 2.578 | -3.80 | 43.4 | 73.6 |
| multivariate | 1 | 198 | 1.448 | 1.431 | -1.21 | 46.0 | 73.7 |
| multivariate | 5 | 110 | 3.090 | 2.924 | -5.71 | 39.1 | 77.3 |
| univariate | all | 990 | 2.676 | 2.578 | -3.81 | 44.3 | 73.8 |
| univariate | 1 | 198 | 1.459 | 1.431 | -1.94 | 44.9 | 76.3 |
| univariate | 5 | 110 | 3.064 | 2.924 | -4.80 | 46.4 | 74.5 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 10 | -10.75 |
| multivariate | Consumer Discretionary | 10 | -0.33 |
| multivariate | Consumer Staples | 10 | -5.86 |
| multivariate | Energy | 10 | -8.16 |
| multivariate | Financials | 10 | -7.74 |
| multivariate | Health Care | 10 | 21.03 |
| multivariate | Industrials | 10 | -25.53 |
| multivariate | Information Technology | 10 | -23.37 |
| multivariate | Materials | 10 | -1.58 |
| multivariate | Real Estate | 10 | -2.21 |
| multivariate | Utilities | 10 | 7.34 |
| univariate | Communication Services | 10 | -6.02 |
| univariate | Consumer Discretionary | 10 | 6.50 |
| univariate | Consumer Staples | 10 | -25.05 |
| univariate | Energy | 10 | -14.72 |
| univariate | Financials | 10 | -3.74 |
| univariate | Health Care | 10 | 24.39 |
| univariate | Industrials | 10 | -20.13 |
| univariate | Information Technology | 10 | -9.10 |
| univariate | Materials | 10 | -0.46 |
| univariate | Real Estate | 10 | 0.11 |
| univariate | Utilities | 10 | 5.64 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 5 | -4.80 | -5.67 |
| multivariate | INCONCLUSIVE | 5 | -5.71 | -6.59 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 5. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 5. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
