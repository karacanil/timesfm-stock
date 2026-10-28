# TimesFM 3.0 forward test

Frozen forecast origins: **12**. Pending ticker/date outcomes: **1392**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 528 | 2.313 | 2.007 | -15.27 | 40.7 | 78.8 |
| multivariate | 1 | 88 | 1.140 | 1.133 | -0.65 | 53.4 | 77.3 |
| multivariate | 5 | 56 | 2.427 | 1.936 | -25.33 | 35.7 | 83.9 |
| univariate | all | 528 | 2.340 | 2.007 | -16.64 | 36.6 | 79.5 |
| univariate | 1 | 88 | 1.153 | 1.133 | -1.79 | 50.0 | 78.4 |
| univariate | 5 | 56 | 2.432 | 1.936 | -25.59 | 28.6 | 82.1 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 7 | -25.59 | -20.03 |
| multivariate | INCONCLUSIVE | 7 | -25.33 | -19.78 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 7. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 7. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
