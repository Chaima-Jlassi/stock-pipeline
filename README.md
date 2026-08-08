# Infer from code
A Python-based ETL pipeline for extracting, transforming, and loading stock market data.

## Table of Contents
* [Overview](#overview)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Pipeline Details](#pipeline-details)
* [Database Configuration](#database-configuration)
* [Code Structure](#code-structure)
* [Contributing](#contributing)
* [License](#license)

## Overview
This project uses Python to create an ETL pipeline for stock market data. It extracts data from Yahoo Finance, transforms it, and loads it into a MySQL database.

## Requirements
* Python 3.8+
* `yfinance` library for data extraction
* `mysql-connector-python` library for database connection
* `pandas` library for data manipulation
* `schedule` library for scheduling tasks
* `airflow` library for workflow management

## Installation
To install the required libraries, run the following command:
```bash
pip install yfinance mysql-connector-python pandas schedule airflow
```
## Usage
To run the pipeline, execute the `scheduler.py` file:
```bash
python scheduler.py
```
This will start the pipeline, which will extract data, transform it, and load it into the database.

## Pipeline Details
The pipeline consists of three main tasks:

1. **Extract**: Extracts stock market data from Yahoo Finance using the `yfinance` library.
2. **Transform**: Transforms the extracted data by calculating daily returns, moving averages, and volume spikes.
3. **Load**: Loads the transformed data into a MySQL database using the `mysql-connector-python` library.

## Database Configuration
The database configuration is stored in the `config/db_config.py` file. You can modify the configuration to connect to your own database.

## Code Structure
The code is organized into the following directories and files:

* `scheduler.py`: The main pipeline script.
* `dags/stock_dag.py`: The Airflow DAG file.
* `scripts/extract.py`: The data extraction script.
* `scripts/transform.py`: The data transformation script.
* `scripts/load.py`: The data loading script.
* `config/db_config.py`: The database configuration file.

## Contributing
To contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.