# Async Intraday Stock Downloader (Python + HTTPX + AsyncIO)

This project demonstrates how to fetch multiple intraday stock time series concurrently using httpx.AsyncClient and asyncio.  
It retrieves intraday OHLCV data from the Alpha Vantage API, processes each symbol in parallel, and outputs a single consolidated CSV file containing all timestamps and prices for all selected tickers.

---

## Features
- Fully asynchronous API fetching using httpx.AsyncClient  
- Concurrent requests for all tickers  
- Clean tuple unpacking for (symbol, data)  
- Basic handling of missing data and rate-limit notes  
- Outputs one combined CSV: all_symbols.csv  
- Simple structure suitable for scaling into larger async market-data pipelines  

---

## Requirements

Install dependencies:

```bash
pip install httpx
```

asyncio is built into Python 3.7+

You will also need an Alpha Vantage API key.

---

## How It Works

1. fetch_intraday sends a request for a single symbol  
2. asyncio.gather runs all fetches concurrently  
3. Each result returns a tuple: (symbol, data)  
4. The script iterates over all timestamps and writes them to a unified CSV  
5. Any API warnings or rate limits are printed to the terminal  

---

## CSV Output Format

all_symbols.csv will contain:

| column    | description                   |
|-----------|-------------------------------|
| symbol    | The ticker symbol             |
| timestamp | Intraday timestamp            |
| open      | Opening price                 |
| high      | High price                    |
| low       | Low price                     |
| close     | Closing price                 |
| volume    | Trading volume (integer)      |

---

## Usage

Run the script:

```bash
python main.py
```

This will:
- Fetch intraday data for all symbols listed  
- Output diagnostic messages for missing keys or API notes  
- Save the final combined dataset to all_symbols.csv  

---

## Project Structure

```
.
├── main.py
├── all_symbols.csv        # created after running script
└── README.md
```

---

## Customisation

### Change symbols
Edit:

```python
symbols = ["AAPL", "MSFT", "AMZN"]
```

### Change interval
Valid Alpha Vantage intraday intervals include 1min, 5min, 15min, 30min, and 60min.

```python
interval = "5min"
```

### Use an environment variable for the API key
Recommended:

```bash
export ALPHAVANTAGE_API_KEY="your_key_here"
```

---

## Technologies Used
- Python 3.10+
- httpx for asynchronous HTTP requests  
- asyncio for concurrency  
- csv for output formatting  
