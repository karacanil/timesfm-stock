# TimesFM 3.0 forward test

Frozen forecast origins: **14**. Pending ticker/date outcomes: **4158**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2002 | 3.373 | 3.242 | -4.04 | 44.1 | 74.6 |
| multivariate | 1 | 286 | 1.547 | 1.506 | -2.68 | 46.2 | 74.8 |
| multivariate | 5 | 198 | 3.299 | 3.160 | -4.38 | 41.4 | 78.3 |
| univariate | all | 2002 | 3.339 | 3.242 | -3.01 | 46.2 | 72.9 |
| univariate | 1 | 286 | 1.544 | 1.506 | -2.53 | 44.4 | 75.9 |
| univariate | 5 | 198 | 3.273 | 3.160 | -3.57 | 48.0 | 74.2 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 18 | -8.86 |
| multivariate | Consumer Discretionary | 18 | -4.66 |
| multivariate | Consumer Staples | 18 | 3.49 |
| multivariate | Energy | 18 | -11.99 |
| multivariate | Financials | 18 | -0.04 |
| multivariate | Health Care | 18 | 10.22 |
| multivariate | Industrials | 18 | -14.15 |
| multivariate | Information Technology | 18 | -11.91 |
| multivariate | Materials | 18 | -2.75 |
| multivariate | Real Estate | 18 | 2.75 |
| multivariate | Utilities | 18 | 2.57 |
| univariate | Communication Services | 18 | -10.34 |
| univariate | Consumer Discretionary | 18 | 5.90 |
| univariate | Consumer Staples | 18 | -13.02 |
| univariate | Energy | 18 | -20.18 |
| univariate | Financials | 18 | 4.29 |
| univariate | Health Care | 18 | 13.71 |
| univariate | Industrials | 18 | -7.96 |
| univariate | Information Technology | 18 | -7.44 |
| univariate | Materials | 18 | -0.87 |
| univariate | Real Estate | 18 | 2.47 |
| univariate | Utilities | 18 | -0.00 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 9 | -3.57 | -4.21 |
| multivariate | INCONCLUSIVE | 9 | -4.38 | -5.03 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 9. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 9. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
