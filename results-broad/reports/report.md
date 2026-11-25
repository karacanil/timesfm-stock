# TimesFM 3.0 forward test

Frozen forecast origins: **22**. Pending ticker/date outcomes: **1452**. Split exclusions: **0**.

Errors are normalized by the price at the forecast origin. Baseline predicts that price at every horizon. Positive skill means lower MAE than the baseline. Coverage measures the q10–q90 interval (nominal 80%).

| Mode | Horizon (sessions) | N | MAE % | Baseline MAE % | Skill % | Direction % | Coverage % |
|---|---:|---:|---:|---:|---:|---:|---:|
| multivariate | all | 8228 | 5.095 | 4.847 | -5.12 | 46.0 | 72.6 |
| multivariate | 1 | 484 | 1.712 | 1.660 | -3.13 | 47.9 | 73.8 |
| multivariate | 5 | 484 | 3.600 | 3.463 | -3.96 | 43.6 | 77.5 |
| multivariate | 20 | 242 | 8.290 | 7.845 | -5.68 | 42.1 | 61.6 |
| univariate | all | 8228 | 5.141 | 4.847 | -6.07 | 50.1 | 67.8 |
| univariate | 1 | 484 | 1.701 | 1.660 | -2.43 | 47.3 | 73.3 |
| univariate | 5 | 484 | 3.664 | 3.463 | -5.82 | 49.6 | 72.7 |
| univariate | 20 | 242 | 8.320 | 7.845 | -6.05 | 48.8 | 58.3 |

## Sector diagnostics (5-session horizon)

| Mode | Sector | N | Skill vs last price % |
|---|---|---:|---:|
| multivariate | Communication Services | 44 | -8.71 |
| multivariate | Consumer Discretionary | 44 | -0.78 |
| multivariate | Consumer Staples | 44 | -11.89 |
| multivariate | Energy | 44 | -4.14 |
| multivariate | Financials | 44 | -5.33 |
| multivariate | Health Care | 44 | 5.72 |
| multivariate | Industrials | 44 | -11.32 |
| multivariate | Information Technology | 44 | -6.09 |
| multivariate | Materials | 44 | 2.33 |
| multivariate | Real Estate | 44 | 1.86 |
| multivariate | Utilities | 44 | 4.85 |
| univariate | Communication Services | 44 | -11.58 |
| univariate | Consumer Discretionary | 44 | 1.60 |
| univariate | Consumer Staples | 44 | -31.85 |
| univariate | Energy | 44 | -4.41 |
| univariate | Financials | 44 | 0.31 |
| univariate | Health Care | 44 | 5.55 |
| univariate | Industrials | 44 | -10.09 |
| univariate | Information Technology | 44 | -1.36 |
| univariate | Materials | 44 | 1.44 |
| univariate | Real Estate | 44 | 0.80 |
| univariate | Utilities | 44 | -15.71 |

Sector results are exploratory diagnostics; they do not replace the fixed pooled primary endpoint.

N counts ticker/origin/target outcomes, not independent observations. Daily forecasts overlap; one month provides descriptive evidence, not proof of a persistent trading advantage. Direction compares movement from the origin, including exact zero-move ties. Prices are Yahoo Close, not dividend-adjusted total returns. First-observed actuals are frozen; provider corrections may differ later.

See summary.csv for per-symbol scores and predictions.csv for individual outcomes.

## Pilot decision

**NO_GO** — primary horizon: 5 trading sessions.

PROMISING supports a new untouched confirmation experiment before strategy research. NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.

| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |
|---|---|---:|---:|---:|
| univariate | NO_GO | 22 | -5.82 | -6.08 |
| multivariate | NO_GO | 22 | -3.96 | -4.22 |

Approximate paired block intervals use 98.75% confidence per comparison (adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. With a short pilot these intervals remain fragile, and cross-regime reliability is untested.

**univariate:** last_price: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. drift: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. At least one baseline comparison excludes the required 5.0% gain in both block checks.
**multivariate:** last_price: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. drift: failed checks: at_least_5pct_improvement, positive_lower_interval_both_blocks, wins_on_most_symbols, positive_skill_both_halves, positive_skill_after_removing_any_symbol. At least one baseline comparison excludes the required 5.0% gain in both block checks.

See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.
