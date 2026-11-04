# Day 10 — Decorators, Simulation, groupby

**Theme:** Add behavior to functions cleanly, simulate markets to test ideas statistically, and master split-apply-combine for cross-sectional research.
**Time budget:** ~7 h
**Save to:** `solutions/day10/`

---

## Track A — Python: decorators and context managers

- **P10.1 [E]** `@timer` that logs runtime. Use `functools.wraps` and show `__name__` / `__doc__` are preserved (and what breaks without it).
- **P10.2 [E]** `Timer` context manager class with `__enter__` / `__exit__`, storing elapsed time.
- **P10.3 [M]** Parametrized `@retry(times=3, backoff=0.5, exceptions=(ConnectionError,))`.
- **P10.4 [M]** `@validate_output` that raises if a returned array/DataFrame contains NaN or inf.
- **P10.5 [M]** `@contextmanager` helpers: a temporary working directory and a temporary `np.errstate` that turns divide-by-zero into an exception. Use `contextlib.suppress` in one place where it's genuinely appropriate.
- **P10.6 [H]** `@cache_to_parquet(dir)`: caches a function's DataFrame result to disk keyed by a hash of its arguments; skips recomputation on a hit; `force=True` overrides.
- **P10.7 [P]** Signal registry: `@register_signal("mom_20")` adds functions to a registry; a CLI `python -m signals run mom_20 --symbol CL` runs any registered signal. Also: stack `@timer` and `@validate_output` in both orders and explain the difference in behavior.

## Track B — NumPy: random numbers and simulation

- **N10.1 [E]** `rng = np.random.default_rng(42)`: draw normal, Student-t and uniform samples. Show reproducibility, and why the legacy `np.random.seed` global state is discouraged.
- **N10.2 [E]** GBM: 10,000 paths × 252 steps, fully vectorized. Check the mean terminal price against `S0·e^{μT}`.
- **N10.3 [M]** Ornstein–Uhlenbeck spread with the *exact* discretization. Recover κ, θ, σ by regressing `x_t` on `x_{t−1}` (AR(1)) with your Day 8 OLS. Compute the half-life of mean reversion.
- **N10.4 [M]** Monte Carlo price of a European call on a futures contract vs the **Black-76** closed form. Plot error vs number of paths (log-log) and add antithetic variates. How much variance reduction?
- **N10.5 [M]** Bootstrap a 95% confidence interval for the Sharpe ratio of a CL 60-day momentum strategy: iid bootstrap, then a block bootstrap (block length ~20). Compare widths and explain.
- **N10.6 [H]** Permutation test: shuffle the signal 5,000 times to build a null distribution of Sharpe ratios. Compute the p-value of the real strategy.
- **N10.7 [P]** Multi-asset simulator: Student-t shocks, Cholesky correlation, two-state Markov volatility regime. Simulate one year for a 12-asset portfolio and compute 1-day 99% VaR and Expected Shortfall. Compare with historical VaR/ES on the panel.

## Track C — pandas: `groupby`

Use the long panel with a `ret` column (log return per symbol — compute it with `groupby("symbol").close.transform(...)` or `groupby(...).shift`).

- **D10.1 [E]** Per symbol: mean volume, last close, row count.
- **D10.2 [E]** Named aggregations: `agg(avg_vol=("volume", "mean"), vol=("ret", "std"), n=("ret", "size"))`.
- **D10.3 [M]** Cross-sectional demeaning with `groupby("date").ret.transform("mean")`. Verify it matches your Day 3 wide-format answer exactly.
- **D10.4 [M]** 20-day momentum per symbol, then `rank(pct=True)` within each date and quintiles with `qcut` per date (handle dates with fewer than 5 symbols).
- **D10.5 [M]** Monthly returns per symbol with `pd.Grouper(freq="ME")`. Seasonality of NG by calendar month; day-of-week effects for all symbols.
- **D10.6 [H]** Per-symbol rolling 20-day vol four ways: `groupby.apply`, `groupby.rolling`, `groupby.transform(lambda...)`, and pivot→rolling→stack. Check equality and time each.
- **D10.7 [P]** **Factor quintile analysis.** Replace your Day 1 loop table with one `groupby`. Then: momentum quintiles each date → average *next-day* return per quintile → time series of Q5−Q1 → mean, t-stat (Newey–West from Day 8), and Q5 turnover. Write a 5-line conclusion.

---

## Interview drill
1. What is the difference between `groupby().transform` and `groupby().agg`?
2. Why is a block bootstrap preferred for time series?
3. Write Black-76 for a call from memory.

## Done when
- [ ] D10.7 results table committed
- [ ] Committed: `day10: decorators, Monte Carlo & bootstrap, groupby factor analysis`
- [ ] **Tomorrow is Capstone 2** — read `capstones/capstone2_risk_curve_lab.md`
