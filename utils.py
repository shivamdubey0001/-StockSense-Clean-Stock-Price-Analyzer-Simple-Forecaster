# utils.py
"""
Utility functions for Stock Price Analysis Project.
This file contains small helper functions to make the project
more user-friendly, safe, and readable.
"""

import os
import sys
import time


def clear_screen():
    """
    Clears the terminal screen for better readability.
    Works for Windows, macOS, and Linux.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        # If clear fails, just print some new lines
        print("\n" * 5)


def safe_input(prompt: str) -> str:
    """
    Handles user input safely. Prevents program crash if
    user suddenly presses Ctrl+D or Ctrl+Z.
    """
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n⚠️ Input cancelled by user.")
        sys.exit(0)


def show_progress(message: str = "Loading", steps: int = 5, delay: float = 0.3):
    """
    Displays a simple progress animation in the terminal.
    Example:
    Loading. 
    Loading.. 
    Loading...
    """
    for i in range(steps):
        dots = "." * (i % 4)
        print(f"\r{message}{dots}", end="")
        time.sleep(delay)
    print("\r" + " " * (len(message) + 4), end="\r")  # Clear line


def print_line(char: str = "-", length: int = 50):
    """
    Prints a horizontal line for neat separation in CLI.
    """
    print(char * length)


def safe_division(numerator: float, denominator: float) -> float:
    """
    Safely divides two numbers.
    Returns 0 if denominator is zero (to avoid crash).
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0.0
