# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **1368**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2152 | 4.667 | 4.202 | -11.06 | 44.0 | 69.3 |
| multivariate | 1 | 176 | 1.647 | 1.616 | -1.94 | 53.4 | 71.6 |
| multivariate | 5 | 152 | 3.652 | 3.254 | -12.25 | 42.1 | 74.3 |
| multivariate | 20 | 32 | 8.174 | 7.366 | -10.97 | 46.9 | 68.8 |
| univariate | all | 2152 | 4.799 | 4.202 | -14.20 | 41.8 | 68.1 |
| univariate | 1 | 176 | 1.676 | 1.616 | -3.69 | 48.9 | 71.0 |
| univariate | 5 | 152 | 3.702 | 3.254 | -13.77 | 44.7 | 72.4 |
| univariate | 20 | 32 | 8.316 | 7.366 | -12.89 | 40.6 | 68.8 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 19 | -13.77 | -11.24 |
| multivariate | INCONCLUSIVE | 19 | -12.25 | -9.75 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 19. Too many missing or excluded primary observations.
**multivariate:** Primary-horizon outcomes remain pending. Need 20 complete origins; have 19. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
