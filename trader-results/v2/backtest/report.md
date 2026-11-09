# Trend strategy backtest (policy v2)

Period 2006-01-03 to 2026-11-06. Decided at each month's last close, filled at the next open, 10 bps per trade (20 bps in the stress row). Dividend-adjusted Yahoo prices; cash earns the 13-week T-bill rate.

## Verdict: **PROCEED**

| Check | Result |
|---|---|
| max drawdown better than spy and 60 40 | pass |
| max drawdown above floor | pass |
| sharpe within tolerance of spy | pass |
| positive cagr each third | pass |
| cost drag within limit | pass |
| doubled costs still meets sharpe bar | pass |

Sharpe floor (SPY Sharpe minus tolerance): 0.44

## Results

| Portfolio | CAGR % | Volatility % | Sharpe | Max drawdown % | Worst year | Turnover %/yr | Cost drag %/yr |
|---|---:|---:|---:|---:|---|---:|---:|
| Trend strategy | 6.45 | 8.54 | 0.58 | -12.0 (2016-01-20) | 2022: -8.9% | 301 | 0.30 |
| Trend, 2x costs | 6.13 | 8.55 | 0.54 | -12.3 (2016-01-20) | 2022: -9.1% | 302 | 0.60 |
| SPY buy & hold | 10.79 | 19.21 | 0.54 | -55.2 (2009-03-09) | 2008: -36.8% | 5 | 0.00 |
| 60/40 SPY/IEF | 8.06 | 10.81 | 0.61 | -32.5 (2009-03-09) | 2008: -17.9% | 27 | 0.03 |

## Stress years (calendar-year return %)

| Portfolio | 2008 | 2020 | 2022 |
|---|---:|---:|---:|
| Trend strategy | 5.8 | 9.3 | -8.9 |
| Trend, 2x costs | 5.6 | 9.1 | -9.1 |
| SPY buy & hold | -36.8 | 18.3 | -18.2 |
| 60/40 SPY/IEF | -17.9 | 16.4 | -16.6 |

## CAGR by third of the period (%)

| Portfolio | First | Second | Third |
|---|---:|---:|---:|
| Trend strategy | 5.67 | 6.73 | 7.03 |
| Trend, 2x costs | 5.41 | 6.36 | 6.70 |
| SPY buy & hold | 3.83 | 14.14 | 14.81 |
| 60/40 SPY/IEF | 5.77 | 9.59 | 8.90 |

Average gross exposure: 76.2%. Rebalances fully in cash: 4.4%.

This is a sanity check of a published idea, not proof of future returns. The rules were fixed in the policy file before this backtest ran; a RETHINK verdict means changing the strategy in a new policy version, not tuning parameters until this period looks good. Yahoo adjusted prices can be revised; fractional shares are assumed; taxes are ignored.
