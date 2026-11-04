# Day 05 — Time, Precision, Returns

**Theme:** Handle dates and time zones correctly, respect floating point, and compute returns and drawdowns the way a risk team would check them.
**Time budget:** ~6–7 h
**Save to:** `solutions/day05/`

---

## Track A — Python: `datetime`, `zoneinfo`, floats, `decimal`

- **P5.1 [E]** Parse `"2025-03-03 08:30:00"` as Chicago time with `zoneinfo`. Convert to UTC, London and Dhaka.
- **P5.2 [E]** Days to expiry: calendar days and weekday-only business days (loop skipping weekends) from today to a given expiry.
- **P5.3 [M]** List the UTC time of the 08:30 Chicago open for every Monday in March 2025. Observe the jump at the DST change. In 3–4 sentences, explain why storing naive local times breaks joins across venues.
- **P5.4 [M]** Implement `cl_expiry(year, month)` for the CL rule: trading ends 3 business days before the 25th calendar day of the month *before* delivery; if the 25th isn't a business day, count from the business day before it. The dataset uses the US federal holiday calendar (`pandas.tseries.holiday.USFederalHolidayCalendar`), so use the same holidays. Check your function against every contract in `futures_cl.parquet` — all must match.
- **P5.5 [M]** Floating point: show `0.1 + 0.2 != 0.3`; add `0.01` one million times vs `math.fsum`; use `math.isclose` with relative and absolute tolerances. When is each tolerance appropriate?
- **P5.6 [H]** PnL accounting with `Decimal` (prices quantized to the tick, fees in cents) vs `float` over 1,000,000 random fills. How large does float drift get? Where would it matter?
- **P5.7 [P]** `TradingCalendar` class: holidays, `is_trading_day`, `next_trading_day`, `prev_trading_day`, `trading_days_between`, `session_open_utc(date)` / `session_close_utc(date)` for a given exchange time zone (DST-aware). Tests around both DST transitions and around Christmas/New Year.

## Track B — NumPy: cumulative operations, returns, drawdown, NaN

- **N5.1 [E]** Simple and log returns with `np.diff`. Verify `sum(log returns) == log(P_T / P_0)`.
- **N5.2 [E]** Equity curve with `np.cumprod(1 + r)`. Check the final value against `P_T / P_0`.
- **N5.3 [M]** Maximum drawdown with `np.maximum.accumulate`. Then the longest underwater period (number of days below a prior peak), vectorized.
- **N5.4 [M]** Compound daily simple returns into monthly returns; do the same with log returns. Show with numbers why *averaging simple returns across time* overstates growth, while *averaging simple returns across assets* is exactly right for an equal-weight portfolio.
- **N5.5 [M]** Inject NaNs. Compare `mean` vs `nanmean`, and watch `cumprod` break. Fix by filling *returns* (not prices) with 0 and explain what that assumes economically.
- **N5.6 [H]** Calmar, Sortino (downside deviation), and Ulcer Index from scratch, vectorized for all 12 assets.
- **N5.7 [P]** `drawdown_table(equity, top_n=5)`: the top 5 drawdowns with peak index, trough index, recovery index (or `None`), depth and length. Vectorize the core; a short loop to separate episodes is fine. Validate on a hand-built equity curve where you know the answer.

## Track C — pandas: DatetimeIndex, time zones, calendars, returns

- **D5.1 [E]** Wide closes with a `DatetimeIndex`: partial-string slicing `"2020"`, `"2020-03":"2020-05"`.
- **D5.2 [E]** Add `year`, `month`, `weekday`, `quarter` columns via the `.dt` accessor (on the long panel).
- **D5.3 [M]** `ticks_trades.parquet` is in UTC. Convert to `America/Chicago`, set as index, and use `between_time("08:30", "09:00")` to count opening-half-hour trades per day.
- **D5.4 [M]** `pct_change` and log returns for the wide frame. Annualized mean, vol and Sharpe per symbol. Compare with your NumPy `summary_stats` from Day 3 (must match).
- **D5.5 [M]** Build `CustomBusinessDay(calendar=USFederalHolidayCalendar())` dates for 2015–2025. Compare against the panel's dates: list dates present in one but not the other.
- **D5.6 [H]** Create one Series with naive Chicago timestamps and one with UTC timestamps for the same events. Try to join them, observe the failure or silent mismatch, and fix it properly.
- **D5.7 [P]** `returns_report(closes) -> pd.DataFrame`: daily/weekly/monthly compounded returns, annualized stats, worst month, best year, max drawdown — one tidy table, one row per symbol. Unit tests comparing with your NumPy functions.

---

## Interview drill
1. Why store timestamps in UTC?
2. Log returns or simple returns: which add across time, which add across assets?
3. A strategy has 20% annual return and a 40% max drawdown. What is its Calmar ratio?

## Done when
- [ ] `TradingCalendar` and `drawdown_table` tested
- [ ] Committed: `day05: time zones, precision, returns & drawdowns`
- [ ] **Tomorrow is Capstone 1** — skim `capstones/capstone1_data_quality_toolkit.md` tonight
