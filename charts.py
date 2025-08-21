"""
charts.py
---------
This file handles all chart plotting for the Stock Analyzer project.
It uses matplotlib to create line charts, moving averages, and
comparison charts. Charts help visualize stock trends and predictions.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_price(df: pd.DataFrame, symbol: str):
    """
    Plots the closing price of the stock.

    Args:
        df (pd.DataFrame): Data with stock prices.
        symbol (str): Stock symbol for title.
    """
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["Close"], label="Close Price", color="blue")
        plt.title(f"{symbol} Closing Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"[Error] Could not plot price chart: {e}")


def plot_moving_average(df: pd.DataFrame, symbol: str, window: int = 20):
    """
    Plots the closing price along with a moving average.

    Args:
        df (pd.DataFrame): Stock data.
        symbol (str): Stock symbol.
        window (int): Number of days for moving average.
    """
    try:
        ma = df["Close"].rolling(window=window).mean()

        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["Close"], label="Close Price", color="blue")
        plt.plot(df.index, ma, label=f"{window}-Day MA", color="red")
        plt.title(f"{symbol} Price with {window}-Day Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"[Error] Could not plot moving average chart: {e}")


def plot_comparison(df: pd.DataFrame, forecast_df: pd.DataFrame, symbol: str):
    """
    Plots historical close prices and forecasted prices together.

    Args:
        df (pd.DataFrame): Historical stock data.
        forecast_df (pd.DataFrame): Forecasted data.
        symbol (str): Stock symbol.
    """
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["Close"], label="Historical Price", color="blue")
        plt.plot(forecast_df.index, forecast_df["Forecast"], label="Forecast", color="green")
        plt.title(f"{symbol} Price vs Forecast")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"[Error] Could not plot comparison chart: {e}")
