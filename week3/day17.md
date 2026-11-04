# Day 17 — Event-Driven Design, Microstructure Metrics, Tick Data

**Theme:** Move from daily bars to the order book. Build the event-driven pieces you'll need for Capstone 4, and measure what really happens at the tick level.
**Time budget:** ~7–8 h
**Save to:** `solutions/day17/`

Data: `ticks_quotes.parquet`, `ticks_trades.parquet`, `lob_events.parquet`

---

## Track A — Python: event-driven architecture

- **P17.1 [E]** Frozen dataclasses for events: `MarketEvent`, `SignalEvent`, `OrderEvent`, `FillEvent`, each with `ts` and a `priority`.
- **P17.2 [M]** Event queue on `heapq` ordered by `(ts, priority, seq)`. Test that same-timestamp events come out in the intended order (market data before signals before orders).
- **P17.3 [M]** Dispatcher: `dict[type, list[Callable]]`; `subscribe(event_type, handler)`; `run()` loops until the queue is empty. Handlers may push new events.
- **P17.4 [H]** Merge quotes, trades and scheduled EIA releases into one lazy stream with generators + `heapq.merge`. Verify global time order and count events by type.
- **P17.5 [P]** **Reconciliation.** Event-driven daily backtester for one Capstone 3 strategy. It must reproduce the vectorized PnL (same costs, same timing). Document every discrepancy you hit and its cause — reconciling two engines is a real job skill.

## Track B — NumPy: order book and microstructure metrics

- **N17.1 [E]** Mid, spread (ticks) and relative spread (bps) from quotes. Distribution by hour of day.
- **N17.2 [E]** Microprice `(bid·ask_size + ask·bid_size) / (bid_size + ask_size)`. How far from mid on average?
- **N17.3 [M]** Top-of-book imbalance `(bid_size − ask_size)/(bid_size + ask_size)`. Correlation with the mid change over the next 10, 50, 200 quote updates.
- **N17.4 [M]** **Order Flow Imbalance** (Cont, Kukanov & Stoikov) from consecutive quotes, fully vectorized with `np.where` on bid/ask price changes.
- **N17.5 [H]** Aggregate OFI and mid changes into 10-second intervals. Regress mid change on OFI with `lstsq`; report the slope and R² per day.
- **N17.6 [P]** Reconstruct top-5 depth on a 1-second grid from `lob_events.parquet` with a Numba array-based book (prices as integer tick offsets into a fixed array). Check the final state against `lob_final_snapshot.csv` and your P13.8 book.

## Track C — pandas: tick data processing

- **D17.1 [E]** Clean trades: drop duplicates, sort by time, detect the out-of-order rows (`is_monotonic_increasing`, then locate them).
- **D17.2 [E]** Per-day statistics: trade count, volume, VWAP, high, low, buy-volume share.
- **D17.3 [M]** Intraday volume curve: 5-minute buckets in Chicago time, averaged across days. Plot the U-shape.
- **D17.4 [M]** Realized variance from mid returns sampled every 1s, 5s, 30s, 1min, 5min. Plot the **volatility signature** (RV vs sampling interval) and explain the shape.
- **D17.5 [H]** Volume bars and dollar bars from trades. Jarque–Bera test on returns for time, volume and dollar bars. Which is closest to normal?
- **D17.6 [P]** **Price impact response function.** Average mid move `k` trades after a buy vs a sell (k = 1…200), using `merge_asof` to get mids. Also the autocorrelation of trade signs. Plot both and interpret.

---

## Interview drill
1. What is the microprice and why is it a better fair value than the mid?
2. Why does realized variance blow up at very high sampling frequencies?
3. In an event-driven backtester, why does event ordering at equal timestamps matter?

## Done when
- [ ] Event-driven and vectorized engines reconcile
- [ ] Committed: `day17: event engine, OFI & microprice, tick data analysis`
