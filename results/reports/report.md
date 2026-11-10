# TimesFM 3.0 forward test

Frozen forecast origins: **21**. Pending ticker/date outcomes: **1680**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 1680 | 4.266 | 3.807 | -12.06 | 42.7 | 68.5 |
| multivariate | 1 | 160 | 1.656 | 1.624 | -2.02 | 53.1 | 70.0 |
| multivariate | 5 | 128 | 3.478 | 3.057 | -13.76 | 41.4 | 73.4 |
| multivariate | 20 | 8 | 7.716 | 6.964 | -10.81 | 37.5 | 62.5 |
| univariate | all | 1680 | 4.371 | 3.807 | -14.82 | 39.9 | 68.1 |
| univariate | 1 | 160 | 1.687 | 1.624 | -3.90 | 47.5 | 70.0 |
| univariate | 5 | 128 | 3.571 | 3.057 | -16.80 | 42.2 | 71.1 |
| univariate | 20 | 8 | 7.643 | 6.964 | -9.75 | 50.0 | 62.5 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 16 | -16.80 | -13.22 |
| multivariate | INCONCLUSIVE | 16 | -13.76 | -10.27 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 16. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 16. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
