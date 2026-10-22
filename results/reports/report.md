# TimesFM 3.0 forward test

Frozen forecast origins: **8**. Pending ticker/date outcomes: **1056**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 224 | 1.605 | 1.496 | -7.28 | 49.1 | 84.4 |
| multivariate | 1 | 56 | 1.026 | 1.017 | -0.88 | 55.4 | 80.4 |
| multivariate | 5 | 24 | 1.974 | 1.728 | -14.20 | 45.8 | 83.3 |
| univariate | all | 224 | 1.691 | 1.496 | -13.00 | 34.8 | 83.0 |
| univariate | 1 | 56 | 1.029 | 1.017 | -1.20 | 50.0 | 80.4 |
| univariate | 5 | 24 | 2.166 | 1.728 | -25.33 | 25.0 | 83.3 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 3 | -25.33 | -21.05 |
| multivariate | INCONCLUSIVE | 3 | -14.20 | -10.29 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 3. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 3. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
