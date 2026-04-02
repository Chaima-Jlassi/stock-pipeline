import pandas as pd

def transform(df: pd.DataFrame) -> pd.DataFrame:

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    # Daily return
    df["daily_return"] = df.groupby("ticker")["close_price"].pct_change()

    # Moving averages
    df["ma_7"]  = df.groupby("ticker")["close_price"].transform(
        lambda x: x.rolling(window=7).mean()
    )
    df["ma_30"] = df.groupby("ticker")["close_price"].transform(
        lambda x: x.rolling(window=30).mean()
    )

    # Volume spike flag
    volume_ma30 = df.groupby("ticker")["volume"].transform(
        lambda x: x.rolling(window=30).mean()
    )
    df["volume_spike"] = df["volume"] > 2 * volume_ma30

    # Drop rows where ma_30 is NaN (first 29 days)
    df = df.dropna(subset=["ma_30"])

    df = df.reset_index(drop=True)
    print(f"Transformed {len(df)} rows.")
    return df

if __name__ == "__main__":
    from extract import extract
    df_raw = extract()
    df_transformed = transform(df_raw)
    print(df_transformed.head())
    print(df_transformed.dtypes)