# Day 07 — Robust Code, Searching, Shift & Resample

**Theme:** Make code fail loudly and usefully, search sorted data fast, and learn the single most important rule of backtesting: never use information you didn't have yet.
**Time budget:** ~7 h
**Save to:** `solutions/day07/`

---

## Track A — Python: errors, logging, files, modules, CLI

- **P7.1 [E]** `try / except / else / finally` around reading a file that may not exist. Catch only specific exceptions; explain why bare `except:` is dangerous.
- **P7.2 [E]** Exception hierarchy: `DataError` → `MissingDataError`, `StaleDataError`, `BadTickError`. Raise each from a small validator and catch them by base class.
- **P7.3 [M]** Retry with exponential backoff (`1s, 2s, 4s…`, max 5 tries) around a function that fails randomly 60% of the time. Log each attempt.
- **P7.4 [M]** Configure `logging` with console (INFO) and file (DEBUG) handlers and a format with timestamp and module name. Replace every `print` in Capstone 1 with proper log calls.
- **P7.5 [M]** With `pathlib`: list every file under `data/` with size in MB, build output paths safely, and save/load a JSON config.
- **P7.6 [H]** `argparse` CLI with subcommands: `clean` (input, output) and `report` (input, output dir, `--symbols`). Wire it to Capstone 1.
- **P7.7 [P]** Declarative validation layer: `validate(df, rules) -> None` where rules are small objects like `NoNaN("close")`, `MonotonicIndex()`, `Positive("close")`, `HighLowConsistent()`. Collect *all* failures and raise one error listing them. Tests for each rule plus a combined failure.

## Track B — NumPy: sorting, searching, unique, binning

- **N7.1 [E]** Rank assets each day by return with `argsort(argsort(...))`. Check against `scipy.stats.rankdata` for one row.
- **N7.2 [E]** Top 3 returns per row with `np.partition` (no full sort). Compare speed with `np.sort` on a `(10000, 500)` array.
- **N7.3 [M]** `np.unique(..., return_inverse=True, return_counts=True)` to map symbol strings to integer codes and back.
- **N7.4 [M]** **As-of join in NumPy.** Convert quote and trade timestamps to `int64` nanoseconds. Use `np.searchsorted(quote_ts, trade_ts, side="right") - 1` to attach the prevailing quote to each trade. Handle trades before the first quote (index −1).
- **N7.5 [M]** Bucket daily returns into deciles with `np.quantile` + `np.digitize`; compute the average *next-day* return per decile. Any pattern?
- **N7.6 [H]** `np.lexsort` trades by `(day, ts, size)`. Verify stability and order. Explain why `lexsort` takes keys in reverse order.
- **N7.7 [P]** **Front-month mapping, vectorized.** From `futures_cl.parquet`, take sorted unique expiries and the trading dates. Using `searchsorted`, assign each date the contract you'd hold if you roll *N business days before expiry*. Validate against a slow loop.

## Track C — pandas: `shift`, look-ahead bias, `resample`

- **D7.1 [E]** For CL show `shift(1)`, `shift(-1)`, `diff()`, `pct_change()` side by side in one frame for 10 rows. Label which columns are "known at the close of day t".
- **D7.2 [E]** Resample daily CL to weekly (`"W-FRI"`, last) and month-end (`"ME"`, last). Compute weekly and monthly returns.
- **D7.3 [M]** From `ticks_trades.parquet` (cleaned: deduplicated, sorted), build 1-minute OHLCV bars with `resample("1min")` — `.ohlc()` on price, `sum` on size. Compare to your pure-Python bars from P4.6.
- **D7.4 [M]** Build 5-minute bars with every combination of `label` and `closed` (left/right). For a trade at exactly `10:05:00`, show which bar it lands in. State which configuration lets a signal "at bar close" be computed without peeking.
- **D7.5 [H]** **Look-ahead lab.** Strategy: long when today's return > 0. Version A (bug): earn *today's* return. Version B (correct): signal shifted one day. Report both Sharpes. Then find one subtler leak of your own (e.g. normalizing with a full-sample mean) and quantify it too.
- **D7.6 [H]** EIA releases come out Wednesday 10:30 ET. Merge `eia_weekly.csv` onto the daily panel so each day sees the *latest released* surprise. Is the Wednesday surprise usable for a signal at Wednesday's close? At Wednesday's open? Encode the answer in code.
- **D7.7 [P]** `make_bars(trades, kind, threshold)` supporting time bars, tick bars (every N trades), and volume bars (every V contracts) using `cumsum` and integer division as group keys (light `groupby` preview). Compare the kurtosis of returns for each bar type and explain the result.

---

## Week 1 review (30–45 min)
Without looking anything up, write answers to these in `notes/week1_review.md`, then check:
1. Three ways to copy a list and when each is a shallow copy.
2. How broadcasting decides compatible shapes.
3. Why `s.iloc[1:] / s.iloc[:-1]` fails in pandas.
4. The difference between `resample(...).last()` and `asfreq()`.
5. Two different ways look-ahead bias enters a backtest.

## Done when
- [ ] D7.5 results written up (this is a great README section)
- [ ] Committed: `day07: validation & CLI, searchsorted as-of join, look-ahead lab`
