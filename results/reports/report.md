# TimesFM 3.0 forward test

Frozen forecast origins: **10**. Pending ticker/date outcomes: **1240**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 360 | 2.209 | 1.965 | -12.44 | 40.8 | 76.9 |
| multivariate | 1 | 72 | 1.166 | 1.146 | -1.76 | 51.4 | 75.0 |
| multivariate | 5 | 40 | 2.390 | 1.920 | -24.49 | 35.0 | 82.5 |
| univariate | all | 360 | 2.255 | 1.965 | -14.76 | 34.2 | 77.2 |
| univariate | 1 | 72 | 1.182 | 1.146 | -3.15 | 47.2 | 76.4 |
| univariate | 5 | 40 | 2.428 | 1.920 | -26.48 | 25.0 | 82.5 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 5 | -26.48 | -20.69 |
| multivariate | INCONCLUSIVE | 5 | -24.49 | -18.78 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 5. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 5. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
