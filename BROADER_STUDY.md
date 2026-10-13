# Broader stock forecasting study

Declared **October 13, 2026**, before any target outcome from the original pilot has completed. This is a parallel breadth study, not a future-period confirmation experiment. It changes the research universe, while keeping the forecast method, context, horizon, baselines, and decision policy fixed.

## Research universe

Two companies per major US sector, selected for business/size variety and a sufficiently long price history. The labels are research sector buckets based on business activities; they are not a claim of a complete point-in-time GICS database. Smaller peers are relative complements, not a fixed market-cap category. This is a deliberately selected sample, not a random sample of all listed stocks.

| Sector | Larger company | Complementary company |
|---|---|---|
| Information Technology | Apple (AAPL) | Texas Instruments (TXN) |
| Communication Services | Alphabet (GOOGL) | Fox (FOXA) |
| Consumer Discretionary | Amazon (AMZN) | Harley-Davidson (HOG) |
| Consumer Staples | Procter & Gamble (PG) | J. M. Smucker (SJM) |
| Health Care | Johnson & Johnson (JNJ) | Baxter (BAX) |
| Financials | JPMorgan Chase (JPM) | Assurant (AIZ) |
| Industrials | Caterpillar (CAT) | GATX (GATX) |
| Energy | Exxon Mobil (XOM) | Ovintiv (OVV) |
| Utilities | NextEra Energy (NEE) | OGE Energy (OGE) |
| Materials | Linde (LIN) | Sonoco (SON) |
| Real Estate | Prologis (PLD) | Kilroy Realty (KRC) |

There are **22 individual stocks, no ETFs**. SPY remains an index control in the original pilot. Equal numbers per sector give each sector equal pooled weight when the panels are complete. Outcomes remain correlated; sector balance does not create 22 independent market experiments.

Company/ticker reference examples: [Harley-Davidson](https://investor.harley-davidson.com/overview/default.aspx), [Sonoco](https://investor.sonoco.com/overview/default.aspx), [Kilroy Realty](https://investors.kilroyrealty.com/ir-home/default.aspx). [S&P sector definitions](https://www.spglobal.com/spdji/en/landing/investment-themes/sectors/) describe the sector framework. The initial data preflight verifies all 22 ticker histories against completed sessions; missing histories fail explicitly, and stocks are not silently replaced based on model outcomes.

## Settings and isolation

- `config-broad.json` defines this universe and its sector mapping.
- Outputs live exclusively in **results-broad/**.
- Original configuration, policy, snapshots, and outcomes remain in results/.
- Same 512-session context, 20-session horizon, raw-close target policy, and both forecasting modes.
- Same exact Hugging Face weight revision as the original pilot: `43046b85ec22d584a13f8098c2ed39c889e129c2`.
- Same 30-calendar-day collection period, beginning with the first successful forecast; scoring continues afterward.
- Same [decision policy](EVALUATION.md). The 62.5% stock-breadth threshold means **at least 14 of 22 stocks** must improve against each baseline. Readiness still requires at least 20 complete origins and 90% completeness among saved origins.

## Automated and manual execution

The GitHub workflow has three daily opportunities (04:17, 06:47, and 09:17 Istanbul, Tuesday–Saturday) and runs both studies, preserving each study's output even if the other fails. The broader study's initial preflight downloads no model and only verifies historical data coverage. A successful preflight is saved at results-broad/preflight.json; it does not start the collection clock or issue a prediction.

```bash
python -m timesfm_stock.cli preflight --config config-broad.json --output results-broad
python -m timesfm_stock.cli daily --config config-broad.json --output results-broad
```

During an already-open target session, forecasting safely waits for the next finalized close. No earlier forecast is fabricated. The first scheduled broader forecast is expected on **October 14 at about 04:17 Istanbul**, using October 13's completed US close, if the workflow/provider succeed. Dates remain provisional until results-broad/experiment.json exists.

## Reporting

- results-broad/reports/report.md: pooled scores, sector diagnostics, pilot decision and reasons.
- results-broad/reports/summary.csv: individual-stock and pooled scores.
- results-broad/reports/sector_summary.csv: scores by sector, mode, and 1/5/20-session horizon.
- results-broad/reports/decision.json: fixed primary decision with paired block uncertainty and consistency checks.

Sector breakdowns are exploratory; do not change the primary endpoint or cherry-pick a successful sector as evidence of broad utility. The two studies should be discussed separately, not pooled into a larger sample (they overlap in stocks/dates). Joint forecasts also depend on the universe composition; differences from the original pilot are not solely a ticker selection effect.

## What this adds—and what it cannot establish

It makes the pilot less dominated by technology-related megacaps and tests whether improvement is spread across businesses with different exposures. It remains a selected, US-listed, survivorship-conditioned universe over one short period. A meaningful gain here still requires confirmation on a fresh untouched period before strategy research. No trading, portfolio allocation, or investment recommendations are produced.
