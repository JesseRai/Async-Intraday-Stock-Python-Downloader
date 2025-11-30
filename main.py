import httpx
import csv
import asyncio

# Inputs
alpha_base = "https://www.alphavantage.co/query"
api_key = "your_api_key_here"
symbols = ["AAPL", "MSFT", "AMZN"]
interval = "5min"

async def fetch_intraday(client, symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": api_key
    }
    response = await client.get(alpha_base, params=params, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    return symbol, data

async def main():

    # Fetch all symbols concurrently
    async with httpx.AsyncClient() as client:
        tasks = [fetch_intraday(client, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)

    # Write everything into one CSV
    with open('all_symbols.csv', 'w', newline='') as csvfile:
        fieldnames = ['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for symbol, data in results:
            print(f"Fetching intraday ({interval}) data for {symbol}")
            print(symbol, "Keys: ", list(data.keys()))

            time_series_key = f"Time Series ({interval})"
            if time_series_key not in data:
                print(f"WARNING: No '{time_series_key}' key for '{symbol}'. Got Keys: {list(data.keys())}")
                continue
            time_series_data = data[time_series_key]

            for timestamp, ohlcv in time_series_data.items():
                row = {
                    'symbol': symbol,
                    'timestamp': timestamp,
                    'open': float(ohlcv['1. open']),
                    'high': float(ohlcv['2. high']),
                    'low': float(ohlcv['3. low']),
                    'close': float(ohlcv['4. close']),
                    'volume': float(ohlcv['5. volume'])
                }

                writer.writerow(row)

        print("All data saved to all_symbols.csv")

if __name__ == "__main__":
    asyncio.run(main())
