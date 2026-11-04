# Quant Python Marathon — 21 Days of Python, NumPy & pandas for Quantitative Research

A 21-day, exercise-driven program to go from "I've learned it" to "I can use it under pressure" in the three libraries every quant researcher lives in. All three tracks run **in parallel every day**, difficulty climbs from easy to professional, and five capstone projects tie the skills together around commodity futures and market microstructure.

![tests](https://img.shields.io/badge/tests-add%20your%20CI%20badge%20on%20Day%2012-lightgrey)

---

## How it works

Each day has three tracks plus an interview drill:

| Track | Focus |
|---|---|
| **A — Python** | Language depth, data structures, OOP, testing, performance, concurrency |
| **B — NumPy** | Arrays, broadcasting, linear algebra, simulation, vectorization, Numba |
| **C — pandas** | Cleaning, time series, rolling/groupby, merges, reshaping, futures & tick data |

**Difficulty levels**

| Tag | Level | What it means |
|---|---|---|
| **[E]** | Easy | Direct use of one feature. 5–10 min. |
| **[M]** | Medium | Combine features; small realistic task. 15–25 min. |
| **[H]** | Hard | Non-obvious solution, performance or correctness subtlety. 30–45 min. |
| **[P]** | Professional | What you'd be asked to build on the job: tested, reusable, documented. 45–90 min. |

**Daily minimum:** all [E] and [M], plus at least one [H] per track. [P] exercises are where the portfolio value is — do them when time allows, and come back for the ones you skip.

---

## Schedule

| Day | Python | NumPy | pandas |
|---|---|---|---|
| [01](week1/day01.md) | Types, mutability, strings, control flow | ndarray, dtypes, creation, memory layout | Series/DataFrame, inspection, I/O |
| [02](week1/day02.md) | Data structures, Big-O, `collections` | Indexing, masks, views vs copies | `loc`/`iloc`, filtering, setting values |
| [03](week1/day03.md) | Functions, scope, closures, `functools` | ufuncs, reductions, `axis`, `ddof` | Index alignment, `reindex` |
| [04](week1/day04.md) | Comprehensions, generators, `itertools` | Broadcasting | Missing data, cleaning, dtypes |
| [05](week1/day05.md) | `datetime`, time zones, floats, `Decimal` | Returns, cumulative ops, drawdowns | DatetimeIndex, tz, calendars, returns |
| **[06](week1/day06.md)** | **Capstone 1 — Data Quality & Returns Toolkit** | | |
| [07](week1/day07.md) | Errors, logging, `pathlib`, CLI | Sorting, `searchsorted`, binning | `shift`, look-ahead bias, `resample` |
| [08](week2/day08.md) | OOP: classes, dunders, properties | Linear algebra I: OLS, Newey–West | `rolling`, `expanding` |
| [09](week2/day09.md) | Dataclasses, enums, ABCs, composition | Linear algebra II: PCA, Cholesky, shrinkage | `ewm`, rolling cov/corr |
| [10](week2/day10.md) | Decorators, context managers | Random numbers, Monte Carlo, bootstrap | `groupby`, cross-sectional ranks |
| **[11](week2/day11.md)** | **Capstone 2 — Risk & Futures Curve Lab** | | |
| [12](week2/day12.md) | Type hints, `pytest`, `hypothesis`, CI | `sliding_window_view`, `einsum`, Numba intro | `merge`, `concat`, `merge_asof` |
| [13](week2/day13.md) | `heapq`, `bisect`, algorithms, order book | Memory, overflow, structured arrays | Reshaping, MultiIndex, feature engine |
| [14](week2/day14.md) | Profiling, GIL, optimization | Numba in depth | pandas performance, Parquet, Polars |
| [15](week3/day15.md) | Multiprocessing, walk-forward | Black-76, variance reduction, deflated Sharpe | Continuous futures construction |
| **[16](week3/day16.md)** | **Capstone 3 — Futures Signal Research & Backtester** | | |
| [17](week3/day17.md) | Event-driven architecture | Microprice, OFI, order book arrays | Tick data, bars, price impact |
| [18](week3/day18.md) | `asyncio` | Kyle's λ, Roll spread, execution cost | Intraday seasonality, event studies |
| **[19](week3/day19.md)** | **Capstone 4 (1/2) — Microstructure engine** | | |
| **[20](week3/day20.md)** | **Capstone 4 (2/2) — Market making study** | | |
| **[21](week3/day21.md)** | **Capstone 5 — Ship It + timed mock interview** | | |

Capstone specs live in [`capstones/`](capstones/).

---

## Setup

```bash
git clone <your-repo-url> quant-python-marathon
cd quant-python-marathon
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python data/generate_data.py                            # creates data/raw/ (~10 MB, ~1 second)
```

## The datasets

All data is **synthetic and reproducible** (seed 42), so you can publish everything on GitHub without licensing issues. It is built to behave like real commodity data, including the traps.

| File | Rows | What it is | Built-in quirks to discover |
|---|---|---|---|
| `panel_daily.parquet` | ~33k | Daily OHLCV for 12 commodities (CL, BRN, NG, HO, RB, GC, SI, HG, ZC, ZS, ZW, KC), 2015–2025, long format | Fat tails, volatility regimes, sector correlations, slow trends, NG winter volatility, KC starts in mid-2016 |
| `panel_daily_dirty.csv` | ~33k | Same panel with errors injected | Duplicates, gaps, missing closes, decimal-shift bad ticks, `"1,234"` volumes, negative volumes, messy symbols, two date formats, shuffled rows |
| `futures_cl.parquet` | ~50k | Daily settles, volume and open interest for individual CL-style contracts | Real CL expiry rule with US holidays, contango/backwardation regimes, volume rolls from M1 to M2 before expiry |
| `eia_weekly.csv` | 574 | Weekly crude inventory releases: consensus, actual, surprise | Holiday weeks move to Thursday; energy prices genuinely react to surprises |
| `ticks_quotes.parquet` | 400k | Top-of-book quotes, 5 sessions, UTC nanoseconds | U-shaped intraday activity; session hours are Chicago time |
| `ticks_trades.parquet` | ~75k | Trades with true aggressor side | Duplicates, 20 out-of-order rows; trade signs carry short-term information |
| `lob_events.parquet` | ~73k | Level-3 order events: add / cancel / execute | Partial executions, price-time priority |
| `lob_final_snapshot.csv` | 10 | Book after the last event | Your replay must match it exactly |

---

## Repo structure

```
quant-python-marathon/
├── README.md
├── requirements.txt
├── data/
│   ├── generate_data.py
│   └── raw/                  # generated, git-ignored
├── week1/ week2/ week3/      # daily exercise sheets
├── capstones/                # capstone specs (+ your capstone code folders)
├── solutions/
│   └── dayXX/
│       ├── python_track.py   # or one file per exercise: p01_parse_contract.py ...
│       ├── numpy_track.py
│       ├── pandas_track.py
│       ├── tests/
│       └── README.md         # what you solved, what was hard
└── notes/                    # write-ups and reviews
```

## Daily workflow

1. Read the day's sheet top to bottom (10 min).
2. Rotate tracks in ~90-minute blocks: A → B → C. Switching keeps all three fresh and mirrors real work.
3. For each exercise: **predict → write → run → test**. Write the docstring and one test before the code for [H] and [P].
4. Stuck for 30 minutes? Read the official docs for the function involved. Only then look for help — and re-solve it from scratch the next morning.
5. End of day: run `pytest`, fill in `solutions/dayXX/README.md`, commit.

**Commit message format:** `dayXX: <what you built>` — e.g. `day07: searchsorted as-of join, look-ahead lab`. Several small commits per day look better than one dump.

## Rules that make this work

- **No copy-paste solutions.** Typing it yourself is the point.
- **Every [P] exercise gets tests.** From Day 12, CI must stay green.
- **Never peek into the future.** Every signal must be computable at the time it is used. You'll build tests that prove it.
- **Write down surprises.** A `notes/` entry for every "I didn't expect that" is worth more than the exercise itself.

## Progress

- [ ] Day 01  - [ ] Day 02  - [ ] Day 03  - [ ] Day 04  - [ ] Day 05  - [ ] **Day 06 (C1)**  - [ ] Day 07
- [ ] Day 08  - [ ] Day 09  - [ ] Day 10  - [ ] **Day 11 (C2)**  - [ ] Day 12  - [ ] Day 13  - [ ] Day 14
- [ ] Day 15  - [ ] **Day 16 (C3)**  - [ ] Day 17  - [ ] Day 18  - [ ] **Day 19 (C4)**  - [ ] **Day 20 (C4)**  - [ ] **Day 21 (C5)**
