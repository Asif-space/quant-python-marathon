# Day 02 — Data Structures, Indexing, Selection

**Theme:** Choose the right container, select exactly the data you mean, and know when you're holding a view or a copy.
**Time budget:** ~6–7 h
**Save to:** `solutions/day02/`

---

## Track A — Python: data structures, complexity, `collections`

- **P2.1 [E]** Generate 100,000 symbols drawn randomly from the 12 panel symbols. Count occurrences with a plain `dict`, then with `Counter`. Print the top 3 with `most_common`.
- **P2.2 [E]** Build sets of trading dates for CL and KC from the panel. Find common dates, CL-only dates and the symmetric difference. Explain the result.
- **P2.3 [M]** Benchmark 10,000 membership checks against 1,000,000 integers stored in a `list`, a `set` and a `dict`. Tabulate the timings and connect them to Big-O.
- **P2.4 [M]** Use `defaultdict(list)` to group trade tuples `(symbol, qty, price)` by symbol, then compute VWAP per symbol.
- **P2.5 [M]** Streaming rolling mean: with `deque(maxlen=20)` and a running sum, update the 20-tick mean in O(1) per tick. Verify against brute-force `sum(window)/len(window)` on 10,000 prices.
- **P2.6 [H]** Store 1,000,000 trade records as `dict`, `namedtuple` and a plain class. Compare memory (`tracemalloc`) and attribute-access speed.
- **P2.7 [H]** Implement `LRUCache(capacity)` with `OrderedDict` (`get`/`put` in O(1)) to cache loaded price series by symbol. Test eviction order.
- **P2.8 [P]** **FIFO position ledger.** Process a stream of fills `(symbol, side, qty, price)`. Keep a `deque` of open lots per symbol; match closing fills FIFO; track realized PnL and current position. Handle a single fill that flips long → short. Write 6 edge-case tests (partial close, exact close, flip, multiple lots, short first, zero-qty rejection).

## Track B — NumPy: indexing, slicing, views vs copies

- **N2.1 [E]** From a 252-day price array: first 10, last 10, every 5th, reversed, last 20 days.
- **N2.2 [E]** For a `(1000, 12)` returns matrix: column 3; rows 100–199 for columns 0–4; the last row; the diagonal of the first 12 rows.
- **N2.3 [E]** Boolean masks: extract negative returns; count days with |r| > 2σ; set returns beyond 5σ to `NaN` (copy first!).
- **N2.4 [M]** With `np.where`, map a z-score array to signals (+1 if z > 1, −1 if z < −1, else 0). Then find the indices where the signal changes.
- **N2.5 [M]** Given a `(T, 12)` momentum array, use `argsort` + `np.take_along_axis` to extract the returns of the top-3 assets each day.
- **N2.6 [H]** Run 6 experiments — basic slice, boolean mask, fancy index, `reshape`, `ravel` vs `flatten`, `.T`. Predict view or copy for each, then verify with `np.shares_memory` and `.base`. Record results in a table.
- **N2.7 [H]** Bug hunt: write a function that "normalizes" a price window by dividing a slice in place, and show how it silently corrupts the caller's data. Fix it two different ways.
- **N2.8 [P]** **Holding mask from signals, no loops.** Given boolean `entry` and `exit` arrays, compute a boolean `in_position` array (you are in from an entry until the next exit). Hint: build arrays of "index of last entry" and "index of last exit" with `np.where` + `np.maximum.accumulate`, then compare. Validate against a simple loop on 1,000 random cases.

## Track C — pandas: selection with `loc`, `iloc`, masks, setting values

Setup: `wide = panel.pivot(index="date", columns="symbol", values="close")`

- **D2.1 [E]** With `loc`, select CL and NG for 2020. With `iloc`, select the first 10 rows and columns 2–5.
- **D2.2 [E]** Find the days when CL closed below its own 1st percentile. How many, and in which years?
- **D2.3 [E]** On the long panel, use `query` to find rows where `symbol == "CL" and volume > 300000`.
- **D2.4 [M]** Use `isin` and `between` to select all metals rows from 2020-03-01 to 2020-06-30.
- **D2.5 [M]** Create a column `bad_bar` that is `True` where `high < max(open, close)` or `low > min(open, close)`, using `.loc[mask, col] = ...`. Then demonstrate chained assignment (`df[mask]["col"] = ...`), show that it doesn't modify `df` under Copy-on-Write, and explain why.
- **D2.6 [M]** Make a Series with integer index `[10, 20, 30, 40]`. Compare `s[1]`, `s.loc[10]`, `s.iloc[1]`, and slicing `s.loc[10:30]` vs `s.iloc[0:2]` (inclusive vs exclusive). Write notes.
- **D2.7 [H]** Time 100,000 scalar reads with `.at`, `.iat`, `.loc`, `.iloc`. Then rewrite the loop as one vectorized operation and time that. Conclusion?
- **D2.8 [P]** `select_window(df, symbols, start, end, cols)` — validates inputs, warns (not fails) for unknown symbols, always returns a copy. `pytest`: modifying the output must never change the input.

---

## Interview drill
1. What is the time complexity of `x in my_list` vs `x in my_set`? Why?
2. Does `arr[arr > 0]` return a view or a copy? What about `arr[2:5]`?
3. `loc` vs `iloc`: which is inclusive at the end of a slice?

## Done when
- [ ] P2.8 ledger passes all 6 tests (you'll reuse it on Day 8)
- [ ] N2.6 table committed
- [ ] Committed: `day02: collections, indexing, views vs copies, loc/iloc`
