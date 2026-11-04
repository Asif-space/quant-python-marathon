# Day 18 — Async Streams, Execution Analytics, Event Studies

**Theme:** Handle live-style data streams, measure trading costs and liquidity, and test whether scheduled news really moves prices.
**Time budget:** ~7 h
**Save to:** `solutions/day18/`

---

## Track A — Python: `asyncio`

- **P18.1 [E]** `async def`, `await asyncio.sleep`, `asyncio.gather` of three coroutines. Show total time ≈ the longest, not the sum.
- **P18.2 [M]** Async generator replaying `ticks_quotes.parquet` at 100× speed (sleep scaled to real inter-arrival times).
- **P18.3 [M]** Producer/consumer with `asyncio.Queue`: feed → signal → order logger. Use bounded queues and observe backpressure.
- **P18.4 [H]** Timeouts and cancellation: a watchdog that raises an alert if no quote arrives for 2 (simulated) seconds; cancel tasks cleanly on shutdown.
- **P18.5 [P]** **Async paper trader.** Two feeds (quotes, trades) merged; a microprice/OFI signal; orders sent to a simulated exchange with random latency; fills logged to Parquet; graceful shutdown on Ctrl+C. Tests with `pytest-asyncio`.

## Track B — NumPy: liquidity and execution

- **N18.1 [E]** VWAP and TWAP over 5-minute windows from trades.
- **N18.2 [M]** **Kyle's lambda:** regress 5-minute mid changes on signed volume. Units and interpretation.
- **N18.3 [M]** **Roll's spread estimator** `2·sqrt(−cov(Δp_t, Δp_{t−1}))` from trade prices. Compare with the actual quoted spread.
- **N18.4 [H]** Implementation shortfall: execute a 500-lot parent order via TWAP and via 10% POV against the recorded trades and quotes. Cost in bps vs the arrival mid, per day.
- **N18.5 [P]** **Queue position model.** For a limit buy joining the best bid at time *t*, estimate fill probability within 1/5/30 seconds from `lob_events` (executions consume the queue ahead; assume cancels are uniformly distributed in the queue). Monte Carlo over many start times.

## Track C — pandas: seasonality and event studies

- **D18.1 [E]** Intraday seasonality: mean and std of 5-minute mid returns by time of day (Chicago time).
- **D18.2 [M]** EIA event study on daily CL: release-day return vs non-release days; by surprise sign; by surprise quintile. t-tests.
- **D18.3 [M]** Event windows [−5, +5] trading days around each release. Abnormal return = return minus trailing 60-day mean (computed *before* the window). Average CAR with a 95% confidence band.
- **D18.4 [H]** Regress release-day CL return on the surprise (in standard deviations). Robustness: winsorized surprise, HAC errors, first half vs second half of the sample, and HO/RB/BRN as dependent variables.
- **D18.5 [P]** Generic `event_study(returns, events, window, model="mean"|"market")` returning tidy CAR results with confidence intervals. Validate by injecting a known effect into simulated data and recovering it.

---

## Interview drill
1. What does Kyle's lambda measure?
2. Why might a TWAP schedule underperform POV on a volatile day?
3. Why must the "normal return" in an event study be estimated before the event window?

## Done when
- [ ] EIA event-study chart saved
- [ ] Committed: `day18: asyncio paper trader, execution costs, EIA event study`
- [ ] **Tomorrow starts Capstone 4 (two days)** — read the spec tonight
