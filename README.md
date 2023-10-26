# Didi Index Stock Checker

The Didi Index Stock Checker is a Python script designed to automate the process of checking stocks that are close to triggering the Didi Index condition. This script is inspired by Didi Aguiar's technique, which involves the use of moving averages (MA) with periods typically set to 3, 8, and 20. The "needle point" occurs when these three MAs cross each other at the same time, known as the "perfect needle point."

## Didi Index Overview

The Didi Index is a technical indicator used in stock trading. It is based on the concept of moving average crossovers. The key elements are as follows:

- 3-period, 8-period, and 20-period moving averages are used.
- When the 3-period MA crosses above the 8-period MA and the 20-period crosses below the 8-period MA, it's considered a BUY event.
- When the 3-period MA crosses below the 8-period MA and the 20-period crosses above the 8-period MA, it's considered a SELL event.
- The "perfect needle point" occurs when all three MAs cross simultaneously.

## Usage

The script reads a list of stock codes from a CSV file, `stock_list.csv`, located in the same folder as the script. The stock codes in this file should follow the yfinance format (e.g., `PETR4.SA` for Petrobras stock on B3 – São Paulo stock market). The script then uses the Yahoo Finance API to download historical stock prices and applies the Didi Index logic to identify stocks that meet the criteria.

The script categorizes stocks into two groups:

1. **Perfect Needle Points**: Stocks that exhibit the "perfect needle point" where all three MAs cross simultaneously. These are potentially significant trading opportunities.

2. **Attention Stocks**: Stocks that show MAs crossing very close in time. These stocks warrant further examination.

## Notes

- The script focuses on the Didi Index using moving averages but does not consider other indicators like ADX, Bollinger Bands, Trix, or Stochastic, which are part of the broader Didi Aguiar's technique.

- By automating the process of identifying potential Didi Index conditions, this script saves time compared to manually checking each stock in the list.

- This is not a complete trading system, it is a tool that simplifies stock trend analysis.

## Instructions

1. Create a CSV file named `stock_list.csv` in the same folder as the `didi_check.py` script.
2. In `stock_list.csv`, list the stock codes you want to check using the yfinance format.
3. Run the `didi_check.py` script to analyze the stocks in the list.
