# TimesFM 3.0 forward test

Frozen forecast origins: **8**. Pending ticker/date outcomes: **2904**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 616 | 2.279 | 2.242 | -1.64 | 45.6 | 74.5 |
| multivariate | 1 | 154 | 1.511 | 1.484 | -1.76 | 42.2 | 69.5 |
| multivariate | 5 | 66 | 3.005 | 2.836 | -5.95 | 36.4 | 77.3 |
| univariate | all | 616 | 2.306 | 2.242 | -2.83 | 44.0 | 74.2 |
| univariate | 1 | 154 | 1.524 | 1.484 | -2.67 | 40.9 | 72.1 |
| univariate | 5 | 66 | 2.945 | 2.836 | -3.84 | 45.5 | 74.2 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 6 | -8.49 |
| multivariate | Consumer Discretionary | 6 | -6.73 |
| multivariate | Consumer Staples | 6 | -3.89 |
| multivariate | Energy | 6 | -5.77 |
| multivariate | Financials | 6 | 0.85 |
| multivariate | Health Care | 6 | 20.18 |
| multivariate | Industrials | 6 | -26.19 |
| multivariate | Information Technology | 6 | -23.46 |
| multivariate | Materials | 6 | 0.05 |
| multivariate | Real Estate | 6 | -14.24 |
| multivariate | Utilities | 6 | 3.82 |
| univariate | Communication Services | 6 | -3.49 |
| univariate | Consumer Discretionary | 6 | 0.22 |
| univariate | Consumer Staples | 6 | -16.76 |
| univariate | Energy | 6 | -10.35 |
| univariate | Financials | 6 | 11.43 |
| univariate | Health Care | 6 | 28.12 |
| univariate | Industrials | 6 | -20.81 |
| univariate | Information Technology | 6 | -1.19 |
| univariate | Materials | 6 | 1.02 |
| univariate | Real Estate | 6 | -7.18 |
| univariate | Utilities | 6 | -0.80 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 3 | -3.84 | -5.57 |
| multivariate | INCONCLUSIVE | 3 | -5.95 | -7.71 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 3. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 3. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
