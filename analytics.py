"""
analytics.py
-------------
This module calculates stock indicators and analysis summary:
- Daily returns (%), cumulative returns
- Moving averages (SMA/EMA)
- RSI (Relative Strength Index, 14-day)
- Volatility (30-day standard deviation of returns)
- Maximum drawdown
- Export summary report
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ===== Helper Functions ===== #

def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily returns and cumulative returns to the DataFrame."""
    df = df.copy()
    df["Return"] = df["Adj Close"].pct_change()
    df["Cumulative"] = (1 + df["Return"]).cumprod() - 1
    return df

def compute_sma(df: pd.DataFrame, window: int) -> pd.Series:
    """Simple Moving Average (SMA)."""
    return df["Adj Close"].rolling(window=window).mean()

def compute_ema(df: pd.DataFrame, window: int) -> pd.Series:
    """Exponential Moving Average (EMA)."""
    return df["Adj Close"].ewm(span=window, adjust=False).mean()

def compute_rsi(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    Compute RSI (Relative Strength Index).
    Uses Wilder's smoothing method.
    """
    delta = df["Adj Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window).mean()

    rs = avg_gain / (avg_loss + 1e-9)  # avoid division by zero
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_volatility(df: pd.DataFrame, window: int = 30, annualize: bool = False) -> float:
    """
    Compute volatility (std of daily returns).
    - window: number of days
    - annualize: if True, multiply by sqrt(252)
    """
    returns = df["Adj Close"].pct_change()
    vol = returns.tail(window).std()
    if annualize:
        vol *= np.sqrt(252)
    return vol * 100  # percentage

def compute_drawdown(df: pd.DataFrame):
    """
    Compute maximum drawdown and recovery period.
    Drawdown = peak-to-trough decline in value.
    """
    df = df.copy()
    df["Cumulative"] = (1 + df["Adj Close"].pct_change()).cumprod()
    cummax = df["Cumulative"].cummax()
    drawdown = (df["Cumulative"] - cummax) / cummax

    min_dd = drawdown.min()
    end_date = drawdown.idxmin()
    start_date = (df.loc[:end_date, "Cumulative"].idxmax()
                  if not df.loc[:end_date].empty else None)

    return {
        "max_drawdown": float(min_dd * 100),  # %
        "start_date": str(start_date.date()) if start_date else "N/A",
        "end_date": str(end_date.date()) if end_date else "N/A"
    }

# ===== Main Functions ===== #

def analyze(df: pd.DataFrame, annualize_vol: bool = False) -> dict:
    """
    Perform full analysis and return a compact summary dict.
    """
    if df is None or df.empty:
        raise ValueError("No data provided for analysis.")

    df = compute_returns(df)
    last_close = df["Adj Close"].iloc[-1]

    sma20 = compute_sma(df, 20).iloc[-1]
    sma50 = compute_sma(df, 50).iloc[-1]

    # SMA trend check
    if sma20 > sma50:
        sma_trend = "UP (bullish short-term)"
    elif sma20 < sma50:
        sma_trend = "DOWN (bearish short-term)"
    else:
        sma_trend = "Neutral"

    rsi_value = compute_rsi(df, 14).iloc[-1]
    if rsi_value < 30:
        rsi_status = f"{rsi_value:.2f} (oversold)"
    elif rsi_value > 70:
        rsi_status = f"{rsi_value:.2f} (overbought)"
    else:
        rsi_status = f"{rsi_value:.2f} (neutral)"

    vol30 = compute_volatility(df, window=30, annualize=annualize_vol)
    dd = compute_drawdown(df)

    summary = {
        "last_close": round(last_close, 2),
        "sma_trend": sma_trend,
        "rsi": rsi_status,
        "volatility_30d": round(vol30, 2),
        "max_drawdown": round(dd["max_drawdown"], 2),
        "dd_start": dd["start_date"],
        "dd_end": dd["end_date"]
    }
    return summary

def export_report(df: pd.DataFrame, ticker: str, start: str, end: str, config: dict):
    """
    Export analysis summary into a CSV report.
    """
    summary = analyze(df, annualize_vol=config.get("annualize_vol", False))
    export_dir = Path(config.get("export_dir", "exports"))
    export_dir.mkdir(exist_ok=True)

    report_path = export_dir / "report_summary.csv"

    # convert dict to single-row DataFrame for easy save
    row = pd.DataFrame([{
        "ticker": ticker,
        "period": f"{start} → {end}",
        **summary
    }])

    try:
        if report_path.exists():
            row.to_csv(report_path, mode="a", header=False, index=False)
        else:
            row.to_csv(report_path, index=False)
        print(f"[save] Report exported to {report_path}")
    except Exception as e:
        print(f"[!] Could not export report: {e}")
