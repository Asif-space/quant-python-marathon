# Day 14 — Performance Engineering

**Theme:** Measure first, then make it fast. Professional research code is judged by correctness *and* by whether it finishes overnight.
**Time budget:** ~7 h
**Save to:** `solutions/day14/`

---

## Track A — Python: profiling, the GIL, optimization

- **P14.1 [E]** Profile your Capstone 1 report with `cProfile` and sort with `pstats` by cumulative time. List the top 5 hotspots.
- **P14.2 [E]** `timeit` micro-benchmarks: string `+=` vs `"".join`; list comprehension vs `map` vs `for` loop; attribute lookup in a loop vs a local alias.
- **P14.3 [M]** `line_profiler` on your slowest function; optimize it and show the before/after line timings.
- **P14.4 [M]** Find a memory leak with `tracemalloc` snapshot diffs: write an unbounded cache on purpose, detect it, fix it with your LRU cache from P2.7.
- **P14.5 [H]** GIL demo: a CPU-bound task with 4 threads vs 4 processes; an I/O-bound task (simulated with `time.sleep`) with threads. Explain the results.
- **P14.6 [P]** **Speed-up challenge.** Write a deliberately naive backtest (`iterrows`, `DataFrame.append`-style concatenation in a loop, repeated lookups). Then make it ≥100× faster in steps, recording each step's runtime in a table in your README. Results must be identical at every step.

## Track B — NumPy + Numba

- **N14.1 [E]** `@njit` a loop sum. Measure first-call (compile) time vs subsequent calls. Try `cache=True`.
- **N14.2 [M]** EWMA recursion in Numba vs `pandas.ewm(adjust=False)`. Assert equality, compare speed.
- **N14.3 [M]** Break Numba deliberately: pass a list of mixed types, a DataFrame, a dict. Read the errors and write down the rules of nopython mode.
- **N14.4 [H]** Monte Carlo pricing with `@njit(parallel=True)` and `prange` vs vectorized NumPy. Benchmark across 1e5, 1e6, 1e7 paths; note where each wins.
- **N14.5 [P]** **Numba backtest core.** Inputs: prices `(T, A)`, target positions `(T, A)`, cost per unit traded, position limits, per-asset stop-loss. Output: positions, PnL, costs, trades. Compare against an equivalent pandas implementation for equality and speed.

## Track C — pandas performance and storage

- **D14.1 [E]** `category` dtype for `symbol`: memory before/after; `groupby` speed before/after (`observed=True`).
- **D14.2 [E]** Write the panel as CSV and Parquet. Compare file sizes and read times; read only selected `columns`; use Parquet `filters` to read one symbol.
- **D14.3 [M]** On 1M rows, compute the same value with `iterrows`, `itertuples`, `apply(axis=1)` and a vectorized expression. Table of timings.
- **D14.4 [M]** Heavy math via `.to_numpy()`; `df.eval` / `df.query` on a 5M-row frame vs standard syntax.
- **D14.5 [H]** Export quotes to CSV and compute daily mid VWAP-style averages with `read_csv(chunksize=...)` without loading the whole file. Verify against the in-memory answer.
- **D14.6 [H]** `dtype_backend="pyarrow"`: memory and speed for string-heavy and numeric operations vs NumPy-backed dtypes.
- **D14.7 [P]** **Polars port.** Re-implement the Day 13 feature engine with the Polars lazy API (`scan_parquet`, `over`, `rolling`, `shift`). Assert results equal pandas within tolerance and compare runtime.

---

## Week 2 review (45 min) — `notes/week2_review.md`
1. Explain Newey–West in plain words.
2. Why do PCA loadings on a futures curve look like level/slope/curvature?
3. When would you choose Numba over vectorized NumPy?
4. Draw the data flow of `merge_asof` for trades and quotes.
5. What makes a feature engine leak-free, and how do you *test* that?

## Done when
- [ ] Speed-up table in README
- [ ] Committed: `day14: profiling, numba backtest core, polars port`
