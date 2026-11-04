# Capstone 4 — Event-Driven Microstructure Backtester & Market-Making Study

**Days 19–20 · Builds on Days 1–18 · Repo folder:** `capstones/c4_microstructure/`

## Why this project
Market-making and short-horizon firms want to see that you understand what a vectorized backtest hides: queue position, latency, adverse selection, and inventory risk. This project makes those visible.

## Inputs
- `data/raw/lob_events.parquet` + `lob_final_snapshot.csv` (order book replay and its check)
- `data/raw/ticks_quotes.parquet`, `ticks_trades.parquet` (top-of-book strategies)

## Architecture
```
c4_microstructure/
├── src/mstruct/
│   ├── events.py      # frozen dataclasses (Day 17)
│   ├── engine.py      # heap event queue + dispatcher
│   ├── book.py        # price-time order book (Day 13), optional Numba arrays
│   ├── exchange.py    # simulated matching: latency, queue position, partial fills
│   ├── strategies/
│   │   ├── base.py    # Strategy ABC: on_book, on_trade, on_fill, on_timer
│   │   ├── market_maker.py
│   │   └── ofi_taker.py
│   ├── accounting.py  # positions, PnL, attribution
│   └── report.py
└── tests/
```

## Requirements

### Section 1 — Event engine (Day 19)
- Events ordered by `(ts, priority, seq)`; deterministic replay; timers supported.

### Section 2 — Order book replay (Day 19)
- Replay all events; final top-5 levels must match `lob_final_snapshot.csv` exactly.
- Throughput reported (events/second); stretch: Numba array book ≥ 5× faster.

### Section 3 — Simulated exchange (Day 19)
- Your orders get a configurable latency (e.g. 0.5–5 ms) before reaching the book.
- **Queue position:** a resting limit order joins the back of the queue at its price; it fills only after the volume ahead of it is executed (cancels ahead of you reduce the queue — state your assumption).
- Market orders walk the book; partial fills supported; fees/rebates per contract.
- Tests: an order behind 10 lots is not filled by a 5-lot execution; latency changes which book state an order sees.

### Section 4 — Strategies (Day 20)
- **Market maker:** quote bid and ask around the microprice; skew quotes by inventory (`reservation price = microprice − γ·inventory`); hard inventory limit; cancel/replace when the fair value moves by a tick.
- **OFI taker:** cross the spread when short-horizon OFI exceeds a threshold; exit after a fixed horizon or a stop.

### Section 5 — Analysis (Day 20)
- **PnL attribution** for the market maker: spread capture vs adverse selection (mid move after your fills) vs inventory PnL.
- **Fill-assumption experiment:** run the market maker with (a) naive fills (any touch fills you), (b) queue-position fills, (c) queue-position fills + latency. Show how much PnL disappears at each step.
- Sensitivity: PnL vs latency, vs γ, vs quote size.

### Section 6 — Report & README (Day 20)
- Equity curve, inventory over time, fill rate, average adverse selection at 1s/5s/30s.
- Table: the three fill assumptions side by side.

### Pro
- Run the market maker over the quote/trade dataset as well (top-of-book approximation) and compare conclusions.
- Async version of the strategy runner reusing Day 18 code.

## Acceptance checks
- Snapshot match is exact.
- PnL reconciles: realized + unrealized = sum of attribution components (to the cent).
- Deterministic results across runs.

## README must contain
- Diagram of the event flow
- The fill-assumption table — this is your headline finding
- What you'd need from real data to trust the results (true queue data, exchange latency, fee schedule)

## Common pitfalls
- Letting your own order fill against liquidity that was consumed by someone else first.
- Ignoring that your cancels also have latency.
- Measuring adverse selection with the mid at fill time instead of after.
