# TimesFM 3.0 forward test

Frozen forecast origins: **14**. Pending ticker/date outcomes: **1512**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 728 | 2.553 | 2.240 | -13.97 | 41.5 | 80.2 |
| multivariate | 1 | 104 | 1.246 | 1.231 | -1.19 | 51.9 | 77.9 |
| multivariate | 5 | 72 | 2.454 | 2.008 | -22.16 | 37.5 | 86.1 |
| univariate | all | 728 | 2.563 | 2.240 | -14.42 | 39.6 | 80.6 |
| univariate | 1 | 104 | 1.260 | 1.231 | -2.35 | 48.1 | 78.8 |
| univariate | 5 | 72 | 2.443 | 2.008 | -21.62 | 33.3 | 83.3 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 9 | -21.62 | -17.06 |
| multivariate | INCONCLUSIVE | 9 | -22.16 | -17.58 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 9. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 9. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
