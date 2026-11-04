# Day 19 — Capstone 4, Part 1: The Engine

Build the engine of **Capstone 4: Event-Driven Microstructure Backtester & Market-Making Study**.

➡️ Full spec: [`capstones/capstone4_microstructure_backtester.md`](../capstones/capstone4_microstructure_backtester.md)

**Today's scope:** spec sections 1–3 — event loop, order book replay, simulated exchange with latency and queue-position fills, and the test suite proving the engine is correct *before* any strategy touches it.

**Skills you're combining:** event-driven design (Day 17), heaps & order book (Day 13), dataclasses/ABCs (Day 9), Numba (Day 14), merge_asof & tick cleaning (Days 12, 17), testing & typing (Day 12).

**Time budget:** 8 h.

**Commit plan:**
1. `capstone4: event types and queue`
2. `capstone4: order book replay matches snapshot`
3. `capstone4: simulated exchange with latency + queue position`
4. `capstone4: engine test suite`
