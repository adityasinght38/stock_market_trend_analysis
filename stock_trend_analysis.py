"""
Stock Market Trend Analysis
Author: Aditya Thakur
Description: Collects historical stock data, performs time-series analysis,
             calculates moving averages and visualizes price trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings("ignore")

# ── Try yfinance; fall back to synthetic data ──────────────────────────────────
try:
    import yfinance as yf
    USE_LIVE = True
except ImportError:
    USE_LIVE = False

# ── Configuration ──────────────────────────────────────────────────────────────
TICKERS     = ["AAPL", "MSFT", "GOOGL"]
START_DATE  = "2022-01-01"
END_DATE    = "2024-12-31"
SHORT_WINDOW = 50    # 50-day moving average
LONG_WINDOW  = 200   # 200-day moving average


# ── Data Collection ────────────────────────────────────────────────────────────
def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker.
    Uses yfinance when available; otherwise generates synthetic data for demo.
    """
    if USE_LIVE:
        print(f"  Fetching live data for {ticker} ...")
        df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
        df = df[["Close", "Volume"]].copy()
        df.columns = ["Close", "Volume"]
    else:
        print(f"  Generating synthetic data for {ticker} (yfinance not installed) ...")
        import numpy as np
        np.random.seed(hash(ticker) % 2**31)
        dates = pd.date_range(START_DATE, END_DATE, freq="B")
        prices = 150 * (1 + np.random.randn(len(dates)).cumsum() * 0.01).cumprod()
        volume = np.random.randint(10_000_000, 80_000_000, size=len(dates))
        df = pd.DataFrame({"Close": prices, "Volume": volume}, index=dates)

    df.index.name = "Date"
    return df


# ── Feature Engineering ────────────────────────────────────────────────────────
def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Add short-term and long-term simple moving averages."""
    df[f"SMA_{SHORT_WINDOW}"]  = df["Close"].rolling(window=SHORT_WINDOW).mean()
    df[f"SMA_{LONG_WINDOW}"]   = df["Close"].rolling(window=LONG_WINDOW).mean()
    return df


def add_volatility(df: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Add rolling 21-day annualised volatility (std of daily returns × √252)."""
    daily_ret = df["Close"].pct_change()
    df["Volatility_21d"] = daily_ret.rolling(window).std() * (252 ** 0.5)
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add Relative Strength Index (RSI)."""
    delta = df["Close"].diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, float("nan"))
    df["RSI_14"] = 100 - (100 / (1 + rs))
    return df


def detect_golden_death_cross(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mark Golden Cross  (SMA_50 crosses above SMA_200) → bullish signal
    Mark Death  Cross  (SMA_50 crosses below SMA_200) → bearish signal
    """
    prev_short = df[f"SMA_{SHORT_WINDOW}"].shift(1)
    prev_long  = df[f"SMA_{LONG_WINDOW}"].shift(1)

    df["Golden_Cross"] = (
        (df[f"SMA_{SHORT_WINDOW}"] > df[f"SMA_{LONG_WINDOW}"]) &
        (prev_short <= prev_long)
    )
    df["Death_Cross"] = (
        (df[f"SMA_{SHORT_WINDOW}"] < df[f"SMA_{LONG_WINDOW}"]) &
        (prev_short >= prev_long)
    )
    return df


