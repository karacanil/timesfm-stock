# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **1224**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2296 | 4.762 | 4.298 | -10.79 | 44.3 | 69.9 |
| multivariate | 1 | 176 | 1.647 | 1.616 | -1.94 | 53.4 | 71.6 |
| multivariate | 5 | 160 | 3.696 | 3.302 | -11.95 | 41.9 | 75.0 |
| multivariate | 20 | 40 | 8.190 | 7.299 | -12.22 | 45.0 | 70.0 |
| univariate | all | 2296 | 4.897 | 4.298 | -13.94 | 42.6 | 68.5 |
| univariate | 1 | 176 | 1.676 | 1.616 | -3.69 | 48.9 | 71.0 |
| univariate | 5 | 160 | 3.734 | 3.302 | -13.10 | 46.2 | 72.5 |
| univariate | 20 | 40 | 8.367 | 7.299 | -14.64 | 37.5 | 70.0 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 20 | -13.10 | -11.03 |
| multivariate | INCONCLUSIVE | 20 | -11.95 | -9.90 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending.
**multivariate:** Primary-horizon outcomes remain pending.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
