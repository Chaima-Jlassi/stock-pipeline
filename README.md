#  Stock Market ETL Pipeline

An automated ETL pipeline that extracts, transforms, and loads daily stock market data into a MySQL database.

##  Architecture
```
yfinance API → extract.py → transform.py → load.py → MySQL
                                    ↓
                            schedule.py (daily run)
                                    ↓
                         dags/stock_dag.py (Airflow DAG)
```

##  Tech Stack

- **Python** — pandas, yfinance
- **MySQL** — data storage
- **Apache Airflow** — orchestration (DAG implemented)
- **schedule** — local daily execution

##  Project Structure
```
stock-pipeline/
├── dags/
│   └── stock_dag.py       ← Airflow DAG
├── scripts/
│   ├── extract.py         ← Fetches stock data via yfinance
│   ├── transform.py       ← Computes metrics (MA, daily return, volume spikes)
│   └── load.py            ← Upserts data into MySQL
├── config/
│   └── db_config.py       ← MySQL credentials (not tracked)
├── schedule.py            ← Runs pipeline daily at 09:00
├── requirements.txt
└── README.md
```

##  Tracked Stocks

| Ticker | Company |
|--------|---------|
| AAPL | Apple |
| MSFT | Microsoft |
| TSLA | Tesla |
| AMZN | Amazon |
| GOOGL | Google |

##  Computed Metrics

| Metric | Description |
|--------|-------------|
| `daily_return` | `(close - prev_close) / prev_close` |
| `ma_7` | 7-day moving average |
| `ma_30` | 30-day moving average |
| `volume_spike` | `True` if volume > 2× 30-day average |

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MySQL
Edit `config/db_config.py` with your credentials.

### 3. Run the pipeline
```bash
python schedule.py
```


yfinance
pandas
mysql-connector-python
schedule
apache-airflow
```
