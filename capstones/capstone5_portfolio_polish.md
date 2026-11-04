# Capstone 5 — Ship It: Research Library + Portfolio Polish

**Day 21 (morning, ~4–5 h) · Builds on everything · Repo folder:** `quantkit/` + repo-level README

## Why this project
Hiring managers spend minutes, not hours, on a GitHub profile. This turns 21 days of exercises into one installable library and a front page that shows your best work immediately.

## Requirements

### 1. `quantkit` — an installable library
Extract the reusable, tested pieces you built into one package:
```
quantkit/
├── pyproject.toml          # pip install -e .
├── src/quantkit/
│   ├── data/      # loaders, cleaning, TradingCalendar, ContinuousFuture
│   ├── stats/     # returns, risk metrics, drawdown table, OLS + Newey–West, bootstrap, deflated Sharpe
│   ├── risk/      # covariance models, VaR/ES, Kupiec/Christoffersen
│   ├── signals/   # Signal ABC, registry, momentum/carry/mean-reversion
│   ├── backtest/  # vectorized engine, cost models
│   └── micro/     # order book, OFI, microprice, Lee–Ready
└── tests/
```
- Capstones 1–4 import from `quantkit` where it makes sense (refactor at least two of them).
- `mypy` and `ruff` clean; CI green; test coverage reported (`pytest-cov`), aim for ≥ 80%.
- Docstrings (NumPy style) on every public function, with a formula where relevant.

### 2. Repo front page (`README.md` at the root)
- One-line summary of who you are and what this repo shows.
- A table: Capstone → question it answers → key result → link.
- 2–3 of your best charts embedded.
- Skills matrix: Python / NumPy / pandas topics → where each is demonstrated.
- How to reproduce everything (`python data/generate_data.py`, `pip install -e quantkit`, `pytest`).

### 3. Clean history
- Every day's folder has a short `README.md`: what you solved, what was hard, what you'd do differently.
- Remove dead code, notebooks with errors, and large files (`data/raw/` stays in `.gitignore` — it's reproducible).

### Pro
- Publish a short write-up (blog post or LinkedIn article) on the most interesting finding — e.g. the fill-assumption experiment or the look-ahead lab.
- Swap synthetic data for a free real source in one capstone (e.g. EIA API for inventories, CFTC COT data) and compare.

## Acceptance checks
- A stranger can clone, run three commands, and reproduce your headline charts.
- CI badge green on the README.