# ── Visualisation ──────────────────────────────────────────────────────────────
def plot_ticker(df: pd.DataFrame, ticker: str) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(14, 11),
                             gridspec_kw={"height_ratios": [3, 1, 1]},
                             sharex=True)
    fig.suptitle(f"{ticker}  –  Stock Trend Analysis", fontsize=16, fontweight="bold")

    # ── Panel 1: Price + Moving Averages + Crossover Signals ──────────────────
    ax = axes[0]
    ax.plot(df.index, df["Close"],
            label="Close Price", color="#2196F3", linewidth=1.2)
    ax.plot(df.index, df[f"SMA_{SHORT_WINDOW}"],
            label=f"{SHORT_WINDOW}-day SMA", color="#FF9800", linewidth=1.5, linestyle="--")
    ax.plot(df.index, df[f"SMA_{LONG_WINDOW}"],
            label=f"{LONG_WINDOW}-day SMA", color="#E91E63", linewidth=1.5, linestyle="--")

    gc = df[df["Golden_Cross"]]
    dc = df[df["Death_Cross"]]
    ax.scatter(gc.index, gc["Close"], marker="^", color="green",
               s=120, zorder=5, label="Golden Cross ▲")
    ax.scatter(dc.index, dc["Close"], marker="v", color="red",
               s=120, zorder=5, label="Death Cross ▼")

    ax.set_ylabel("Price (USD)")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)

    # ── Panel 2: Volatility ────────────────────────────────────────────────────
    axes[1].plot(df.index, df["Volatility_21d"] * 100,
                 color="#9C27B0", linewidth=1.2)
    axes[1].axhline(y=df["Volatility_21d"].mean() * 100,
                    color="gray", linestyle=":", linewidth=1, label="Mean vol")
    axes[1].set_ylabel("21d Vol (%)")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.3)

    # ── Panel 3: RSI ──────────────────────────────────────────────────────────
    axes[2].plot(df.index, df["RSI_14"], color="#00BCD4", linewidth=1.2, label="RSI (14)")
    axes[2].axhline(70, color="red",   linestyle="--", linewidth=0.8, label="Overbought (70)")
    axes[2].axhline(30, color="green", linestyle="--", linewidth=0.8, label="Oversold (30)")
    axes[2].fill_between(df.index, df["RSI_14"], 70,
                         where=(df["RSI_14"] >= 70), alpha=0.2, color="red")
    axes[2].fill_between(df.index, df["RSI_14"], 30,
                         where=(df["RSI_14"] <= 30), alpha=0.2, color="green")
    axes[2].set_ylim(0, 100)
    axes[2].set_ylabel("RSI")
    axes[2].legend(fontsize=8)
    axes[2].grid(alpha=0.3)

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    axes[2].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    fname = f"{ticker}_trend_analysis.png"
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    print(f"  Chart saved → {fname}")
    plt.close()


# ── Summary Statistics ─────────────────────────────────────────────────────────
def print_summary(df: pd.DataFrame, ticker: str) -> None:
    latest = df["Close"].iloc[-1]
    start  = df["Close"].iloc[0]
    total_return = (latest - start) / start * 100
    annual_vol   = df["Volatility_21d"].mean() * 100
    golden = df["Golden_Cross"].sum()
    death  = df["Death_Cross"].sum()

    print(f"\n  ── {ticker} Summary ──")
    print(f"     Period         : {df.index[0].date()} → {df.index[-1].date()}")
    print(f"     Start Price    : ${start:,.2f}")
    print(f"     End Price      : ${latest:,.2f}")
    print(f"     Total Return   : {total_return:+.1f}%")
    print(f"     Avg Volatility : {annual_vol:.1f}%  (annualised)")
    print(f"     Golden Crosses : {golden}")
    print(f"     Death  Crosses : {death}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("   Stock Market Trend Analysis")
    print("=" * 55)

    all_close = {}

    for ticker in TICKERS:
        print(f"\n[{ticker}]")
        df = fetch_stock_data(ticker)
        df = add_moving_averages(df)
        df = add_volatility(df)
        df = add_rsi(df)
        df = detect_golden_death_cross(df)

        print_summary(df, ticker)
        plot_ticker(df, ticker)

        df.to_csv(f"{ticker}_data.csv")
        print(f"  Data saved  → {ticker}_data.csv")
        all_close[ticker] = df["Close"]

    # ── Comparative price chart (normalised to 100) ────────────────────────────
    compare = pd.DataFrame(all_close).dropna()
    normalised = compare / compare.iloc[0] * 100

    fig, ax = plt.subplots(figsize=(13, 5))
    for col in normalised.columns:
        ax.plot(normalised.index, normalised[col], label=col, linewidth=1.5)

    ax.axhline(100, color="gray", linestyle=":", linewidth=0.8)
    ax.set_title("Comparative Performance (Normalised to 100)", fontsize=14, fontweight="bold")
    ax.set_ylabel("Indexed Price")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("comparative_performance.png", dpi=150, bbox_inches="tight")
    print("\n  Comparative chart saved → comparative_performance.png")
    plt.close()

    print("\n✅  Analysis complete!")


if __name__ == "__main__":
    main()
