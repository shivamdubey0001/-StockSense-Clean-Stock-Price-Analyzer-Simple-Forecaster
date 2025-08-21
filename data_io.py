"""
data_io.py
-----------
This module handles stock data input/output:
- Fetch from yfinance (OHLCV + Adj Close)
- Cache locally as CSV (in data/ folder)
- Read from cache if available
- Clean duplicates, missing days, timezone issues
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime
from pathlib import Path

# make sure data directory exists
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def safe_filename(ticker: str, start: str, end: str) -> str:
    """
    Generate a safe filename for cached data.
    Example: AAPL_2018-01-01_2025-08-21.csv
    """
    return f"{ticker.upper()}_{start}_{end}.csv"

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw stock data:
    - Remove duplicates
    - Drop rows with missing Close values
    - Reset timezone to naive (date-only index)
    """
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # Remove duplicate dates if any
    df = df[~df.index.duplicated(keep="last")]

    # Drop rows where 'Close' is missing
    df = df.dropna(subset=["Close"])

    # Reset timezone (yfinance gives UTC sometimes)
    if hasattr(df.index, "tz") and df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    return df

def fetch_data(ticker: str, start: str, end: str, cache: bool = True) -> pd.DataFrame:
    """
    Fetch stock OHLCV data for given ticker and date range.
    If cache is enabled, try loading from local CSV first.
    Otherwise, download from yfinance.
    """

    # handle "today" keyword
    if end.lower() == "today":
        end = datetime.today().strftime("%Y-%m-%d")

    file_path = DATA_DIR / safe_filename(ticker, start, end)

    # try cache first
    if cache and file_path.exists():
        try:
            df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
            df = clean_data(df)
            if not df.empty:
                print(f"[cache] Loaded {ticker} ({len(df)} rows) from {file_path}")
                return df
        except Exception as e:
            print(f"[!] Failed to load cache: {e}. Will re-download...")

    # fetch fresh from yfinance
    print(f"[net] Downloading {ticker} data from Yahoo Finance...")
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    except Exception as e:
        raise RuntimeError(f"yfinance download failed: {e}")

    df = clean_data(df)

    if df.empty:
        raise ValueError(f"No data found for {ticker} in {start} → {end}")

    # save to cache
    try:
        df.to_csv(file_path)
        print(f"[save] Cached to {file_path}")
    except Exception as e:
        print(f"[!] Could not save cache: {e}")

    return df

def read_offline(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Read stock data from local CSV only (no internet).
    Returns empty DataFrame if file not found.
    """
    file_path = DATA_DIR / safe_filename(ticker, start, end)
    if not file_path.exists():
        print(f"[!] Cache file not found: {file_path}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path, parse_dates=["Date"], index_col="Date")
        return clean_data(df)
    except Exception as e:
        print(f"[!] Failed to read cache: {e}")
        return pd.DataFrame()
