# Capstone 1 — Commodity Data Quality & Returns Analytics Toolkit

**Day 6 · Builds on Days 1–5 · Repo folder:** `capstones/c1_qtools/`

## Why this project
Every quant research job starts with someone handing you messy data. Showing you can turn a dirty file into clean, validated, documented data — and then produce correct risk statistics — is exactly what a first-week task at a trading firm looks like.

## Inputs
- `data/raw/panel_daily_dirty.csv` (dirty)
- `data/raw/panel_daily.parquet` (clean reference, used **only** in tests)

## Package layout
```
c1_qtools/
├── src/qtools/
│   ├── __init__.py
│   ├── io.py          # loading with schema enforcement
│   ├── clean.py       # cleaning pipeline + report
│   ├── calendar.py    # TradingCalendar (Day 5)
│   ├── returns.py     # simple/log returns, compounding, resampling
│   ├── risk.py        # vol, Sharpe, Sortino, Calmar, drawdown table
│   └── report.py      # CLI entry point, tables and charts
├── tests/
├── reports/           # generated output (commit one example run)
├── pyproject.toml
└── README.md
```

## Requirements

### Core (must have)
1. `load_panel(path)` reads CSV or Parquet and enforces the schema.
2. `clean_panel(raw) -> (clean_df, report_dict)` fixes: symbol formatting, mixed date formats, volume strings, negative volumes, duplicates (with a documented rule), decimal-shift bad ticks, missing closes (forward fill with a limit — never backward fill).
3. Returns module: simple and log returns per symbol; weekly and monthly compounding.
4. Risk module, vectorized over all symbols: annualized return/vol, Sharpe, Sortino, max drawdown, Calmar, skew, kurtosis, hit rate, and `drawdown_table(top_n=5)`.
5. CLI: `python -m qtools.report data/raw/panel_daily_dirty.csv --out reports/` writes
   - `data_quality.md` — every fix with counts
   - `clean_panel.parquet`
   - `stats.csv` — one row per symbol
   - `figures/`: equity curves, drawdowns, return histogram vs fitted normal (one symbol), correlation heatmap
6. At least 20 `pytest` tests, including: cleaning matches the reference within tolerance; drawdown on a hand-built series; compounding identities; every risk metric against a loop-based reference.

### Stretch
- Logging instead of prints, configurable via CLI flag.
- Rolling 1-year Sharpe chart per symbol.
- Calendar-aware gap detection: flag missing trading days per symbol (not just NaNs).

### Pro
- `mypy --strict` clean, `ruff` clean.
- Data-quality checks as declarative rules (Day 7 style, can be added after Day 7).
- Report rendered as a single HTML page with embedded figures.

## Acceptance checks
- Cleaned closes match the reference on ≥ 99% of shared `(date, symbol)` rows with |diff| < 1e-6.
- No look-ahead in any fill step (write a test that proves it).
- `stats.csv` metrics match a pure-NumPy re-computation.

## README must contain
- One-paragraph problem statement
- Data-quality findings table (problem → count → fix)
- Stats table and two charts
- How to run (3 commands)
- Design decisions you made and why (e.g. dedup rule, fill limit)

## Common pitfalls
- Computing returns across symbol boundaries in the long format.
- Forward-filling prices across a symbol's listing gap (KC before 2016).
- Annualizing with 365 instead of 252 for daily trading data.
