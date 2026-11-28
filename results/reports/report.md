# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **288**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 3232 | 6.026 | 5.220 | -15.44 | 41.0 | 65.4 |
| multivariate | 1 | 176 | 1.647 | 1.616 | -1.94 | 53.4 | 71.6 |
| multivariate | 5 | 176 | 3.772 | 3.320 | -13.59 | 40.3 | 76.1 |
| multivariate | 20 | 112 | 10.084 | 8.737 | -15.42 | 33.9 | 50.9 |
| univariate | all | 3232 | 6.150 | 5.220 | -17.81 | 41.3 | 63.6 |
| univariate | 1 | 176 | 1.676 | 1.616 | -3.69 | 48.9 | 71.0 |
| univariate | 5 | 176 | 3.795 | 3.320 | -14.30 | 44.9 | 72.2 |
| univariate | 20 | 112 | 10.302 | 8.737 | -17.92 | 37.5 | 53.6 |

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**NO_GO** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | NO_GO | 22 | -14.30 | -11.99 |
| multivariate | NO_GO | 22 | -13.59 | -11.30 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** last_price: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. drift: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. At least one baseline comparison excludes the required 5.0% gain in both block checks.
**multivariate:** last_price: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. drift: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. At least one baseline comparison excludes the required 5.0% gain in both block checks.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
