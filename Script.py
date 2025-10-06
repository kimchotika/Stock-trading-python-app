import requests
import os
import csv
from dotenv import load_dotenv

def run_stock_job():
    load_dotenv()
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

    LIMIT = 1000
    url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"

    tickers = []

    response = requests.get(url)
    data = response.json()

    tickers.extend(data.get("results", []))

    while "next_url" in data:
        print("Requesting next page:", data["next_url"])
        next_url = data["next_url"] + f"&apiKey={POLYGON_API_KEY}"
        response = requests.get(next_url)
        data = response.json()
        tickers.extend(data.get("results", []))

    print(f"Collected {len(tickers)} tickers")

    fieldnames = [
        "ticker",
        "name",
        "market",
        "locale",
        "primary_exchange",
        "type",
        "active",
        "currency_name",
        "cik",
        "composite_figi",
        "share_class_figi",
        "last_updated_utc"
    ]

    with open("tickers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickers)

    print("✅ Data written to tickers.csv")

# Optional: allow running manually
if __name__ == "__main__":
    run_stock_job()