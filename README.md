# TimesFM 3.0 stock forward test

A prospective research experiment using **current Yahoo Finance daily closes** and Google's official **TimesFM 3.0** weights. Forecasts are recorded before their target sessions begin, then scored as real prices arrive. No historical backtest is presented as live performance.

## What it measures

- Eight configurable US symbols: AAPL, MSFT, GOOGL, AMZN, NVDA, JPM, XOM, SPY.
- Last **512 completed trading sessions** as input; next **20 trading sessions** as targets.
- **Univariate**: each symbol forecast independently.
- **Multivariate**: all symbols forecast jointly with native cross-series attention.
- Point forecasts (median), nine quantiles, and a **last-price baseline**.
- Reports at 1, 5, and 20 sessions, plus all available horizons: normalized MAE/RMSE, skill versus baseline, direction accuracy, 80% interval coverage, interval width, and quantile pinball loss.

Twenty sessions is roughly a month; five is roughly a week. These are exchange sessions, not calendar days. Default XNYS sessions also suit this US watchlist's Nasdaq listings. Other exchanges require a matching calendar and homogeneous watchlist. Daily bars are not real-time intraday quotes.

## Start locally

Python 3.11+ (3.12 recommended):

```bash
git clone https://github.com/karacanil/timesfm-stock.git
cd timesfm-stock
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e '.[model]'
python -m timesfm_stock.cli daily
```

First run downloads the 330M-parameter model from Hugging Face. A CPU is supported; a CUDA GPU can be selected with `"device": "cuda"` in config.json. CPU time and memory depend on the number of symbols/context length; reduce the watchlist/context if needed. Set OMP_NUM_THREADS and MKL_NUM_THREADS to suit your machine. You need network access to Yahoo Finance, Hugging Face, and GitHub during installation.

Commands:

```bash
python -m timesfm_stock.cli forecast  # Freeze one forecast per completed origin
python -m timesfm_stock.cli evaluate  # Fetch realized closes; no model needed
python -m timesfm_stock.cli report    # Rebuild reports offline
python -m timesfm_stock.cli daily     # Evaluate, forecast, report
```

Repeat `daily` after the US close (default: one-hour publication buffer). Running before the next market open is required. A rerun for the same origin never changes the saved forecast. Market holidays/weekends create no additional origin. Missing latest data fails the run instead of quietly forecasting from stale data.

## Run automatically on GitHub

The **Daily forward test** workflow starts on the initial code push (and later code/config changes), and runs Tuesday–Saturday at **01:17 UTC / 04:17 Istanbul**, after US weekday sessions. It can also be started from **Actions → Daily forward test → Run workflow**. Scheduling begins after this workflow is committed to the default branch; GitHub may delay scheduled runs. No API secrets are required for public checkpoint/Yahoo access. GitHub Actions must be enabled and the repository must allow its GITHUB_TOKEN to write contents. If repository rules block direct pushes, run locally and commit results yourself.

Every run commits snapshots and reports to `results/`, and uploads an artifact. Check workflow logs for failures; a missed origin is not recreated later and mislabeled as prospective.

New forecast collection stops **30 calendar days after the first successful forecast** (`collection_days` in config.json). Evaluation continues afterward so the last 20-session forecasts can mature—roughly another month. Disable the workflow once all outcomes have matured. For a short pilot, set collection_days to 7 **before the first forecast**. To change tickers/settings later, start a new output directory, e.g. `--output results-study-2`; the default workflow operates on `results/`.

## Inspect results

- `results/experiment.json`: fixed configuration, exact weight revision, collection window.
- `results/runs/YYYY-MM-DD.json`: issue time, prices actually used, history hash, model/code versions, target dates, both modes' forecasts and quantiles.
- `results/observations/<origin>/<symbol>/<date>.json`: first-observed realized close or split exclusion. Never overwritten.
- `results/reports/report.md`: readable overview.
- `results/reports/summary.csv`: per-symbol and pooled metrics.
- `results/reports/predictions.csv`: individual scored forecasts and baseline.

All errors are normalized by each origin's last close, so high-price stocks do not dominate the pooled scores. **Positive skill** means lower MAE than predicting the last close; negative skill means TimesFM did worse. Exact zero-move ties are included in direction accuracy. The model's q10–q90 interval has nominal 80% coverage; empirical coverage may be very different. All-horizon totals mix short and long targets, so inspect horizon-specific scores too. N counts overlapping ticker/origin/target outcomes, not independent samples.

## Data and experimental boundaries

Yahoo requests retry up to three times with bounded delays. Yahoo Finance is suitable for an exploratory personal study, but can have missing/revised data and rate limits. Its historical daily `Close` is split-adjusted and **not dividend-adjusted** here (`auto_adjust=False`). The target is the provider's quoted close, not total return. Historical inputs are frozen at issue time. If a split occurs after an origin, newly observed outcomes for that origin are excluded because Yahoo may rewrite even pre-split closes; previously frozen observations remain unchanged. Outcomes use the first close obtained after the publication buffer, rather than a later revised download. No missing-session interpolation or artificial weekend bars are used.

The first experiment resolves `checkpoint_revision` to an exact Hugging Face commit and reuses it. TimesFM source is pinned to upstream commit `e51928e27119cb17bebc005be2696b75e0a9e688`. Runtime package versions are captured with each forecast; transitive dependency updates can still change runtime behavior. Model switches/settings require a separate experiment. Both modes share identical histories and evaluation dates. No fine-tuning, technical indicators, future covariates, or automated trading is included in this first experiment.

A week or month is useful for debugging and descriptive comparison, but cannot establish a persistent investment advantage. Daily forecast horizons overlap and stocks are correlated. Any later trading study needs explicit execution timing, costs, slippage, and longer untouched evaluation periods.

## Model license

This project is for **non-commercial, non-production research**. TimesFM 3.0 weights have a [separate restrictive license](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE), including restrictions on commercial decision-making. No model weights are committed or redistributed. The upstream source is Apache 2.0. See [upstream documentation](https://github.com/google-research/timesfm) and Yahoo's applicable data terms before extending the study.

## Tests

```bash
pip install -e .
python -m unittest discover -s tests -v
```

Offline tests cover exchange sessions/holidays/early closes, unfinished bars, missing data, immutable forecasts and outcomes, experiment configuration, split handling, metric calculations, and late-issued forecasts. CI runs these without model downloads. Real network/inference checks require the model extra and external services.
