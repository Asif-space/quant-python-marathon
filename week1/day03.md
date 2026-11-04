# Day 03 — Functions, Reductions, Alignment

**Theme:** Write reusable functions, reduce arrays along the right axis, and control how pandas aligns data.
**Time budget:** ~6–7 h
**Save to:** `solutions/day03/`

---

## Track A — Python: functions, arguments, scope, closures, `functools`

- **P3.1 [E]** `annualized_vol(returns, *, periods_per_year=252, ddof=1)` in pure Python. The `*` makes the options keyword-only — explain why that's good API design.
- **P3.2 [E]** Write `add_trade(trade, blotter=[])`, demonstrate the mutable-default bug over three calls, then fix it with `None`.
- **P3.3 [E]** `log_call(func, *args, **kwargs)` prints the function name and arguments, calls it, and returns the result.
- **P3.4 [M]** Closure: `make_ewma(alpha)` returns a function that takes one new price and returns the updated EWMA. Keep state with `nonlocal`. Verify against a manual loop.
- **P3.5 [M]** Write 5 short snippets testing LEGB scope (global shadowing, `global`, `nonlocal`, loop variable leakage, a closure capturing a loop variable — the classic `lambda` in a list bug). Predict, then run.
- **P3.6 [M]** From `momentum(prices, lookback)` create `mom_20` and `mom_60` with `functools.partial`. Sort a list of strategy result dicts by Sharpe with `sorted(key=...)`, descending.
- **P3.7 [H]** Price an American put with a recursive Cox-Ross-Rubinstein binomial tree. Time it for 20 steps uncached, then add `@lru_cache` and run 200 steps. Explain the speedup in terms of overlapping subproblems.
- **P3.8 [P]** `compose(*funcs)` returns a function applying them left to right. Build a cleaning pipeline from small pure functions (`drop_nans`, `remove_outliers`, `to_returns`). Write tests showing that order matters and that each function leaves its input unmodified.

## Track B — NumPy: ufuncs, reductions, `axis`, `ddof`

Setup: `prices` = wide close matrix from the panel as `(T, 12)` array (drop KC or rows with NaN for today).

- **N3.1 [E]** Simple returns via slicing `p[1:] / p[:-1] - 1` and log returns via `np.log`. Verify `log(1 + simple) == log returns` with `np.allclose`.
- **N3.2 [E]** Mean, std, min, max per asset (`axis=0`) and per day across assets (`axis=1`). Write the resulting shape next to every line.
- **N3.3 [M]** Use `argmax`/`argmin`: the best and worst day per asset, and the best asset each day. Map indices back to dates and symbols.
- **N3.4 [M]** Compute std with NumPy default and with `ddof=1`; compare with pandas `.std()`. Explain the mismatch in one sentence.
- **N3.5 [M]** Z-score each asset's returns over time with `keepdims=True`. Then z-score cross-sectionally per day. Assert means ≈ 0 and stds ≈ 1 along the right axis.
- **N3.6 [H]** Winsorize returns at each asset's 1st/99th percentile using `np.percentile(axis=0)` + `np.clip` with broadcasting.
- **N3.7 [H]** Implement skewness and excess kurtosis per asset from scratch using reductions. Verify against `scipy.stats.skew` / `kurtosis`.
- **N3.8 [P]** `summary_stats(returns, periods=252) -> dict[str, np.ndarray]`: annualized return, vol, Sharpe, skew, kurtosis, hit rate, best/worst day — fully vectorized for any number of assets. Write a loop-based reference version and assert both agree.

## Track C — pandas: index alignment

- **D3.1 [E]** Take CL and KC close Series and add them. Count the NaNs created and explain exactly where they came from.
- **D3.2 [E]** Use `align(join="inner")` and `align(join="outer")`. Compare lengths.
- **D3.3 [M]** Reindex CL onto `pd.bdate_range` (weekdays). Count the new NaNs (holidays). Then reindex with `method="ffill"`, `limit=2`.
- **D3.4 [M]** Subtract each day's cross-sectional mean from a wide returns frame using `df.sub(row_mean, axis=0)`. Show what `df - row_mean` does instead and why it's wrong.
- **D3.5 [M]** Drop 5% random rows from CL and from BRN independently, then compute the CL/BRN ratio. Use `align` deliberately and report how many dates survive.
- **D3.6 [H]** Classic trap: compute returns as `s.iloc[1:] / s.iloc[:-1] - 1`. Why do you get (almost) all zeros? Fix it three ways (`.to_numpy()`, `.shift()`, `.pct_change()`) and explain.
- **D3.7 [P]** `align_frames(*objs, how="inner", calendar=None, ffill_limit=None)` aligns any number of Series/DataFrames to a common index, optionally onto a supplied calendar, forward-fills up to a limit, and logs how many values were filled per input. Tests for each option.

---

## Interview drill
1. What does `axis=0` mean for a `(T, N)` returns array — "per asset" or "per day"?
2. Why does `pd.Series([1,2], index=["a","b"]) + pd.Series([1,2], index=["b","c"])` produce NaNs?
3. Why use `ddof=1` for sample volatility?

## Done when
- [ ] N3.8 `summary_stats` saved — you'll reuse it all three weeks
- [ ] Committed: `day03: functions & closures, reductions, index alignment`
