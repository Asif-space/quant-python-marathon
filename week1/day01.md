# Day 01 — Objects, Arrays, Frames

**Theme:** Get comfortable with the three core objects you will touch every day: Python objects, the NumPy `ndarray`, and the pandas `DataFrame`.
**Time budget:** ~6–7 h · Python 2 h · NumPy 2 h · pandas 2 h · commit 15 min
**Save to:** `solutions/day01/`

Difficulty: **[E]** easy · **[M]** medium · **[H]** hard · **[P]** professional

---

## Track A — Python: types, mutability, strings, control flow

- **P1.1 [E]** Write `parse_contract(code: str) -> dict` that turns `"CLZ26"` into `{"root": "CL", "month": 12, "year": 2026}`. Support 2- and 3-letter roots (`"BRNF27"`). Raise `ValueError` with a clear message for an invalid month code or a malformed string.
- **P1.2 [E]** *Predict, then run.* Write 8 snippets about aliasing: `a = b = []`, list slice copy `b = a[:]`, `copy.copy` vs `copy.deepcopy` on a nested list of positions `[["CL", 5], ["NG", -2]]`, a function that appends to a list argument, `+=` vs `= a + [...]` on an aliased list. Write your prediction in a comment before running each. Note every one you got wrong.
- **P1.3 [E]** Print a trade blotter from a list of tuples `(symbol, side, qty, price, pnl)` as an aligned table using f-strings: price to 2 decimals, PnL with sign and thousands separator (`+12,345.50`), return as a percentage (`-1.25%`).
- **P1.4 [M]** `classify_returns(returns: list[float]) -> dict`: count up/down/flat days, longest winning streak and longest losing streak, using only loops and `if` statements (no libraries).
- **P1.5 [M]** Given ticks as a list of `(time_str, price)`, return the first time the price crosses a barrier. Use `for ... else` so the "barrier never hit" case lives in the `else` clause.
- **P1.6 [H]** `format_price(price: float, tick_size: float) -> str`: round to the nearest tick and print with exactly the precision the tick implies (0.01 → 2 dp, 0.25 → 2 dp, 0.005 → 3 dp). Bonus: support US Treasury 1/32 ticks printed as `"112-16"`. Write 10 test cases with `assert`.
- **P1.7 [P]** Build a small order-entry parser with `match`/`case` that accepts `"BUY 5 CLZ26 @ 71.25"`, `"SELL 3 NGF27 MKT"`, `"CANCEL 1042"` and returns structured dicts. Reject malformed input with specific error messages (unknown side, non-integer quantity, bad contract code — reuse P1.1).

## Track B — NumPy: the ndarray, dtypes, creation

- **N1.1 [E]** Create a 252-element price array five ways: `zeros`, `ones * 100`, `full`, `arange`, `linspace`. For each print `shape`, `ndim`, `size`, `dtype`, `itemsize`, `nbytes`.
- **N1.2 [E]** Make a Python list of 1,000,000 random floats and the equivalent array. Time `sum(list)` vs `np.sum(arr)` with `timeit`. Report the speed ratio in one sentence.
- **N1.3 [E]** Store the same prices as `float64`, `float32`, and `int32` (prices in cents). Compare `nbytes` and compute the mean in each. When is integer-cents storage the right choice?
- **N1.4 [M]** Using `datetime64[D]`, `np.busday_offset`, `np.is_busday` and a holiday list you type in (New Year, MLK, Presidents', Good Friday, Memorial, Juneteenth, Independence, Labor, Thanksgiving, Christmas), build all 2025 trading days and count trading days per month.
- **N1.5 [M]** Generate 2,520 daily returns. `reshape` to `(10, 252)` and compute per-year mean; `reshape(-1, 5)` for weekly blocks. What happens when the length isn't divisible? Write a helper that trims safely.
- **N1.6 [H]** Create a 5000×5000 `float64` matrix in C order and F order. Time `.sum(axis=0)` and `.sum(axis=1)` for each. Inspect `.strides` and `.flags`. Explain the timings in a short markdown note (`notes/day01_memory_layout.md`).
- **N1.7 [P]** Simulate a 100,000-step random walk four ways: Python list append, `np.append` in a loop, preallocated `np.empty` filled in a loop, and fully vectorized `cumsum`. Time all four and write a conclusion: why is `np.append` in a loop a trap?

## Track C — pandas: Series, DataFrame, Index, inspection, I/O

Data: `data/raw/panel_daily.parquet`, `data/raw/panel_daily_dirty.csv`

- **D1.1 [E]** Load the clean panel. Report shape, dtypes, `memory_usage(deep=True)`, number of symbols, and overall date range.
- **D1.2 [E]** Build a `Series` of CL closes indexed by date. Show `head`, `tail`, `min`, `max`, `idxmin`, `idxmax`.
- **D1.3 [E]** Construct DataFrames three ways: dict of lists, list of dicts (trade records), and a 2-D NumPy array with explicit `index` and `columns`.
- **D1.4 [M]** Build a summary table with one row per symbol: first date, last date, observations, min/max close, mean volume. Today, a loop over symbols is fine — you'll replace it with a single `groupby` on Day 10.
- **D1.5 [M]** Use `value_counts` to count rows per symbol. Which symbol has the fewest rows, and why? Prove it from the data.
- **D1.6 [H]** Load `panel_daily_dirty.csv` naively with `read_csv`. Don't fix anything yet. Investigate and write a data-quality report (`notes/day01_dirty_data.md`) listing every problem you find, with counts and an example row for each. (You fix them on Day 4 — the more you find now, the better.)
- **D1.7 [P]** Write `load_panel(path) -> pd.DataFrame` that reads `.parquet` or `.csv`, enforces a schema (column names and dtypes), and raises a clear error if required columns are missing. Add 3 `pytest` tests (good file, missing column, wrong extension).

---

## Interview drill (10 min)
1. Why does `def f(x, acc=[])` behave strangely across calls?
2. What is the difference between `a += [1]` and `a = a + [1]` when `a` is aliased?
3. Why is a NumPy array faster than a list for numeric work? Give two reasons.

## Done when
- [ ] All [E] and [M] exercises solved and run without errors
- [ ] At least one [H] per track
- [ ] Notes written for N1.6 and D1.6
- [ ] Committed: `day01: python basics, ndarray creation, pandas I/O`
