# TimesFM 3.0 forward test

Frozen forecast origins: **16**. Pending ticker/date outcomes: **1600**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 960 | 3.196 | 2.816 | -13.50 | 38.8 | 74.6 |
| multivariate | 1 | 120 | 1.335 | 1.314 | -1.61 | 52.5 | 74.2 |
| multivariate | 5 | 88 | 2.737 | 2.291 | -19.45 | 35.2 | 84.1 |
| univariate | all | 960 | 3.196 | 2.816 | -13.50 | 38.8 | 75.6 |
| univariate | 1 | 120 | 1.369 | 1.314 | -4.19 | 46.7 | 75.0 |
| univariate | 5 | 88 | 2.728 | 2.291 | -19.06 | 36.4 | 81.8 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 11 | -19.06 | -14.15 |
| multivariate | INCONCLUSIVE | 11 | -19.45 | -14.52 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 11. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 11. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
