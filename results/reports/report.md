# TimesFM 3.0 forward test

Frozen forecast origins: **15**. Pending ticker/date outcomes: **1560**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 840 | 2.920 | 2.561 | -14.02 | 39.4 | 77.0 |
| multivariate | 1 | 112 | 1.307 | 1.283 | -1.84 | 52.7 | 75.0 |
| multivariate | 5 | 80 | 2.568 | 2.114 | -21.52 | 36.2 | 86.2 |
| univariate | all | 840 | 2.918 | 2.561 | -13.93 | 39.2 | 78.1 |
| univariate | 1 | 112 | 1.323 | 1.283 | -3.12 | 47.3 | 75.9 |
| univariate | 5 | 80 | 2.548 | 2.114 | -20.53 | 35.0 | 83.8 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 10 | -20.53 | -15.85 |
| multivariate | INCONCLUSIVE | 10 | -21.52 | -16.80 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 10. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 10. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
