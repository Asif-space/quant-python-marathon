# Capstone 2 — Commodity Risk & Futures Curve Lab

**Day 11 · Builds on Days 1–10 · Repo folder:** `capstones/c2_risklab/`

## Why this project
Risk modeling and curve analysis are core to every commodity desk. This project shows you can estimate covariance properly, decompose a futures curve into factors, simulate portfolio losses, and — critically — *test* whether your risk model is any good.

## Inputs
- `data/raw/panel_daily.parquet` — 12 commodities
- `data/raw/futures_cl.parquet` — individual CL contracts

## Design
```python
class RiskModel(ABC):
    @abstractmethod
    def fit(self, returns: np.ndarray) -> "RiskModel": ...
    @abstractmethod
    def covariance(self) -> np.ndarray: ...
```
Implementations: `SampleCov`, `EWMACov(lam)`, `ShrinkageCov(delta)` (constant-correlation or diagonal target).
Use `@dataclass` for configs and results, `Enum` for model names, a `@timer` decorator, and logging.

## Requirements

### Core
1. **Covariance models** (above), each tested on simulated data with a known covariance matrix.
2. **Model comparison:** rolling 1-day-ahead forecasts of equal-weight and minimum-variance portfolio volatility from each model over 2017–2025. Score with MSE and QLIKE against realized squared returns.
3. **Futures curve PCA:** constant-rank curve changes (M1…M12) computed within contracts; first three loadings, variance explained, factor time series. Chart of loadings vs maturity.
4. **Monte Carlo VaR/ES engine:** Cholesky-correlated Student-t shocks with the chosen covariance; 1-day 95% and 99% VaR and ES for a given weight vector; compare with historical-simulation VaR.
5. **VaR backtest:** rolling daily 99% VaR forecasts, count exceptions, implement the **Kupiec proportion-of-failures test** and the **Christoffersen independence test** from scratch (likelihood ratios, chi-square p-values).
6. CLI producing a report folder with tables and charts. ≥ 20 tests.

### Stretch
- Ledoit–Wolf optimal shrinkage intensity (implement the formula, check against `sklearn.covariance.LedoitWolf`).
- Stress scenarios: shock PCA factor 1 by ±3σ and reprice a calendar-spread position.
- Regime-aware VaR using a 2-state volatility classifier.

### Pro
- Numba-accelerated simulation with `prange` and reproducible `SeedSequence` streams.
- Property tests: every covariance output is symmetric positive semi-definite.

## Acceptance checks
- Exception rate of the best model within the Kupiec 95% acceptance region.
- PCA variance explained by the first three factors reported and sensible (level should dominate).
- All randomness reproducible from one seed.

## README must contain
- Model comparison table (MSE, QLIKE, exception rates, Kupiec/Christoffersen p-values)
- Curve loadings chart with interpretation
- VaR vs realized P&L chart with exceptions marked
- One paragraph: which model you'd use on a desk and why

## Common pitfalls
- Computing curve changes across a roll (the "M1" contract changes identity).
- Using the same day's data to forecast that day's VaR.
- Sample covariance with `rowvar` wrong.
