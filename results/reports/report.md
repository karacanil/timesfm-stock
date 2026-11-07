# TimesFM 3.0 forward test

Frozen forecast origins: **20**. Pending ticker/date outcomes: **1680**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1520 | 4.061 | 3.603 | -12.70 | 42.0 | 69.1 |
| multivariate | 1 | 152 | 1.612 | 1.585 | -1.74 | 53.3 | 71.7 |
| multivariate | 5 | 120 | 3.344 | 2.898 | -15.37 | 39.2 | 75.0 |
| univariate | all | 1520 | 4.151 | 3.603 | -15.19 | 39.1 | 68.9 |
| univariate | 1 | 152 | 1.643 | 1.585 | -3.68 | 48.0 | 71.7 |
| univariate | 5 | 120 | 3.432 | 2.898 | -18.40 | 39.2 | 72.5 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 15 | -18.40 | -14.10 |
| multivariate | INCONCLUSIVE | 15 | -15.37 | -11.17 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 15. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 15. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
