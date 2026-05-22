# 📈 Stock Market Trend Analysis

A Python-based project that collects historical stock market data, performs time-series analysis, computes moving average indicators, and visualises price trends and volatility.

---

## 🚀 Features

- **Live Data Fetching** via `yfinance` API (falls back to synthetic data automatically)
- **50-day & 200-day Simple Moving Averages (SMA)** to identify long-term trends
- **Golden Cross / Death Cross** detection for buy/sell signals
- **21-day Annualised Volatility** analysis
- **RSI (14-period)** momentum indicator with overbought/oversold zones
- **Comparative normalised performance** chart across multiple stocks
- Exports cleaned data to CSV for further analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data manipulation & time-series |
| Matplotlib | Visualisation |
| yfinance | Historical stock data API |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stock-market-trend-analysis.git
cd stock-market-trend-analysis

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python stock_trend_analysis.py
```

To change the tickers or date range, edit the **Configuration** block at the top of `stock_trend_analysis.py`:

```python
TICKERS     = ["AAPL", "MSFT", "GOOGL"]   # Add any valid ticker symbols
START_DATE  = "2022-01-01"
END_DATE    = "2024-12-31"
SHORT_WINDOW = 50    # Short moving average window
LONG_WINDOW  = 200   # Long moving average window
```

---

## 📊 Output

For each ticker the script generates:

| File | Description |
|------|-------------|
| `{TICKER}_trend_analysis.png` | 3-panel chart: price+SMAs, volatility, RSI |
| `{TICKER}_data.csv` | Full OHLCV + indicator data |
| `comparative_performance.png` | Normalised multi-stock comparison chart |

### Sample Chart Layout

```
┌─────────────────────────────────┐
│  Close Price + SMA50 + SMA200   │  ← Golden/Death cross signals
│  + Crossover signals            │
├─────────────────────────────────┤
│  21-day Rolling Volatility (%)  │
├─────────────────────────────────┤
│  RSI (14)  [0–100]              │  ← Overbought > 70, Oversold < 30
└─────────────────────────────────┘
```

---

## 📂 Project Structure

```
stock_market_trend_analysis/
├── stock_trend_analysis.py   # Main analysis script
├── requirements.txt          # Python dependencies
└── README.md
```

---

## 🔍 Key Concepts

| Indicator | Interpretation |
|-----------|---------------|
| **SMA 50 > SMA 200** | Bullish trend (Golden Cross) |
| **SMA 50 < SMA 200** | Bearish trend (Death Cross) |
| **RSI > 70** | Overbought — potential reversal down |
| **RSI < 30** | Oversold — potential reversal up |

---

## 👤 Author

**Aditya Thakur**  
[LinkedIn](https://linkedin.com) • [GitHub](https://github.com)  
B.Tech Computer Science, VIT
