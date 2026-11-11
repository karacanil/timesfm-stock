# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **1680**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1840 | 4.461 | 3.997 | -11.61 | 43.4 | 68.2 |
| multivariate | 1 | 168 | 1.651 | 1.609 | -2.59 | 52.4 | 70.8 |
| multivariate | 5 | 136 | 3.604 | 3.211 | -12.23 | 42.6 | 72.1 |
| multivariate | 20 | 16 | 8.205 | 7.605 | -7.89 | 43.8 | 62.5 |
| univariate | all | 1840 | 4.583 | 3.997 | -14.67 | 40.4 | 67.4 |
| univariate | 1 | 168 | 1.686 | 1.609 | -4.76 | 47.0 | 70.8 |
| univariate | 5 | 136 | 3.692 | 3.211 | -14.96 | 44.1 | 69.9 |
| univariate | 20 | 16 | 8.294 | 7.605 | -9.06 | 43.8 | 62.5 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 17 | -14.96 | -11.94 |
| multivariate | INCONCLUSIVE | 17 | -12.23 | -9.28 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 17. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 17. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
