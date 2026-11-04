# Day 21 — Capstone 5: Ship It + Mock Interview

The last day has two halves: turn three weeks of work into something a hiring manager can evaluate in five minutes, then test yourself under time pressure.

➡️ Part 1 spec: [`capstones/capstone5_portfolio_polish.md`](../capstones/capstone5_portfolio_polish.md)

---

## Part 2 — Timed mock interview (2 hours, no internet, no AI)

Set a timer. Write answers in `solutions/day21/mock/`. Grade yourself afterwards with your own notes.

### Section A — Python (40 min)
1. Implement `moving_average(stream, n)` as a generator that yields after every element (O(1) per step).
2. Given a list of `(start, end)` trading halts, merge overlaps and return total halted time.
3. Implement an LRU cache without `OrderedDict` (dict + doubly linked list).
4. Write a decorator `@rate_limit(calls, period)` that raises if called more often than allowed.
5. Explain, with code, a bug caused by a mutable default argument and one caused by late binding in closures.
6. Max profit with at most two transactions.
7. Design (classes + method signatures only) a `Portfolio` that supports fills, marks, and multi-currency PnL.

### Section B — NumPy (40 min)
1. Max drawdown of a price array in one line (plus imports).
2. Cross-sectional z-scores of a `(T, N)` matrix ignoring NaNs.
3. OLS β and its standard error without any regression library.
4. Rolling 20-period mean of a 1-D array without loops or pandas.
5. Simulate 10,000 correlated return paths for 3 assets given a correlation matrix.
6. Given sorted quote times and trade times, return the index of the prevailing quote for each trade.
7. Explain why `a[mask] += 1` works but `a[idx] += 1` with repeated indices doesn't add twice, and fix it with `np.add.at`.

### Section C — pandas (40 min)
1. Compute monthly returns per symbol from a long daily panel in one chain.
2. Rank assets cross-sectionally each day and form an equal-weight top-quintile portfolio with next-day returns.
3. Attach the most recent quote to each trade within 500 ms, no look-ahead.
4. Build 15-minute OHLCV bars from trades with correct labeling for a close-based signal.
5. Rolling 60-day correlation of every asset with CL, in one expression.
6. Find and explain the look-ahead bug in: `df["signal"] = df.close.pct_change() > 0; df["pnl"] = df.signal * df.close.pct_change()`.
7. Construct a ratio-adjusted continuous series from a contract table and a roll schedule.

### Scoring
- 18–21 solved correctly and cleanly: you're ready for technical screens on these libraries
- 12–17: re-do the days covering the misses within the next week
- below 12: repeat the marathon's [M] and [H] exercises before moving on

---

## Retrospective (30 min) — `notes/retrospective.md`
- Which topics still feel slow? Which exercises did you skip?
- What's the one capstone you'd show first, and why?
- Next steps: SciPy/statsmodels depth, scikit-learn + LightGBM on your feature engine, SQL integration with your financial database, C++ basics.

## Done when
- [ ] Portfolio repo polished (Capstone 5 checklist complete)
- [ ] Mock interview done and graded
- [ ] Committed: `day21: final polish, mock interview, retrospective`
