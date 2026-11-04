# TimesFM 3.0 forward test

Frozen forecast origins: **17**. Pending ticker/date outcomes: **1632**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1088 | 3.339 | 2.934 | -13.80 | 39.2 | 73.9 |
| multivariate | 1 | 128 | 1.335 | 1.323 | -0.90 | 52.3 | 75.0 |
| multivariate | 5 | 96 | 2.847 | 2.403 | -18.46 | 35.4 | 81.2 |
| univariate | all | 1088 | 3.356 | 2.934 | -14.38 | 38.6 | 74.4 |
| univariate | 1 | 128 | 1.372 | 1.323 | -3.68 | 47.7 | 75.8 |
| univariate | 5 | 96 | 2.834 | 2.403 | -17.94 | 38.5 | 79.2 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 12 | -17.94 | -12.79 |
| multivariate | INCONCLUSIVE | 12 | -18.46 | -13.28 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 12. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 12. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
