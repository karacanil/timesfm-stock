# How we will decide whether to continue with TimesFM

Policy version 1 was recorded on **October 13, 2026, before the first target session completed**. Forecast settings and previously issued predictions are unchanged. These are practical pilot thresholds we chose in advance, not universal measures of forecasting quality.

## Primary question

Do either of TimesFM 3.0's two modes improve **5-trading-day price forecasts** enough to justify further research? Evaluate univariate and multivariate separately, on the same complete origin/symbol panels. One-day and twenty-day results, directional scores, and quantile scores are supporting evidence, not alternative endpoints to pick if the primary result disappoints.

The target is Yahoo daily Close. Errors are divided by the price at each origin and then averaged with equal weight per symbol/origin.

Two baselines use only the saved input history:

1. **Last price:** forecast the last observed close at every horizon.
2. **Drift:** extrapolate the average per-session price change over the same input window: `last + horizon * (last - first) / (context_length - 1)`.

Drift is reconstructed deterministically from already frozen histories; it does not use realized target prices or fitted test-period parameters. No earlier forecast is rewritten.

## Readiness before any final pilot verdict

- The 30-day collection window has ended.
- All issued 5-session targets are observed or explicitly excluded.
- At least **20 forecast origins** have valid outcomes for **all configured symbols**.
- At least **90% of saved origins** form complete panels. Missing scheduled runs are also visible in Actions/history; this fraction alone does not measure scheduler uptime.

Until these conditions hold, the decision is INCONCLUSIVE and scores are interim. A panel excludes an entire origin if any symbol's primary target is missing/excluded. This keeps the comparison universe constant; ordinary score tables can contain more partially observed rows.

## PROMISING: advance to untouched confirmation

A mode must pass every condition against **both** baselines:

- At least **5% lower normalized mean absolute error**.
- Lower uncertainty bound for skill is above zero with **both 5-origin and 10-origin block resampling**.
- Positive skill for at least **62.5% of configured symbols**, rounded up: **5 of 8** in the original pilot, **14 of 22** in the broader study.
- Positive skill in **both chronological halves** of complete origins.
- Positive pooled skill after removing **any one symbol**.

This supports spending time on a new confirmation study; it does not establish profitable trading or persistent reliability.

## NO_GO: deprioritize this setup

Once readiness holds, a mode is NO_GO if, against at least one baseline, the **upper** skill bound is below the required 5% improvement with both block sizes. That means the required practical advantage is not supported under this pilot's uncertainty model—even if the point estimate is slightly positive.

If both modes are NO_GO, deprioritize this configuration and investigate a different forecasting approach. This is a conclusion about this dataset, input/target policy, and evaluation period, not every possible use of TimesFM.

## INCONCLUSIVE: gather more untouched evidence

Anything else is INCONCLUSIVE: an uncertain gain, insufficient outcomes, unstable results across stocks/time, zero baseline error, or excessive exclusions. Do not promote an inconclusive result to a pass. A short study can legitimately end without a definitive answer.

## Uncertainty method and its limits

Use a paired circular moving-block bootstrap, with **5,000 resamples** and a fixed seed. Every resampled origin includes the entire stock panel. This retains cross-stock dependence and local serial dependence instead of pretending that hundreds of overlapping predictions are independent observations. Check block sizes 5 and 10, and require both to support a decision.

The family confidence target is 95%. For two modes and two baselines, each percentile interval is **98.75%**, using a Bonferroni adjustment. This reduces the risk of selecting an apparent winner among comparisons; it does not make the inference exact. With about one month of origins, there are only a few independent blocks, and intervals can be fragile. The bootstrap assumes the observed error process is informative about similar future periods; it cannot establish performance across unseen market regimes.

## Supporting evidence

- RMSE and baseline RMSE expose large mistakes that MAE can hide.
- Direction accuracy is accompanied by **always up**, **always down**, and **historical-majority direction** benchmarks. Historical majority uses only frozen context, with the same target horizon and an up tie-break. No test outcomes are used to choose it.
- Empirical q10–q90 coverage should be considered together with interval width and quantile pinball loss. Wide intervals alone are not useful evidence. These checks do not claim probabilistic superiority over a calibrated probabilistic baseline, which this version does not yet include.
- Compare joint and independent modes, but report both even if only one passes.

## After the pilot

If PROMISING, select the candidate using this pilot and evaluate it on a **fresh, untouched period** with fixed settings. That confirmation should be longer and cover additional market conditions. Only after the forecasting advantage repeats should we build and assess trading rules in a separate study with executable entry timing, transaction costs, slippage, turnover, drawdowns, and paper trading.

If NO_GO, investigate another method. If INCONCLUSIVE, extend evidence collection through a new experiment with the same policy, without optimizing settings against this pilot's outcomes. Downloaded TimesFM 3.0 weights also retain their non-commercial/non-production restrictions; a successful research result does not change the license.

## Files

- `decision_policy.json`: declared policy.
- `results/decision_policy.json`: immutable copy used for the experiment. Reports reject changed thresholds.
- `results/reports/decision.json`: machine-readable verdict, policy hash, checks, skills, uncertainty intervals, per-stock/half-period/leave-one-out results.
- `results/reports/report.md`: readable verdict and reasons alongside ordinary scores.

Collection settings remain in config.json for the original pilot and config-broad.json for the separate broader study. The same policy is frozen independently in each output directory. Do not change this policy after seeing outcomes; a different policy requires a separate, explicitly labeled experiment.
