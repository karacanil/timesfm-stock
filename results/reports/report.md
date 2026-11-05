# TimesFM 3.0 forward test

Frozen forecast origins: **18**. Pending ticker/date outcomes: **1656**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1224 | 3.582 | 3.184 | -12.49 | 40.4 | 71.9 |
| multivariate | 1 | 136 | 1.521 | 1.502 | -1.28 | 52.2 | 70.6 |
| multivariate | 5 | 104 | 3.041 | 2.607 | -16.64 | 36.5 | 77.9 |
| univariate | all | 1224 | 3.619 | 3.184 | -13.65 | 39.5 | 72.1 |
| univariate | 1 | 136 | 1.550 | 1.502 | -3.18 | 47.8 | 72.1 |
| univariate | 5 | 104 | 3.049 | 2.607 | -16.96 | 37.5 | 76.0 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 13 | -16.96 | -12.48 |
| multivariate | INCONCLUSIVE | 13 | -16.64 | -12.17 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 13. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 13. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
