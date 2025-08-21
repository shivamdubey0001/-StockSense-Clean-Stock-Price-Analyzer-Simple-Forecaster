# 📈 StockSense - Clean Stock Price Analyzer & Simple Forecaster

Hey! 👋 I'm Shivam Dubey, and welcome to **StockSense** - my take on making stock analysis simple and accessible for everyone!

## 🤔 What is StockSense?

StockSense is a lightweight command-line tool that helps you analyze stock prices without all the complexity of heavy machine learning or expensive software. It's perfect for students, beginners, or anyone who wants clean stock insights quickly.

**In simple words**: Give it a stock symbol → Get clean data, helpful indicators, nice charts, and basic forecasts. All from your terminal!

## ✨ What Can It Do?

- **📊 Fetch Real Stock Data**: Get live stock prices from Yahoo Finance
- **🔍 Smart Analysis**: Calculate useful indicators like moving averages, RSI, volatility
- **📈 Beautiful Charts**: Generate clean, easy-to-read price charts and technical indicators  
- **🔮 Simple Forecasting**: Predict next few days using proven baseline methods
- **💾 Smart Caching**: Save data locally so you don't re-download everything
- **📋 Export Reports**: Get your analysis in CSV format for further use

## 🎯 Why StockSense?

- **No Complex Setup**: Just Python and a few basic libraries
- **Fast & Light**: Works great even on Chromebooks or basic computers
- **Educational**: Learn about stock indicators without overwhelming complexity
- **Practical**: Get actionable insights, not just fancy graphs
- **Free**: Uses free data sources, no expensive subscriptions needed

## 📁 Project Structure

```
StockSense/
│── README.md          # This guide you're reading
│── requirements.txt   # Required Python packages  
│── config.json        # Settings (default stock, date ranges, etc.)
│── main.py           # Main program with friendly menu
│── data_io.py        # Handles downloading and saving stock data
│── analytics.py      # Calculates all the technical indicators
│── forecast.py       # Simple prediction models
│── charts.py         # Creates beautiful charts
│── utils.py          # Helper functions
│── logs.csv          # Keeps track of what you've analyzed
└── data/             # Your downloaded stock data gets saved here
    └── AAPL_2018-01-01_2025-08-21.csv  # Example cached data
```

## 🚀 Quick Start

### Installation
1. Make sure Python 3.7+ is installed
2. Download this project
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### First Run
```bash
python main.py
```

You'll see a friendly menu like this:
```
📈 Welcome to StockSense!
1. 📊 Fetch/Update Data
2. 🔍 Analyze Indicators  
3. 📈 Visualize Charts
4. 🔮 Forecast Next N Days
5. 📋 Export Report
6. ❌ Quit
>> 
```

## 💡 How to Use

### Step 1: Fetch Data
- Choose option 1
- Enter a stock symbol (like AAPL, TSLA, MSFT)
- Pick your date range (or use defaults)
- The tool downloads and saves the data

### Step 2: Analyze
- Choose option 2  
- Get a quick snapshot of key indicators:
  - Current price vs moving averages
  - RSI (momentum indicator)
  - Volatility levels
  - Maximum drawdown (biggest loss period)

### Step 3: Visualize
- Choose option 3
- Beautiful charts get saved to `exports/` folder:
  - Price with moving averages
  - RSI momentum chart
  - Drawdown visualization

### Step 4: Forecast
- Choose option 4
- Get simple predictions for next few days using three methods:
  - **Naive**: Assumes price stays same
  - **Moving Average**: Uses recent average trend
  - **Drift Model**: Considers recent price momentum
- Tool picks the most accurate method automatically

### Step 5: Export Report
- Choose option 5
- Get a CSV summary with all key metrics

## 📊 Example Output

When you analyze a stock, you might see:

```
📊 Analysis Snapshot
Ticker: AAPL | Period: 2018-01-01 → 2025-08-21 | Rows: 1,845
Last Close: $224.15
SMA20 vs SMA50: UP (bullish short-term trend)
RSI(14): 62.4 (neutral-high momentum)  
30d Volatility: 1.42%
Max Drawdown: -28.6% (from Jan 2022 to Jun 2022)
```

```
🔮 Forecast Summary
Models tested (accuracy):
 - Naive: 3.12 RMSE
 - MovingAvg(10): 2.85 RMSE  
 - Drift(60): 2.67 RMSE ← best model

Next 7 trading days prediction:
 2025-08-22: $225.10
 2025-08-23: $225.45
 ...

Files saved: exports/forecast.png, exports/forecast.csv
```

## 🛠️ Configuration

Edit `config.json` to set your preferences:

```json
{
  "default_ticker": "AAPL",
  "start": "2018-01-01", 
  "end": "today",
  "forecast_days": 7,
  "cache": true
}
```

## 🧠 What You'll Learn

Using StockSense, you'll get familiar with:

- **Moving Averages (SMA/EMA)**: Trend indicators
- **RSI**: Momentum indicator (overbought/oversold signals)
- **Volatility**: How much prices swing around
- **Drawdown**: Understanding risk and recovery
- **Basic Forecasting**: Simple but effective prediction methods

## 💻 Perfect For

- **Students**: Learning about financial analysis
- **Beginners**: First time analyzing stocks
- **Chromebook Users**: Lightweight, browser-friendly
- **Budget-conscious**: No expensive software needed
- **Quick Analysis**: Fast insights without complexity

## 🔧 Technical Details

- **Data Source**: Yahoo Finance (free and reliable)
- **Forecasting**: Three baseline models (no heavy ML)
- **Charts**: Clean matplotlib visualizations
- **Storage**: Local CSV caching for offline analysis
- **Logging**: Automatic tracking of all your analysis sessions

## ⚠️ Important Notes

- This tool provides **educational insights**, not financial advice
- Predictions are simple baselines - real markets are complex!
- Always do your own research before making investment decisions
- Keep your data updated for best accuracy

## 🔮 Future Ideas

I'm planning to add:
- More technical indicators (MACD, Bollinger Bands)
- Portfolio analysis (multiple stocks at once)
- Simple alert system for price targets
- Web dashboard version
- Crypto support

## 🤝 Want to Help?

Found a bug? Have suggestions? I'd love to hear from you! This project started as a learning exercise and I'm always looking to improve it.

## 📝 Final Thoughts

StockSense is designed to make stock analysis approachable and educational. Whether you're a student learning about finance or someone curious about the stock market, I hope this tool helps you understand how technical analysis works.

Remember - the best investment is in your own learning! Use this tool to understand patterns, but always think critically about what the data is telling you.

Happy analyzing! 📈

---

*Built with ❤️ by Shivam Dubey*

> **Disclaimer**: This tool is for educational purposes only. Not financial advice. Always consult professionals for investment decisions and do your own research.