# TimesFM 3.0 forward test

Frozen forecast origins: **19**. Pending ticker/date outcomes: **4598**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 3762 | 4.593 | 4.455 | -3.11 | 46.2 | 68.4 |
| multivariate | 1 | 396 | 1.771 | 1.727 | -2.56 | 48.0 | 72.5 |
| multivariate | 5 | 308 | 3.990 | 3.837 | -4.00 | 44.2 | 71.1 |
| univariate | all | 3762 | 4.598 | 4.455 | -3.22 | 48.7 | 65.2 |
| univariate | 1 | 396 | 1.769 | 1.727 | -2.41 | 45.7 | 72.2 |
| univariate | 5 | 308 | 4.024 | 3.837 | -4.89 | 50.3 | 66.6 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 28 | -13.01 |
| multivariate | Consumer Discretionary | 28 | -2.45 |
| multivariate | Consumer Staples | 28 | -5.48 |
| multivariate | Energy | 28 | -0.17 |
| multivariate | Financials | 28 | -1.67 |
| multivariate | Health Care | 28 | 8.60 |
| multivariate | Industrials | 28 | -12.27 |
| multivariate | Information Technology | 28 | -7.00 |
| multivariate | Materials | 28 | 0.73 |
| multivariate | Real Estate | 28 | 2.75 |
| multivariate | Utilities | 28 | 2.73 |
| univariate | Communication Services | 28 | -16.36 |
| univariate | Consumer Discretionary | 28 | 5.00 |
| univariate | Consumer Staples | 28 | -23.05 |
| univariate | Energy | 28 | -5.14 |
| univariate | Financials | 28 | 3.83 |
| univariate | Health Care | 28 | 10.07 |
| univariate | Industrials | 28 | -8.10 |
| univariate | Information Technology | 28 | -7.27 |
| univariate | Materials | 28 | -0.82 |
| univariate | Real Estate | 28 | 2.10 |
| univariate | Utilities | 28 | -5.74 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 14 | -4.89 | -4.83 |
| multivariate | INCONCLUSIVE | 14 | -4.00 | -3.94 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 14. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 14. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
