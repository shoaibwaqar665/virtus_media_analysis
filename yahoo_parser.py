import requests
import datetime
import json

def get_full_historical_data(symbol: str, interval="1d", range_period="1mo"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    
    params = {
        "interval": interval,
        "range": range_period,
        "includePrePost": False,
        "events": "div,splits"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get data: {response.status_code}")
    
    data = response.json()
    result = data["chart"]["result"][0]

    timestamps = result["timestamp"]
    indicators = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose", [None]*len(timestamps))

    full_data = []
    for i in range(len(timestamps)):
        entry = {
            "date": datetime.datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d'),
            "open": indicators["open"][i],
            "high": indicators["high"][i],
            "low": indicators["low"][i],
            "close": indicators["close"][i],
            "volume": indicators["volume"][i],
            "adjclose": adjclose[i]
        }
        full_data.append(entry)

    # Sort data by date
    full_data_sorted = sorted(full_data, key=lambda x: x["date"], reverse=True)

    return full_data_sorted


# Example Usage
if __name__ == "__main__":
    symbol = "SHOT"
    data = get_full_historical_data(symbol, range_period="3mo")

    # Write sorted data to JSON file
    with open('yahoo_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Data saved to yahoo_data.json")
