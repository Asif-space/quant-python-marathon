#!/usr/bin/env python3
"""
Synthetic market data for the 21-Day Quant Python Marathon.

Usage (from the repo root):
    python data/generate_data.py

Writes to data/raw/:
    futures_cl.parquet        Daily settles for individual CL-style crude contracts (2015-2025)
    panel_daily.parquet       Clean daily OHLCV for 12 commodities, long format
    panel_daily_dirty.csv     The same panel with realistic data errors injected
    eia_weekly.csv            Weekly crude inventory releases: consensus, actual, surprise
    ticks_quotes.parquet      Top-of-book quotes, 5 sessions, UTC timestamps (ns)
    ticks_trades.parquet      Trades for the same sessions (a few errors injected)
    lob_events.parquet        Level-3 order book event stream (add / cancel / execute), ~1 hour
    lob_final_snapshot.csv    Top 5 levels of the book after the last event (to check your replay)

Everything is synthetic and deterministic (seed=42), so it is safe to publish on GitHub.
Structure, quirks and pitfalls mirror real commodity data:
  - CL expiry rule: 3 business days before the 25th of the month before delivery
    (moved to the prior business day if the 25th is not one), US federal holidays.
  - Volume migrates from the front to the second contract before expiry (roll).
  - Panel returns have fat tails, volatility regimes, sector correlation, slow trends,
    winter volatility in natural gas, and real reactions to EIA inventory surprises.
  - Tick data has a U-shaped intraday activity pattern; trade signs carry
    short-term information about future mid-price moves.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

SEED = 42
OUT = Path(__file__).resolve().parent / "raw"
MONTH_CODES = "FGHJKMNQUVXZ"
START, END = "2015-01-02", "2025-12-31"
CBD = CustomBusinessDay(calendar=USFederalHolidayCalendar())

SYMBOLS = pd.DataFrame(
    [
        ("CL", "energy", 55.0, 0.35, 250_000),
        ("BRN", "energy", 57.0, 0.32, 180_000),
        ("NG", "energy", 2.9, 0.55, 120_000),
        ("HO", "energy", 1.9, 0.35, 60_000),
        ("RB", "energy", 1.5, 0.37, 55_000),
        ("GC", "metals", 1180.0, 0.15, 200_000),
        ("SI", "metals", 15.5, 0.27, 70_000),
        ("HG", "metals", 2.8, 0.22, 50_000),
        ("ZC", "ags", 395.0, 0.25, 300_000),
        ("ZS", "ags", 1020.0, 0.20, 180_000),
        ("ZW", "ags", 590.0, 0.30, 110_000),
        ("KC", "softs", 170.0, 0.33, 25_000),
    ],
    columns=["symbol", "sector", "start_price", "ann_vol", "avg_volume"],
)


def trading_calendar() -> pd.DatetimeIndex:
    return pd.date_range(START, END, freq=CBD)


# --------------------------------------------------------------------------- EIA
def gen_eia(rng: np.random.Generator, dates: pd.DatetimeIndex) -> pd.DataFrame:
    weds = pd.date_range(START, END, freq="W-WED")
    release = pd.DatetimeIndex([d if d in dates else d + CBD for d in weds])
    release = release[release <= dates[-1]]
    n = len(release)
    consensus = np.round(rng.normal(-0.5, 2.5, n), 1)
    actual = np.round(consensus + rng.normal(0, 3.5, n), 1)
    return pd.DataFrame(
        {
            "release_date": release,
            "release_time_et": "10:30",
            "consensus_mb": consensus,
            "actual_mb": actual,
            "surprise_mb": np.round(actual - consensus, 1),
        }
    )


# --------------------------------------------------------------------------- Panel
def correlation_matrix(sectors: list[str]) -> np.ndarray:
    n = len(sectors)
    c = np.full((n, n), 0.12)
    for i in range(n):
        for j in range(n):
            if sectors[i] == sectors[j]:
                c[i, j] = 0.55
    c[0, 1] = c[1, 0] = 0.93          # CL-BRN
    c[0, 3] = c[3, 0] = 0.75          # CL-HO
    c[0, 4] = c[4, 0] = 0.75          # CL-RB
    c[3, 4] = c[4, 3] = 0.70          # HO-RB
    c[5, 6] = c[6, 5] = 0.80          # GC-SI
    np.fill_diagonal(c, 1.0)
    w, v = np.linalg.eigh(c)          # repair to positive definite
    c = v @ np.diag(np.clip(w, 1e-4, None)) @ v.T
    d = np.sqrt(np.diag(c))
    return c / np.outer(d, d)


def gen_panel(rng: np.random.Generator, dates: pd.DatetimeIndex, eia: pd.DataFrame) -> pd.DataFrame:
    n, k = len(dates), len(SYMBOLS)
    dt = 1 / 252
    chol = np.linalg.cholesky(correlation_matrix(SYMBOLS.sector.tolist()))

    df_t = 4
    z = rng.standard_t(df_t, size=(n, k)) / np.sqrt(df_t / (df_t - 2))
    eps = z @ chol.T

    regime = np.zeros(n, dtype=int)
    for i in range(1, n):
        p_stay = 0.985 if regime[i - 1] == 0 else 0.95
        regime[i] = regime[i - 1] if rng.random() < p_stay else 1 - regime[i - 1]
    vol_mult = np.where(regime == 1, 2.0, 1.0)[:, None]

    seas = np.ones((n, k))
    seas[np.isin(dates.month, [12, 1, 2]), 2] = 1.5   # NG winter volatility

    sig = SYMBOLS.ann_vol.to_numpy()[None, :] * np.sqrt(dt) * vol_mult * seas

    mu = np.zeros((n, k))                            # slow trends (annualized drift)
    for i in range(1, n):
        mu[i] = mu[i - 1] - 1.5 * mu[i - 1] * dt + 0.4 * np.sqrt(dt) * rng.standard_normal(k)

    r = mu * dt - 0.5 * sig**2 + sig * eps

    rel = pd.Index(dates).get_indexer(eia.release_date)
    ok = rel >= 0
    shock = -0.004 * eia.surprise_mb.to_numpy()[ok] / 3.5
    for col, beta in [(0, 1.0), (1, 0.9), (3, 0.7), (4, 0.8)]:
        r[rel[ok], col] += beta * shock

    start = SYMBOLS.start_price.to_numpy()
    # weak pull of log price toward its long-run level keeps prices in realistic ranges
    log_p0 = np.log(start)
    log_p = np.empty((n, k))
    level = log_p0
    for i in range(n):
        r[i] -= 0.35 * (level - log_p0) * dt
        level = level + r[i]
        log_p[i] = level
    close = np.exp(log_p)
    prev = np.vstack([start, close[:-1]])
    open_ = prev * np.exp(sig * 0.25 * rng.standard_normal((n, k)))
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0, 0.5, (n, k))) * sig)
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0, 0.5, (n, k))) * sig)
    volume = (
        SYMBOLS.avg_volume.to_numpy() * np.exp(rng.normal(0, 0.25, (n, k))) * (1 + 20 * np.abs(r))
    ).astype(np.int64)

    idx = pd.MultiIndex.from_product([dates, SYMBOLS.symbol], names=["date", "symbol"])
    panel = pd.DataFrame(
        {
            "open": open_.ravel(),
            "high": high.ravel(),
            "low": low.ravel(),
            "close": close.ravel(),
            "volume": volume.ravel(),
        },
        index=idx,
    ).reset_index()
    panel[["open", "high", "low", "close"]] = panel[["open", "high", "low", "close"]].round(4)
    # KC "lists" later than the others -> staggered history (alignment exercises)
    panel = panel[~((panel.symbol == "KC") & (panel.date < "2016-06-01"))].reset_index(drop=True)
    return panel


def make_dirty(rng: np.random.Generator, panel: pd.DataFrame) -> pd.DataFrame:
    df = panel.copy()
    n = len(df)
    bad = rng.choice(n, 40, replace=False)                       # decimal-shift bad ticks
    df.loc[bad, "close"] = df.loc[bad, "close"].to_numpy() * rng.choice([10.0, 0.1], 40)
    miss = rng.choice(n, int(0.004 * n), replace=False)          # missing closes
    df.loc[miss, "close"] = np.nan
    neg = rng.choice(n, 30, replace=False)                       # impossible volumes
    df.loc[neg, "volume"] = -1
    df = df.drop(index=rng.choice(n, int(0.01 * n), replace=False))   # gaps
    dup = df.sample(frac=0.005, random_state=SEED)               # duplicates
    df = pd.concat([df, dup]).sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    sym = df.symbol.astype(object).to_numpy().copy()
    m = rng.random(len(df)) < 0.02
    sym[m] = [f" {s.lower()} " for s in sym[m]]
    df["symbol"] = sym

    ds = df.date.dt.strftime("%Y-%m-%d").to_numpy(dtype=object).copy()
    m = rng.random(len(df)) < 0.15
    ds[m] = df.date[m].dt.strftime("%Y%m%d").to_numpy()
    df["date"] = ds

    vol = df.volume.astype(str).to_numpy(dtype=object).copy()
    m = rng.random(len(df)) < 0.10
    vol[m] = [f"{int(v):,}" for v in df.volume.to_numpy()[m]]
    df["volume"] = vol
    return df


# --------------------------------------------------------------------------- Futures
def contract_table() -> pd.DataFrame:
    rows = []
    for p in pd.period_range("2015-01", "2028-12", freq="M"):
        prior = p - 1
        d25 = pd.Timestamp(prior.year, prior.month, 25)
        if not CBD.is_on_offset(d25):
            d25 = d25 - CBD
        expiry = d25 - 3 * CBD
        code = f"CL{MONTH_CODES[p.month - 1]}{p.year % 100:02d}"
        rows.append((code, p.to_timestamp(), expiry))
    return pd.DataFrame(rows, columns=["contract", "delivery_month", "expiry"])


def gen_futures(rng: np.random.Generator, dates: pd.DatetimeIndex) -> pd.DataFrame:
    n = len(dates)
    dt = 1 / 252
    x, s, c = np.empty(n), np.empty(n), np.empty(n)
    x[0], s[0], c[0] = np.log(55), 0.05, -0.01
    for i in range(1, n):
        jump = rng.normal(0, 0.08) if rng.random() < 0.004 else 0.0
        x[i] = x[i - 1] + 0.8 * (np.log(70) - x[i - 1]) * dt + 0.35 * np.sqrt(dt) * rng.standard_normal() + jump
        s[i] = s[i - 1] + 3.0 * (0.03 - s[i - 1]) * dt + 0.25 * np.sqrt(dt) * rng.standard_normal()
        c[i] = c[i - 1] + 3.0 * (-0.01 - c[i - 1]) * dt + 0.05 * np.sqrt(dt) * rng.standard_normal()

    contracts = contract_table()
    grid = pd.MultiIndex.from_product([dates, contracts.contract], names=["date", "contract"]).to_frame(index=False)
    grid = grid.merge(contracts, on="contract")
    days_to_exp = (grid.expiry - grid.date).dt.days
    tau = days_to_exp / 365.25
    keep = (days_to_exp >= 0) & (tau <= 1.5)
    grid, tau, days_to_exp = grid[keep].copy(), tau[keep], days_to_exp[keep]

    i = pd.Index(dates).get_indexer(grid.date)
    log_f = x[i] + s[i] * tau + c[i] * tau**2 + rng.normal(0, 0.002, len(grid))
    grid["settle"] = np.round(np.exp(log_f), 2)

    grid = grid.sort_values(["date", "expiry"]).reset_index(drop=True)
    rank = grid.groupby("date").cumcount().to_numpy() + 1
    dte = (grid.expiry - grid.date).dt.days.to_numpy()
    front_factor = np.clip(dte / 10.0, 0.05, 1.0)
    ff_by_date = pd.Series(front_factor[rank == 1], index=grid.date[rank == 1].to_numpy())
    ff_date = ff_by_date.reindex(grid.date.to_numpy()).to_numpy()

    w = np.exp(-0.45 * (rank - 1)).astype(float)
    w = np.where(rank == 1, w * ff_date, w)
    w = np.where(rank == 2, w + 0.9 * (1 - ff_date), w)
    grid["volume"] = (300_000 * w * np.exp(rng.normal(0, 0.3, len(grid)))).astype(np.int64)
    oi_w = np.exp(-0.30 * (rank - 1)) * np.where(rank == 1, np.sqrt(ff_date), 1.0)
    grid["open_interest"] = (400_000 * oi_w * np.exp(rng.normal(0, 0.05, len(grid)))).astype(np.int64)
    return grid[["date", "contract", "delivery_month", "expiry", "settle", "volume", "open_interest"]]


# --------------------------------------------------------------------------- Ticks
def gen_ticks(rng: np.random.Generator, n_days: int = 5, q_per_day: int = 80_000, t_per_day: int = 15_000):
    days = pd.bdate_range("2025-03-03", periods=n_days)
    session_ns = pd.Timedelta(hours=5).value
    mid = 6850
    q_frames, t_frames = [], []
    for day in days:
        open_utc = (day + pd.Timedelta(hours=8, minutes=30)).tz_localize("America/Chicago").tz_convert("UTC")

        def times(n: int) -> np.ndarray:
            return open_utc.value + (np.sort(rng.beta(0.6, 0.6, n)) * session_ns).astype(np.int64)

        q_ns = times(q_per_day)
        m = mid + np.cumsum(rng.choice([-1, 0, 1], size=q_per_day, p=[0.12, 0.76, 0.12]))
        mid = int(m[-1] + rng.integers(-30, 31))
        spread = rng.choice([1, 1, 1, 1, 2, 2, 3], q_per_day)
        bid, ask = m, m + spread
        q_frames.append(
            pd.DataFrame(
                {
                    "ts": pd.to_datetime(q_ns, utc=True),
                    "bid": bid / 100,
                    "ask": ask / 100,
                    "bid_size": rng.geometric(0.08, q_per_day),
                    "ask_size": rng.geometric(0.08, q_per_day),
                }
            )
        )
        t_ns = times(t_per_day)
        pos = np.clip(np.searchsorted(q_ns, t_ns, side="right") - 1, 0, None)
        fut = np.minimum(pos + 50, q_per_day - 1)
        p_buy = 0.5 + 0.15 * np.sign(m[fut] - m[pos])
        buy = rng.random(t_per_day) < p_buy
        t_frames.append(
            pd.DataFrame(
                {
                    "ts": pd.to_datetime(t_ns, utc=True),
                    "price": np.where(buy, ask[pos], bid[pos]) / 100,
                    "size": rng.geometric(0.35, t_per_day),
                    "side": np.where(buy, "B", "S"),
                }
            )
        )
    quotes = pd.concat(q_frames, ignore_index=True)
    trades = pd.concat(t_frames, ignore_index=True)
    dup = trades.sample(frac=0.001, random_state=SEED)
    trades = pd.concat([trades, dup]).sort_values("ts", kind="stable").reset_index(drop=True)
    order = np.arange(len(trades))
    for s in rng.choice(len(trades) - 1, 20, replace=False):
        order[s], order[s + 1] = order[s + 1], order[s]
    trades = trades.iloc[order].reset_index(drop=True)
    return quotes, trades


# --------------------------------------------------------------------------- Order book
def gen_lob(rng: np.random.Generator, n_events: int = 60_000):
    t = pd.Timestamp("2025-03-03 14:30", tz="UTC").value
    book: dict[str, dict[int, dict[int, int]]] = {"B": {}, "S": {}}
    loc: dict[int, tuple[str, int]] = {}
    ids: list[int] = []
    pos: dict[int, int] = {}
    rows: list[tuple] = []
    next_id = 1

    def add(side: str, price: int, size: int) -> None:
        nonlocal next_id
        oid = next_id
        next_id += 1
        book[side].setdefault(price, {})[oid] = size
        loc[oid] = (side, price)
        pos[oid] = len(ids)
        ids.append(oid)
        rows.append((t, oid, "A", side, price, size))

    def remove(oid: int) -> None:
        i = pos.pop(oid)
        last = ids.pop()
        if last != oid:
            ids[i] = last
            pos[last] = i
        side, price = loc.pop(oid)
        lvl = book[side][price]
        del lvl[oid]
        if not lvl:
            del book[side][price]

    for lvl in range(10):
        for _ in range(3):
            add("B", 6999 - lvl, int(rng.geometric(0.25)))
            add("S", 7001 + lvl, int(rng.geometric(0.25)))

    for _ in range(n_events):
        t += int(rng.exponential(60e6))
        bb, ba = max(book["B"]), min(book["S"])
        u = rng.random()
        nb, ns = len(book["B"]), len(book["S"])
        if u < 0.55 or nb < 5 or ns < 5:
            side = "B" if nb < 5 else "S" if ns < 5 else ("B" if rng.random() < 0.5 else "S")
            off = int(rng.geometric(0.35)) - 1
            # price relative to the opposite touch: off=0 joins/improves the inside, so spreads stay tight
            if side == "B":
                price = min(ba - 1, bb + 1) - off
            else:
                price = max(bb + 1, ba - 1) + off
            add(side, price, int(rng.geometric(0.25)))
        elif u < 0.88:
            oid = ids[rng.integers(len(ids))]
            side, price = loc[oid]
            rows.append((t, oid, "C", side, price, book[side][price][oid]))
            remove(oid)
        else:
            opp = "S" if rng.random() < 0.5 else "B"
            qty = int(rng.geometric(0.12))
            while qty > 0 and len(book[opp]) > 1:
                p = min(book[opp]) if opp == "S" else max(book[opp])
                lvl = book[opp][p]
                oid, rsz = next(iter(lvl.items()))
                fill = min(qty, rsz)
                qty -= fill
                rows.append((t, oid, "E", opp, p, fill))
                if fill == rsz:
                    remove(oid)
                else:
                    lvl[oid] = rsz - fill

    ev = pd.DataFrame(rows, columns=["ts", "order_id", "action", "side", "price", "size"])
    ev["ts"] = pd.to_datetime(ev.ts, utc=True)
    ev["price"] = ev.price / 100
    snap = []
    for side, prices in (("B", sorted(book["B"], reverse=True)[:5]), ("S", sorted(book["S"])[:5])):
        for lvl_no, p in enumerate(prices, start=1):
            snap.append((side, lvl_no, p / 100, sum(book[side][p].values()), len(book[side][p])))
    snapshot = pd.DataFrame(snap, columns=["side", "level", "price", "total_size", "n_orders"])
    return ev, snapshot


# --------------------------------------------------------------------------- main
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    dates = trading_calendar()

    eia = gen_eia(rng, dates)
    panel = gen_panel(rng, dates, eia)
    dirty = make_dirty(rng, panel)
    futures = gen_futures(rng, dates)
    quotes, trades = gen_ticks(rng)
    lob, snapshot = gen_lob(rng)

    eia.to_csv(OUT / "eia_weekly.csv", index=False)
    panel.to_parquet(OUT / "panel_daily.parquet", index=False)
    dirty.to_csv(OUT / "panel_daily_dirty.csv", index=False)
    futures.to_parquet(OUT / "futures_cl.parquet", index=False)
    quotes.to_parquet(OUT / "ticks_quotes.parquet", index=False)
    trades.to_parquet(OUT / "ticks_trades.parquet", index=False)
    lob.to_parquet(OUT / "lob_events.parquet", index=False)
    snapshot.to_csv(OUT / "lob_final_snapshot.csv", index=False)

    for name, df in [
        ("eia_weekly", eia), ("panel_daily", panel), ("panel_daily_dirty", dirty),
        ("futures_cl", futures), ("ticks_quotes", quotes), ("ticks_trades", trades),
        ("lob_events", lob),
    ]:
        print(f"{name:<20} {len(df):>10,} rows  {list(df.columns)}")
    print(f"\nWritten to {OUT}")


if __name__ == "__main__":
    main()
