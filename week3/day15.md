# Day 15 — Parallelism, Options & Multiple Testing, Continuous Futures

**Theme:** Run research at scale without fooling yourself, price futures options, and build the continuous futures series every commodity strategy starts from.
**Time budget:** ~7–8 h
**Save to:** `solutions/day15/`

---

## Track A — Python: concurrency for research

- **P15.1 [E]** `ProcessPoolExecutor` to run one backtest per symbol in parallel. Compare with sequential.
- **P15.2 [M]** `ThreadPoolExecutor` for I/O: simulate downloading 50 files (`time.sleep(0.2)` each). Collect results with `as_completed` and handle one failing task.
- **P15.3 [M]** Pickling problems: try sending a `lambda` and a 1 GB DataFrame to worker processes. Fix with module-level functions and an `initializer` that loads data once per worker.
- **P15.4 [H]** Parallel parameter sweep: 500 `(lookback, threshold)` combinations, chunked, with progress logging and deterministic per-task seeds (`SeedSequence.spawn`).
- **P15.5 [P]** **Walk-forward optimization engine.** Rolling train/test windows; parallel parameter search on each train window; apply the winner to the following test window; stitch the out-of-sample equity curve. Report how often the chosen parameters change and the in-sample vs out-of-sample Sharpe gap.

## Track B — NumPy: options and statistical honesty

- **N15.1 [E]** `SeedSequence(...).spawn(n)` for independent streams. Show why `seed + i` is a weak alternative.
- **N15.2 [M]** Variance reduction for an arithmetic Asian option on a futures price: antithetic variates + control variate (geometric Asian closed form). Report the variance reduction factor.
- **N15.3 [M]** Black-76 vectorized over a grid of strikes × expiries, with delta, gamma, vega. Implied volatility by vectorized Newton–Raphson with a bisection fallback when vega is tiny.
- **N15.4 [H]** Simulate the CL futures curve 20 days ahead from your Day 9 PCA factors (bootstrap factor shocks). Distribution of the M1−M3 calendar spread; 5th/95th percentiles.
- **N15.5 [P]** **Multiple testing.** Simulate 1,000 strategies on pure noise; plot the distribution of the *maximum* Sharpe vs the number of trials. Implement the **Deflated Sharpe Ratio** (Bailey & López de Prado) and apply it to your P15.4 sweep. Is the winner real?

## Track C — pandas: continuous futures construction

Data: `futures_cl.parquet`

- **D15.1 [E]** Naive front-month series (nearest expiry each day). Plot it and mark the jumps at rolls.
- **D15.2 [E]** Roll schedule: roll *N = 5* business days before expiry. Produce a table of roll dates with from/to contracts.
- **D15.3 [M]** Open-interest rule: switch when M2 open interest exceeds M1. Compare roll dates with the calendar rule. Which rolls earlier?
- **D15.4 [M]** Back-adjustment: difference (additive) vs ratio (multiplicative). Plot unadjusted vs both adjusted series. When can difference adjustment produce negative historical prices?
- **D15.5 [H]** Compute daily returns from the contract *actually held* each day. Show these equal ratio-adjusted returns exactly, and explain why difference-adjusted returns don't.
- **D15.6 [H]** Annualized carry `ln(F1/F2) / (T2 − T1)` as a daily series. Relationship with the subsequent month's front-month return?
- **D15.7 [P]** **`ContinuousFuture` class:** parameters `rule` (calendar/oi/volume), `offset`, `adjust` (none/diff/ratio); outputs price series, held contract per day, and a roll log. Invariant tests: returns match held-contract returns; no date is missing; the held contract is never past expiry.

---

## Interview drill
1. What is the expected maximum Sharpe of N independent zero-skill strategies, roughly?
2. Black-76 vs Black–Scholes: what changes and why?
3. Why must commodity backtests use roll-adjusted data?

## Done when
- [ ] `ContinuousFuture` tested (Capstone 3 depends on it)
- [ ] Committed: `day15: walk-forward engine, black-76 & deflated sharpe, continuous futures`
