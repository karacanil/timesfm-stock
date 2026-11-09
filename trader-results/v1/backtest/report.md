# Trend strategy backtest (policy v1)

Period 2006-01-03 to 2026-11-06. Decided at each week's last close, filled at the next open, 10 bps per trade (20 bps in the stress row). Dividend-adjusted Yahoo prices; cash earns the 13-week T-bill rate.

## Verdict: **RETHINK**

| Check | Result |
|---|---|
| max drawdown better than spy and 60 40 | pass |
| max drawdown above floor | pass |
| sharpe within tolerance of spy | pass |
| positive cagr each third | pass |
| cost drag within limit | FAIL |
| doubled costs still meets sharpe bar | FAIL |

Sharpe floor (SPY Sharpe minus tolerance): 0.44

## Results

| Portfolio | CAGR % | Volatility % | Sharpe | Max drawdown % | Worst year | Turnover %/yr | Cost drag %/yr |
|---|---:|---:|---:|---:|---|---:|---:|
| Trend strategy | 5.49 | 8.29 | 0.48 | -15.0 (2016-04-26) | 2018: -8.9% | 636 | 0.64 |
| Trend, 2x costs | 4.82 | 8.29 | 0.40 | -16.1 (2016-04-26) | 2018: -9.5% | 636 | 1.27 |
| SPY buy & hold | 10.79 | 19.21 | 0.54 | -55.2 (2009-03-09) | 2008: -36.8% | 5 | 0.00 |
| 60/40 SPY/IEF | 8.06 | 10.81 | 0.61 | -32.5 (2009-03-09) | 2008: -17.9% | 27 | 0.03 |

## Stress years (calendar-year return %)

| Portfolio | 2008 | 2020 | 2022 |
|---|---:|---:|---:|
| Trend strategy | 6.4 | 7.8 | -7.1 |
| Trend, 2x costs | 5.8 | 7.3 | -7.4 |
| SPY buy & hold | -36.8 | 18.3 | -18.2 |
| 60/40 SPY/IEF | -17.9 | 16.4 | -16.6 |

## CAGR by third of the period (%)

| Portfolio | First | Second | Third |
|---|---:|---:|---:|
| Trend strategy | 4.64 | 4.66 | 7.23 |
| Trend, 2x costs | 4.06 | 3.89 | 6.58 |
| SPY buy & hold | 3.83 | 14.14 | 14.81 |
| 60/40 SPY/IEF | 5.77 | 9.59 | 8.90 |

Average gross exposure: 75.9%. Rebalances fully in cash: 4.9%.

This is a sanity check of a published idea, not proof of future returns. The rules were fixed in the policy file before this backtest ran; a RETHINK verdict means changing the strategy in a new policy version, not tuning parameters until this period looks good. Yahoo adjusted prices can be revised; fractional shares are assumed; taxes are ignored.
