# TimesFM 3.0 forward test

Frozen forecast origins: **11**. Pending ticker/date outcomes: **1320**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 440 | 2.333 | 2.040 | -14.39 | 38.9 | 77.0 |
| multivariate | 1 | 80 | 1.153 | 1.141 | -1.13 | 52.5 | 76.2 |
| multivariate | 5 | 48 | 2.475 | 1.971 | -25.55 | 33.3 | 83.3 |
| univariate | all | 440 | 2.365 | 2.040 | -15.92 | 34.8 | 77.7 |
| univariate | 1 | 80 | 1.175 | 1.141 | -3.00 | 50.0 | 77.5 |
| univariate | 5 | 48 | 2.494 | 1.971 | -26.54 | 25.0 | 81.2 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 6 | -26.54 | -20.28 |
| multivariate | INCONCLUSIVE | 6 | -25.55 | -19.34 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 6. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 6. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
