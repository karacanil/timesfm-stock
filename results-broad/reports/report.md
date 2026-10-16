# TimesFM 3.0 forward test

Frozen forecast origins: **3**. Pending ticker/date outcomes: **1254**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 66 | 1.543 | 1.576 | 2.04 | 60.6 | 75.8 |
| multivariate | 1 | 44 | 1.393 | 1.409 | 1.11 | 59.1 | 75.0 |
| univariate | all | 66 | 1.598 | 1.576 | -1.41 | 47.0 | 74.2 |
| univariate | 1 | 44 | 1.424 | 1.409 | -1.08 | 45.5 | 72.7 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**INCONCLUSIVE** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | INCONCLUSIVE | 0 | n/a | n/a |
| multivariate | INCONCLUSIVE | 0 | n/a | n/a |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** No complete primary-horizon origins yet.
**multivariate:** No complete primary-horizon origins yet.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
