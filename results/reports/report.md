# TimesFM 3.0 forward test

Frozen forecast origins: **7**. Pending ticker/date outcomes: **952**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 168 | 1.630 | 1.511 | -7.83 | 47.6 | 83.3 |
| multivariate | 1 | 48 | 1.064 | 1.051 | -1.17 | 56.2 | 79.2 |
| multivariate | 5 | 16 | 2.225 | 2.043 | -8.92 | 37.5 | 81.2 |
| univariate | all | 168 | 1.715 | 1.511 | -13.47 | 33.3 | 82.1 |
| univariate | 1 | 48 | 1.060 | 1.051 | -0.82 | 50.0 | 81.2 |
| univariate | 5 | 16 | 2.448 | 2.043 | -19.83 | 18.8 | 81.2 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 2 | -19.83 | -13.92 |
| multivariate | INCONCLUSIVE | 2 | -8.92 | -3.55 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 2. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 2. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
