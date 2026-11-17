# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **1088**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 2432 | 4.889 | 4.391 | -11.36 | 44.2 | 69.9 |
| multivariate | 1 | 176 | 1.647 | 1.616 | -1.94 | 53.4 | 71.6 |
| multivariate | 5 | 168 | 3.737 | 3.307 | -13.01 | 41.1 | 75.6 |
| multivariate | 20 | 48 | 8.380 | 7.426 | -12.85 | 43.8 | 68.8 |
| univariate | all | 2432 | 5.028 | 4.391 | -14.51 | 42.8 | 68.4 |
| univariate | 1 | 176 | 1.676 | 1.616 | -3.69 | 48.9 | 71.0 |
| univariate | 5 | 168 | 3.769 | 3.307 | -13.97 | 45.2 | 72.0 |
| univariate | 20 | 48 | 8.487 | 7.426 | -14.29 | 39.6 | 68.8 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 21 | -13.97 | -11.76 |
| multivariate | INCONCLUSIVE | 21 | -13.01 | -10.82 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Primary-horizon outcomes remain pending.
**multivariate:** Primary-horizon outcomes remain pending.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
