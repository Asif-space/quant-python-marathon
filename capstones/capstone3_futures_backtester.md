# Capstone 3 — Commodity Futures Signal Research & Vectorized Backtester

**Day 16 · Builds on Days 1–15 · Repo folder:** `capstones/c3_futures_research/`

## Why this project
This is the project that looks most like the job: research signals on commodity futures, backtest them honestly with costs, and prove the results aren't luck. Make this your best README.

## Inputs
- `data/raw/futures_cl.parquet` — for the CL carry/curve signal (through your `ContinuousFuture`)
- `data/raw/panel_daily.parquet` — 12 commodities for cross-asset momentum
- `data/raw/eia_weekly.csv` — event filter

## Architecture
```
c3_futures_research/
├── src/fresearch/
│   ├── data.py         # ContinuousFuture (Day 15), panel loader, leak-free features (Day 13)
│   ├── signals.py      # Signal ABC + registry (Days 9–10)
│   ├── analysis.py     # IC, quantile returns, decay
│   ├── backtest.py     # vectorized engine (+ optional Numba core from Day 14)
│   ├── costs.py        # tick-based slippage + commission models
│   ├── validation.py   # walk-forward, bootstrap, permutation, deflated Sharpe
│   └── tearsheet.py
└── tests/
```

## Requirements

### Core
1. **Signals** (all computed with information available at the close of day t, traded at t+1):
   - Time-series momentum (12-1 month and 3-month variants) on all 12 commodities
   - Cross-sectional momentum (long top tercile, short bottom tercile)
   - CL carry: annualized `ln(F1/F2)` from the curve; long backwardation, short contango
2. **Signal analysis:** daily rank IC (Spearman) and its t-stat, IC decay over 1–20 day horizons, quantile returns.
3. **Backtester:** positions → PnL with
   - volatility targeting (EWMA forecast, lagged)
   - transaction costs: half-spread in ticks × tick value + commission per contract, applied to turnover
   - gross/net leverage limits
   - outputs: daily PnL, positions, turnover, costs
4. **Validation:**
   - walk-forward parameter selection (Day 15 engine)
   - block-bootstrap Sharpe confidence interval
   - permutation test p-value
   - deflated Sharpe ratio given the number of variants you tried (**log every variant you run**)
5. **Tearsheet:** equity curve (gross vs net), drawdown, rolling Sharpe, monthly returns heatmap, turnover, cost drag, correlation between strategies.
6. ≥ 25 tests, including a look-ahead test: shifting all data forward by one day must not *improve* results; truncating data after t must not change positions at t.

### Stretch
- Combine the signals (equal-risk blend) and show diversification benefit.
- EIA filter: flatten energy positions on release days; does it help?
- Sensitivity heatmap: Sharpe vs lookback × cost level.

### Pro
- Parallel walk-forward with `ProcessPoolExecutor`.
- Numba core matching the pandas engine to 1e-10.
- Capacity estimate: PnL degradation as position size grows relative to average volume.

## Acceptance checks
- Gross and net results both reported; costs never zero.
- Every reported Sharpe has a confidence interval.
- Look-ahead tests pass.

## README must contain
- Hypothesis for each signal (economic intuition, 2–3 sentences each)
- Results table: Sharpe (CI), annual return, vol, max DD, turnover, cost drag, deflated Sharpe
- Tearsheet figures
- An honest "what could be wrong with this" section (synthetic data, overfitting risk, cost assumptions)

## Common pitfalls
- Using unadjusted front-month prices so roll gaps appear as returns.
- Vol target estimated with today's return included.
- Reporting only the best parameter set without counting trials.
