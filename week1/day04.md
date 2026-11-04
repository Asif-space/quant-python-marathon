# Day 04 — Lazy Iteration, Broadcasting, Cleaning Real Data

**Theme:** Stream data without loading it all, make shapes work for you, and turn the dirty panel into clean, trustworthy data.
**Time budget:** ~7 h (pandas runs long today — it's the most realistic work of the week)
**Save to:** `solutions/day04/`

---

## Track A — Python: comprehensions, iterators, generators, `itertools`

- **P4.1 [E]** Comprehensions: dict `symbol -> last close`, set of sectors, list of positive returns, nested comprehension flattening `[[...], [...]]`.
- **P4.2 [E]** Compare peak memory (`tracemalloc`) of `sum([x*x for x in range(10_000_000)])` vs `sum(x*x for x in range(10_000_000))`.
- **P4.3 [M]** Write an iterator class `ContractRoller(root, start, end)` implementing `__iter__`/`__next__` that yields monthly contract codes (`CLF25`, `CLG25`, ...). Then rewrite it as a generator function and compare length of code.
- **P4.4 [M]** Generator `iter_trades(path, batch_size=10_000)` using `pyarrow.parquet.ParquetFile(...).iter_batches()` over `ticks_trades.parquet`, yielding one trade at a time. Compute total volume and VWAP without ever holding the full table.
- **P4.5 [M]** `itertools`: `product` to build a parameter grid (lookback × threshold × holding period); `combinations` of the 12 symbols for pair candidates (confirm 66); `pairwise` for consecutive price changes; `accumulate(max)` for a running peak.
- **P4.6 [H]** With `itertools.groupby`, turn time-sorted trades into 1-minute OHLCV bars in pure Python. Save the result — you'll check it against pandas on Day 7.
- **P4.7 [H]** Build a lazy pipeline of generators: read → drop duplicate trades → compute tick returns → rolling z-score. Show peak memory stays flat as you process more data.
- **P4.8 [P]** A coroutine-style generator implementing **Welford's online algorithm**: `.send(x)` returns the running mean and variance. Validate against `np.var` on 1,000,000 values centered at 1e9 (shows why the naive `E[x²] − E[x]²` formula fails numerically).

## Track B — NumPy: broadcasting

- **N4.1 [E]** Subtract a `(12,)` vector of per-asset transaction costs from a `(1000, 12)` returns array. Write the broadcast shapes on paper first.
- **N4.2 [E]** Demean by column (`X - X.mean(axis=0)`) and by row (`X - X.mean(axis=1)[:, None]`). Assert results.
- **N4.3 [M]** Payoff matrix: spots `(500,)` and strikes `(20,)` → call payoffs `max(S − K, 0)` with shape `(500, 20)`, no loops.
- **N4.4 [M]** Pairwise Euclidean distance between the 12 assets' return series via `(12, 1, T) − (1, 12, T)`. Then compute the correlation matrix manually by broadcasting and compare with `np.corrcoef`.
- **N4.5 [H]** Risk-parity-style weights: given a `(T, 12)` volatility array, compute `w = (1/vol)` normalized so each row's absolute weights sum to 1. Assert row sums.
- **N4.6 [H]** Write 5 examples where broadcasting silently produces the *wrong* shape (e.g. `(n,)` vs `(n, 1)` turning into `(n, n)`). For each, add an `assert` that would have caught it.
- **N4.7 [P]** **Grid backtest in one array.** For lookbacks `L ∈ {5, 10, …, 250}` (50 values) and 12 assets, compute signal `sign(p_t − p_{t−L})` and next-day PnL in a single `(L, T, A)` array, then Sharpe per `(L, A)`. Measure memory. Then rewrite with a loop over `L` only and compare speed/memory. When is "fully vectorized" not worth it?

## Track C — pandas: missing data, cleaning, dtypes

Data: `data/raw/panel_daily_dirty.csv` (use your Day 1 report)

- **D4.1 [E]** `isna().sum()` per column and percentage missing `close` per symbol.
- **D4.2 [E]** Clean `symbol`: strip whitespace, upper-case. Assert exactly 12 unique symbols.
- **D4.3 [M]** Parse the mixed date formats. Try `pd.to_datetime(..., format="mixed")` and a two-pass approach with explicit formats. Assert no `NaT` and that both approaches agree.
- **D4.4 [M]** Convert `volume` strings like `"1,234"` to integers with `pd.to_numeric(errors="coerce")` after cleaning. Turn negative volumes into `NaN`.
- **D4.5 [M]** Find exact duplicate rows and duplicate `(date, symbol)` keys whose values differ. Decide and document a de-duplication rule.
- **D4.6 [H]** Detect decimal-shift bad ticks (close × 10 or ÷ 10) using the ratio to the previous valid close of the *same symbol* (pivot to wide, or sort and mask where the symbol changes). Report how many you found vs the 40 that were injected.
- **D4.7 [H]** Compare fill policies on a small example: `ffill(limit=3)`, `bfill`, `interpolate`, `dropna`. Build a 10-row example showing exactly how `bfill` and `interpolate` leak future information into a backtest.
- **D4.8 [P]** `clean_panel(raw) -> tuple[pd.DataFrame, dict]` — the full pipeline returning a clean frame plus a report of every fix (counts per category). Test it against `panel_daily.parquet`: matching row count where possible, max absolute close difference on shared rows, and a list of rows you couldn't recover (and why that's fine).

---

## Interview drill
1. What's the difference between an iterator and an iterable?
2. Shapes `(5, 1)` and `(3,)` — do they broadcast? To what?
3. Why is forward fill usually acceptable in a backtest while backward fill is not?

## Done when
- [ ] `clean_panel` reproduces the clean panel closely, with a written report
- [ ] Committed: `day04: generators, broadcasting, data cleaning pipeline`
