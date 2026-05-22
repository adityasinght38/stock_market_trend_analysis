# 📈 Stock Market Trend Analysis

A Python-based stock market analytics project that collects historical market data, performs time-series analysis, computes technical indicators, and visualizes long-term price trends and market volatility.

This project demonstrates financial data analysis, trend forecasting concepts, risk analysis, and data visualization using real-world stock market datasets.

---

## 🚀 Features

- Live stock market data fetching using `yfinance`
- 50-day & 200-day Simple Moving Averages (SMA)
- Golden Cross / Death Cross signal detection
- 21-day annualized volatility analysis
- RSI (14-period) momentum indicator
- Comparative normalized performance analysis across multiple stocks
- Automatic CSV export for processed datasets
- Time-series trend visualization using Matplotlib

---

## 🔑 Skills Demonstrated

- Financial Data Analysis
- Time-Series Analysis
- Data Visualization
- Technical Indicator Analysis
- Exploratory Data Analysis (EDA)
- Python Programming
- Risk & Volatility Analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data manipulation & time-series analysis |
| NumPy | Statistical calculations |
| Matplotlib | Data visualization |
| yfinance | Historical stock market data API |

---

## 📦 Installation

```bash
git clone https://github.com/adityasinght38/stock-market-trend-analysis.git

cd stock-market-trend-analysis

pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python stock_trend_analysis.py
```

---

## ⚙️ Configuration

Modify the configuration block inside `stock_trend_analysis.py`:

```python
TICKERS = ["AAPL", "MSFT", "GOOGL"]

START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

SHORT_WINDOW = 50
LONG_WINDOW = 200
```

---

## 📊 Output Files

| File | Description |
|------|-------------|
| `{TICKER}_trend_analysis.png` | Price trends, SMA, volatility & RSI visualization |
| `{TICKER}_data.csv` | Processed stock market dataset |
| `comparative_performance.png` | Multi-stock normalized comparison chart |

---

## 📸 Sample Analysis Dashboard

```
┌─────────────────────────────────┐
│  Close Price + SMA50 + SMA200   │
│  + Buy/Sell Signal Detection    │
├─────────────────────────────────┤
│  21-day Rolling Volatility (%)  │
├─────────────────────────────────┤
│  RSI (14) Momentum Indicator    │
└─────────────────────────────────┘
```

---

## 🔍 Key Technical Indicators

| Indicator | Interpretation |
|-----------|---------------|
| SMA 50 > SMA 200 | Bullish trend (Golden Cross) |
| SMA 50 < SMA 200 | Bearish trend (Death Cross) |
| RSI > 70 | Overbought condition |
| RSI < 30 | Oversold condition |

---

## 📂 Project Structure

```text
stock_market_trend_analysis/
├── stock_trend_analysis.py
├── requirements.txt
├── README.md
├── comparative_performance.png
└── sample_outputs/
```

---

## 📈 Project Workflow

1. Collected historical stock market data
2. Cleaned and processed time-series datasets
3. Calculated moving averages and volatility
4. Generated RSI momentum indicators
5. Created comparative stock visualizations
6. Exported processed datasets for analysis

---

## 🚀 Future Improvements

- Real-time stock market dashboard
- Streamlit web application integration
- Machine Learning-based trend prediction
- Portfolio optimization analytics
- Interactive visualization dashboards

---

## 👤 Author

**Aditya Thakur**  
B.Tech Computer Science Engineering, VIT  

🔗 GitHub: https://github.com/adityasinght38
