# Day 13 — Algorithms, Memory, Reshaping & MultiIndex

**Theme:** The algorithms interviewers ask and order books rely on, NumPy at the memory level, and panel data reshaping — ending with a leak-free feature engine.
**Time budget:** ~7–8 h
**Save to:** `solutions/day13/`

---

## Track A — Python: `heapq`, `bisect`, algorithms

- **P13.1 [E]** `heapq.nlargest`: the 3 most volatile assets from a stream of `(symbol, vol)` pairs; then maintain a top-3 min-heap incrementally.
- **P13.2 [E]** `bisect.insort` into a sorted price ladder; `bisect_left` to find a price level's index.
- **P13.3 [M]** `heapq.merge` three time-sorted streams (quotes, trades, scheduled events) into one. Break timestamp ties with a priority field, and explain why tie-breaking matters in a backtester.
- **P13.4 [M]** Sliding-window maximum in O(n) with a monotonic `deque`. Verify against brute force.
- **P13.5 [M]** Classic: maximum profit with (a) one transaction, (b) unlimited transactions, (c) at most *k* transactions (dynamic programming).
- **P13.6 [H]** Running median of a stream with two heaps. Use it for a robust "bad tick" filter (reject price if it's more than X% from the running median).
- **P13.7 [H]** Interval problems on timestamps: merge overlapping sessions; find data outages (gaps longer than 2 seconds) in the quote stream.
- **P13.8 [P]** **Limit order book.** Price-time priority book with a `dict` of price → `deque` of orders, heaps for best bid/ask with lazy deletion, and O(1) cancel via an id lookup. Replay `lob_events.parquet` (A = add, C = cancel, E = execute) and match `lob_final_snapshot.csv` exactly.

## Track B — NumPy: memory, in-place ops, overflow, structured arrays

- **N13.1 [E]** In-place vs out-of-place: `a = a * 2`, `a *= 2`, `np.multiply(a, 2, out=a)`. Measure peak memory with `tracemalloc` on a 200 MB array.
- **N13.2 [E]** Overflow: sum `int32` volumes until it wraps; multiply `int64` nanosecond timestamps by 1000; compare `datetime64[ns]` and `datetime64[ms]` ranges.
- **N13.3 [M]** Structured array for trades: `[("ts", "i8"), ("price", "f8"), ("size", "i4"), ("side", "S1")]`. Sort by `ts`, access fields, convert to a DataFrame.
- **N13.4 [M]** Write 50 million `float32` returns with `np.memmap`. Compute mean and std in chunks without ever loading the full array.
- **N13.5 [H]** Cumulative sum of 10 million small returns in `float32` vs `float64` vs Kahan (compensated) summation in Numba. Report the errors.
- **N13.6 [P]** Design a fixed-width binary tick format. Write `ticks_trades` with `tofile`, read it back with `np.fromfile` and `memmap`, and benchmark file size and read time against Parquet and CSV.

## Track C — pandas: reshaping and MultiIndex

- **D13.1 [E]** `pivot` long → wide closes and `melt` wide → long. Assert the round trip is identical (after sorting).
- **D13.2 [E]** `pivot_table`: mean volume by symbol × year.
- **D13.3 [M]** `set_index(["date", "symbol"])`; `xs` for one date and for one symbol; `pd.IndexSlice` for a date range and two symbols; show what happens without `sort_index()`.
- **D13.4 [M]** `stack` / `unstack` between long and wide returns; `groupby(level="date")` for cross-sectional stats.
- **D13.5 [M]** Futures curve: pivot `futures_cl` to date × contract rank (1–12) settles. Plot curve snapshots on four dates and label each contango or backwardation.
- **D13.6 [H]** Calendar spreads M1−M2 and M1−M12 (as % of M1). Fraction of days in contango by year. Does the spread predict the next 20-day front-month return? (Bucket analysis.)
- **D13.7 [P]** **Leak-free feature engine.** Function returning a `(date, symbol)` MultiIndex frame of features: returns 1/5/20d, 20d vol, 60d momentum, 20d z-score, volume ratio. Only `groupby`, `rolling`, `shift`. Then write the *look-ahead test*: truncate the data at date *t*, recompute, and assert features at *t* are unchanged — for 20 random dates.

---

## Interview drill
1. Time complexity of push/pop on a binary heap? Of a cancel with lazy deletion?
2. Why can summing many `float32` numbers give a visibly wrong answer?
3. Long vs wide format: when do you want each?

## Done when
- [ ] Order book replay matches the snapshot
- [ ] Look-ahead test passes for the feature engine
- [ ] Committed: `day13: order book, binary formats, MultiIndex feature engine`
