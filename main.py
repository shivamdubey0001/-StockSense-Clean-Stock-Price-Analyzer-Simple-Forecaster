"""
StockSense - main.py
--------------------
This is the entry point of the StockSense CLI app.
It shows a friendly menu, loads settings from config.json,
and calls other modules (data_io, analytics, charts, forecast, utils).

Goal:
- Safe for beginners (won’t crash easily)
- Clear explanations for each step
- Works even if user presses wrong keys
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

# project modules
import data_io
import analytics
import charts
import forecast
import utils

# load config file safely
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[!] config.json not found. Using safe defaults...")
        return {
            "default_ticker": "AAPL",
            "start": "2018-01-01",
            "end": "today",
            "forecast_days": 7,
            "cache": True,
            "use_adjusted": True,
            "annualize_vol": False,
            "export_dir": "exports",
            "market": "US"
        }
    except Exception as e:
        print(f"[!] Failed to read config.json: {e}")
        return {}

# log every action (append to logs.csv)
def log_action(action, ticker, start, end, rows, status, note=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{ts},{action},{ticker},{start},{end},{rows},{status},{note}\n"
    try:
        with open("logs.csv", "a") as f:
            f.write(log_line)
    except Exception:
        print("[!] Could not write to logs.csv (ignoring).")

# main CLI loop
def main():
    config = load_config()
    ticker = config.get("default_ticker", "AAPL")
    start = config.get("start", "2018-01-01")
    end = config.get("end", "today")
    forecast_days = config.get("forecast_days", 7)

    data = None  # will store stock DataFrame when fetched

    while True:
        print("\n=== StockSense CLI ===")
        print("1. Fetch/Update Data")
        print("2. Analyze Indicators")
        print("3. Visualize Charts")
        print("4. Forecast Next N Days")
        print("5. Export Report")
        print("6. Quit")

        choice = input("Select option (1-6): ").strip()

        if choice == "1":
            # fetch or update
            try:
                ticker = input(f"Enter ticker (default {ticker}): ").strip() or ticker
                start = input(f"Start date (default {start}): ").strip() or start
                end = input(f"End date (default {end}): ").strip() or end

                print(f"\nFetching {ticker} from {start} → {end} ...")
                t0 = time.time()
                data = data_io.fetch_data(
                    ticker=ticker,
                    start=start,
                    end=end,
                    cache=config.get("cache", True)
                )
                elapsed = round((time.time() - t0) * 1000)
                print(f"✓ Data ready. Rows: {len(data)}")
                log_action("FETCH", ticker, start, end, len(data), "OK", f"{elapsed}ms")
            except Exception as e:
                print(f"[x] Failed to fetch data: {e}")
                log_action("FETCH", ticker, start, end, 0, "ERROR", str(e))

        elif choice == "2":
            if data is None:
                print("[!] No data yet. Please fetch first.")
                continue
            try:
                summary = analytics.analyze(data)
                utils.pretty_print_summary(summary, ticker, start, end)
                log_action("ANALYZE", ticker, start, end, len(data), "OK")
            except Exception as e:
                print(f"[x] Analysis failed: {e}")
                log_action("ANALYZE", ticker, start, end, len(data), "ERROR", str(e))

        elif choice == "3":
            if data is None:
                print("[!] No data yet. Please fetch first.")
                continue
            try:
                charts.generate_all(data, ticker, config)
                print("✓ Charts saved in exports/ folder")
                log_action("VISUALIZE", ticker, start, end, len(data), "OK")
            except Exception as e:
                print(f"[x] Chart generation failed: {e}")
                log_action("VISUALIZE", ticker, start, end, len(data), "ERROR", str(e))

        elif choice == "4":
            if data is None:
                print("[!] No data yet. Please fetch first.")
                continue
            try:
                n = input(f"Forecast days (default {forecast_days}): ").strip()
                n = int(n) if n else forecast_days
                result = forecast.run_baselines(data, n)
                utils.pretty_print_forecast(result)
                log_action("FORECAST", ticker, start, end, len(data), "OK")
            except Exception as e:
                print(f"[x] Forecasting failed: {e}")
                log_action("FORECAST", ticker, start, end, len(data), "ERROR", str(e))

        elif choice == "5":
            if data is None:
                print("[!] No data yet. Please fetch first.")
                continue
            try:
                analytics.export_report(data, ticker, start, end, config)
                print("✓ Report exported to exports/report_summary.csv")
                log_action("EXPORT", ticker, start, end, len(data), "OK")
            except Exception as e:
                print(f"[x] Export failed: {e}")
                log_action("EXPORT", ticker, start, end, len(data), "ERROR", str(e))

        elif choice == "6":
            print("Goodbye 👋")
            sys.exit(0)

        else:
            print("[!] Invalid choice. Please pick between 1–6.")

if __name__ == "__main__":
    main()
