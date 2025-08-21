# forecast.py
# -----------------------------------------------------------
# This file provides simple stock price forecasting functions.
# We will not use complex AI/ML here because the goal is
# lightweight, understandable, and useful predictions.
#
# Features:
# - Moving Average Forecast
# - Linear Trend Forecast
#
# Note: These are simple statistical methods.
# They don't guarantee accuracy like real financial models.
# -----------------------------------------------------------

import statistics
import numpy as np


def moving_average_forecast(prices, window=5, days=3):
    """
    Predict future stock prices using a simple moving average.

    Args:
        prices (list): List of past stock prices (float or int).
        window (int): Number of days to calculate moving average.
        days (int): Number of days to predict.

    Returns:
        list: Forecasted stock prices for the given days.
    """
    if not prices or len(prices) < window:
        return []

    forecast = []
    temp_prices = prices.copy()

    for _ in range(days):
        avg = statistics.mean(temp_prices[-window:])
        forecast.append(round(avg, 2))
        temp_prices.append(avg)

    return forecast


def linear_trend_forecast(prices, days=3):
    """
    Predict future stock prices using a simple linear trend.
    (Like fitting a straight line to the last few data points)

    Args:
        prices (list): List of past stock prices.
        days (int): Number of days to predict.

    Returns:
        list: Forecasted stock prices.
    """
    if not prices or len(prices) < 2:
        return []

    x = np.arange(len(prices))
    y = np.array(prices)

    # Fit a straight line (y = m*x + c)
    m, c = np.polyfit(x, y, 1)

    forecast = []
    for i in range(1, days + 1):
        future_x = len(prices) + i
        future_price = m * future_x + c
        forecast.append(round(future_price, 2))

    return forecast


if __name__ == "__main__":
    # Example test run
    sample_prices = [100, 102, 105, 107, 110, 115]

    print("Moving Average Forecast:", moving_average_forecast(sample_prices, window=3, days=5))
    print("Linear Trend Forecast:", linear_trend_forecast(sample_prices, days=5))
