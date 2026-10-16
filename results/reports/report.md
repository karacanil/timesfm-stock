# TimesFM 3.0 forward test

Frozen forecast origins: **4**. Pending ticker/date outcomes: **592**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 48 | 1.206 | 1.160 | -3.99 | 50.0 | 87.5 |
| multivariate | 1 | 24 | 0.971 | 0.941 | -3.12 | 58.3 | 83.3 |
| univariate | all | 48 | 1.243 | 1.160 | -7.19 | 41.7 | 85.4 |
| univariate | 1 | 24 | 0.968 | 0.941 | -2.84 | 50.0 | 83.3 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 0 | n/a | n/a |
| multivariate | INCONCLUSIVE | 0 | n/a | n/a |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** No complete primary-horizon origins yet.
**multivariate:** No complete primary-horizon origins yet.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
