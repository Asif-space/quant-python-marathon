# Day 12 — Types & Tests, Advanced Vectorization, Merging

**Theme:** Make your code trustworthy (types, tests, CI), push NumPy vectorization further, and join datasets correctly — including the as-of join that microstructure research depends on.
**Time budget:** ~7 h
**Save to:** `solutions/day12/`

---

## Track A — Python: type hints, `mypy`, testing

- **P12.1 [E]** Add full type hints to your Capstone 1 package. Run `mypy --strict` on one module and fix every error.
- **P12.2 [E]** `TypedDict` for a backtest config; `Protocol` named `SupportsCompute` so any object with `.compute(prices)` type-checks as a signal (no inheritance).
- **P12.3 [M]** `pytest`: a `conftest.py` fixture providing a small sample panel, `@pytest.mark.parametrize` across symbols, and `tmp_path` for file output tests.
- **P12.4 [M]** Testing numbers: `pytest.approx`, `np.testing.assert_allclose(rtol=, atol=)`, `pd.testing.assert_frame_equal(check_exact=False)`. Write one test that *should* fail with a tight tolerance and passes with a sensible one.
- **P12.5 [H]** Property-based tests with `hypothesis`: drawdowns are always ≤ 0; prices → returns → prices round-trips; your FIFO ledger's position always equals the signed sum of fills; realized PnL is invariant to splitting a fill into two.
- **P12.6 [H]** Generics: `RingBuffer[T]` with `TypeVar` and `Generic`; mypy should reject pushing a `str` into a `RingBuffer[float]`.
- **P12.7 [P]** Add `pre-commit` (ruff + mypy) and a GitHub Actions workflow running `pytest` on every push. Add the CI badge to the repo README. From now on, every commit must pass.

## Track B — NumPy: `sliding_window_view`, `einsum`, vectorizing loops, Numba intro

- **N12.1 [E]** Rolling mean with `sliding_window_view` and with the cumulative-sum trick. Compare speed and floating-point error.
- **N12.2 [E]** Six `einsum` equivalences, each asserted: dot product, matrix product, trace, row sums, column sums, outer product.
- **N12.3 [M]** Rolling std vectorized with `sliding_window_view(..., axis=0)` on `(T, 12)`. Match pandas `rolling(20).std()`.
- **N12.4 [M]** Variances of 10,000 random portfolios at once: `W (N, A)`, `Σ (A, A)` → `np.einsum("ij,jk,ik->i", W, Σ, W)`. Compare against a loop.
- **N12.5 [M]** Time-varying risk: covariance stack `(T, A, A)` (from Day 9 EWM) and weights `(T, A)` → daily portfolio vol in one `einsum`.
- **N12.6 [H]** Rolling regression slope of all 12 assets on the equal-weight index at once using sliding windows `(T, A, W)`. Watch memory; choose `W` and dtype sensibly.
- **N12.7 [P]** **Path dependence.** Trailing stop-loss strategy (exit when price falls X% from the highest price since entry, re-enter on a new 20-day high). Write it as a plain Python loop; attempt a vectorized version and document *why* it's hard; then write it with `@numba.njit`. Benchmark all three and verify identical results.

## Track C — pandas: `merge`, `join`, `concat`, `merge_asof`

- **D12.1 [E]** `concat` a list of per-symbol frames with `keys=` to build a MultiIndex.
- **D12.2 [E]** Make a small metadata table (symbol, sector, exchange, tick size, multiplier). `merge` onto the panel with `validate="many_to_one"`. Break it deliberately (duplicate a metadata row) and read the error.
- **D12.3 [M]** Inner / left / outer joins with `indicator=True`. Diagnose which keys failed to match and why.
- **D12.4 [M]** EIA onto daily data two ways: an exact `merge` on date (left), then `merge_asof(direction="backward")` so every day carries the most recent release. Compare.
- **D12.5 [H]** `merge_asof` trades to quotes (`direction="backward"`, `tolerance=pd.Timedelta("1s")`). Compute effective spread `2·|price − mid|`, and classify each trade as at bid, at ask, or inside. Accuracy of the quote rule vs the true `side` column?
- **D12.6 [H]** `allow_exact_matches=False`: when trade and quote share a timestamp, which quote should a trade see? Build a tiny example and argue the case both ways.
- **D12.7 [P]** **Lee–Ready classification:** quote rule, with the tick rule as a fallback for trades at the midpoint, plus an optional quote lag in milliseconds. Report a confusion matrix vs the true side for several lags. Package it as a tested function.

---

## Interview drill
1. What's the difference between a `Protocol` and an ABC?
2. Express `w.T @ Σ @ w` for many portfolios at once with `einsum`.
3. Why do you need `merge_asof` instead of `merge` for trades and quotes?

## Done when
- [ ] CI is green on GitHub
- [ ] Committed: `day12: typing & CI, einsum & numba, merge_asof & Lee-Ready`
