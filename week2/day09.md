# Day 09 — Dataclasses & ABCs, PCA, Exponential Weighting

**Theme:** Design clean domain objects, decompose risk into factors, and estimate volatility the way risk systems do.
**Time budget:** ~7 h
**Save to:** `solutions/day09/`

---

## Track A — Python: dataclasses, enums, ABCs, composition

- **P9.1 [E]** `Enum`s: `Side`, `OrderType` (`MARKET`, `LIMIT`, `STOP`), `TimeInForce`. Iterate them; convert from strings safely.
- **P9.2 [E]** `@dataclass(frozen=True, slots=True) class Fill(ts, symbol, side, qty, price, fee)`. Demonstrate that mutation raises.
- **P9.3 [M]** `Order` dataclass with `field(default_factory=...)` for an id and `__post_init__` validation (qty > 0, limit price required for `LIMIT`, price is a multiple of the tick).
- **P9.4 [M]** Abstract base class `Signal` with abstract `compute(prices: np.ndarray) -> np.ndarray`. Implement `Momentum(lookback)`, `MeanReversion(lookback, z)`, `Breakout(lookback)`. Instantiating `Signal` directly must fail.
- **P9.5 [M]** Composition: `Strategy(signal, sizer, risk_limit)` where each component is swappable. Run three combinations on CL without writing any subclass of `Strategy`.
- **P9.6 [H]** Benchmark 1,000,000 `Fill`s as `slots=True` dataclass, normal dataclass, plain class and `namedtuple`: memory and creation time.
- **P9.7 [P]** **Mini framework (seed of Capstone 4).** `Strategy` ABC with `on_bar(bar)`; `Broker` that accepts `Order` dataclasses and returns `Fill`s; pluggable `SlippageModel` and `FeeModel` objects. Run a simple momentum strategy on daily CL. Tests for fills, fees and slippage.

## Track B — NumPy: linear algebra II (eigen, SVD, Cholesky, conditioning) → PCA

- **N9.1 [E]** `np.cov(R)` vs `np.cov(R, rowvar=False)` on a `(T, 12)` array. Show the shape trap. Then `np.corrcoef`.
- **N9.2 [E]** `np.linalg.eigh` on the covariance matrix. Sort eigenvalues descending; explained-variance ratio and cumulative.
- **N9.3 [M]** PCA of the 12 commodity returns: project onto the first 3 components. Plot loadings and interpret (do the sectors show up?).
- **N9.4 [M]** PCA via SVD of the demeaned data. Prove numerically that `singular_values² / (T − 1)` equals the eigenvalues and that the components match up to sign.
- **N9.5 [M]** Cholesky: simulate 10,000 days of correlated normals with the sample correlation matrix. Compare empirical vs target correlation (max absolute error).
- **N9.6 [H]** Condition number of the sample covariance as the sample shrinks (`T = 500, 250, 100, 50, 30`) for 12 assets, then for 100 simulated assets. Then shrink toward the diagonal, `Σ̂ = δF + (1−δ)S`, for several δ and show condition number and out-of-sample minimum-variance portfolio vol.
- **N9.7 [P]** **Futures curve PCA.** From `futures_cl.parquet`, build a `(T, 12)` matrix of daily log settle changes for the 1st…12th contracts (rank by expiry; compute each change *within the same contract*, never across a roll). PCA → plot level/slope/curvature loadings against maturity and report variance explained.

## Track C — pandas: `ewm`, rolling covariance/correlation

- **D9.1 [E]** `ewm(span=20).mean()` vs `rolling(20).mean()` on CL. Plot and describe the lag difference.
- **D9.2 [E]** Convert between `span`, `halflife`, `alpha` and `com`. Assert that equivalent parameters give identical results.
- **D9.3 [M]** RiskMetrics EWMA volatility (λ = 0.94) vs 20-day rolling volatility. Which reacts faster to shocks? Show with a specific date.
- **D9.4 [M]** `adjust=True` vs `adjust=False`: hand-code the recursion `s_t = α x_t + (1−α) s_{t−1}` and match one of them exactly. Explain the difference at the start of the series.
- **D9.5 [M]** 120-day rolling correlation and EWM correlation between CL and GC. Do you see regime changes?
- **D9.6 [H]** `df.ewm(span=60).cov()` returns a MultiIndex frame. Extract the covariance matrix on a chosen date, and compute the equal-weight portfolio vol over time.
- **D9.7 [P]** **Volatility targeting.** Position per asset = 10% / (EWMA vol forecast), *lagged one day*. Report realized vol per year vs target. Then evaluate forecasts (rolling vs EWMA) with MSE and QLIKE loss against realized squared returns.

---

## Interview drill
1. What do the first three principal components of a futures curve usually represent?
2. Why does a covariance matrix with more assets than observations cause problems?
3. What does λ = 0.94 mean as a half-life in days?

## Done when
- [ ] Curve PCA chart saved to `solutions/day09/figures/`
- [ ] Committed: `day09: dataclass framework, PCA & shrinkage, EWMA vol targeting`
