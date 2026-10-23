# TimesFM 3.0 forward test

Frozen forecast origins: **9**. Pending ticker/date outcomes: **1152**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 288 | 1.885 | 1.721 | -9.57 | 46.5 | 80.2 |
| multivariate | 1 | 64 | 1.165 | 1.159 | -0.50 | 54.7 | 75.0 |
| multivariate | 5 | 32 | 2.266 | 1.914 | -18.39 | 43.8 | 81.2 |
| univariate | all | 288 | 1.950 | 1.721 | -13.36 | 35.4 | 78.8 |
| univariate | 1 | 64 | 1.175 | 1.159 | -1.44 | 50.0 | 75.0 |
| univariate | 5 | 32 | 2.360 | 1.914 | -23.33 | 25.0 | 81.2 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 4 | -23.33 | -18.86 |
| multivariate | INCONCLUSIVE | 4 | -18.39 | -14.10 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 4. Too many missing or excluded primary observations.
**multivariate:** Collection window still open; results are interim. Primary-horizon outcomes remain pending. Need 20 complete origins; have 4. Too many missing or excluded primary observations.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
