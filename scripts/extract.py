import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

TICKERS = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]
END_DATE = datetime.today().strftime("%Y-%m-%d")
START_DATE = (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d")

def extract():
    all_data = []

    for ticker in TICKERS:
        print(f"Extracting {ticker}...")
        df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True)

        if df.empty:
            print(f"No data for {ticker}, skipping.")
            continue

        df = df.reset_index()
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        df["ticker"] = ticker
        df = df.rename(columns={
            "Date":   "date",
            "Open":   "open_price",
            "High":   "high",
            "Low":    "low",
            "Close":  "close_price",
            "Volume": "volume"
        })
        df = df[["ticker", "date", "open_price", "high", "low", "close_price", "volume"]]
        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)
    print(f"Extracted {len(final_df)} rows total.")
    return final_df

if __name__ == "__main__":
    df = extract()
    print(df.head())