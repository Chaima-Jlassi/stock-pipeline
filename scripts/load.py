import mysql.connector
import pandas as pd
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        sys.exit(1)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            ticker       VARCHAR(10),
            date         DATE,
            open_price   FLOAT,
            high         FLOAT,
            low          FLOAT,
            close_price  FLOAT,
            volume       BIGINT,
            daily_return FLOAT,
            ma_7         FLOAT,
            ma_30        FLOAT,
            volume_spike BOOLEAN,
            PRIMARY KEY (ticker, date)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table ready.")

def load(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO stock_prices
            (ticker, date, open_price, high, low, close_price,
             volume, daily_return, ma_7, ma_30, volume_spike)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open_price   = VALUES(open_price),
            high         = VALUES(high),
            low          = VALUES(low),
            close_price  = VALUES(close_price),
            volume       = VALUES(volume),
            daily_return = VALUES(daily_return),
            ma_7         = VALUES(ma_7),
            ma_30        = VALUES(ma_30),
            volume_spike = VALUES(volume_spike)
    """

    rows = [
        (
            row.ticker,
            row.date.strftime("%Y-%m-%d") if hasattr(row.date, "strftime") else row.date,
            float(row.open_price),
            float(row.high),
            float(row.low),
            float(row.close_price),
            int(row.volume),
            float(row.daily_return) if pd.notna(row.daily_return) else None,
            float(row.ma_7)  if pd.notna(row.ma_7)  else None,
            float(row.ma_30) if pd.notna(row.ma_30) else None,
            bool(row.volume_spike)
        )
        for row in df.itertuples()
    ]

    cursor.executemany(sql, rows)
    conn.commit()
    print(f"{cursor.rowcount} rows upserted.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    from extract import extract
    from transform import transform
    create_table()
    df_raw = extract()
    df_transformed = transform(df_raw)
    load(df_transformed)
    print("Pipeline complete!")