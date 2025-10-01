

---

# 📊 Polygon.io Stock Ticker Data Pipeline

> 🏗️ *This project began as part of the [DataExpert.io Absolutely Free Beginner Data Engineering Boot Camp](https://dataexpert.io), where I learned the fundamentals of building data pipelines in Python.*
>
> 🚀 *I then extended the exercise into a real-world ETL workflow: integrating with the Polygon.io API, handling pagination, transforming JSON into tabular data, and writing the results into a structured CSV dataset with **~5000 US stock tickers**.*
>
> 📖 *This README documents not only the **how**, but also the **why**: how this project simulates the responsibilities of a Data Engineer in a production environment.*

---
## 🎓 Learning Outcomes

From this project, I learned how to:

* Extract data from a REST API with authentication and pagination.

* Transform JSON responses into structured tabular formats.

* Load results into a CSV file that can be imported into databases or BI tools.

* Securely manage credentials with environment variables (.env).

* Write clean, modular Python scripts that simulate real-world ETL pipelines.

* Think about scalability and maintainability (pagination loops, schema mapping, future DB integration).

---
## 📖 Business Scenario

In a financial analytics or trading company, a Data Engineering team might be responsible for maintaining a **reference database of all US-traded securities**.

This project simulates that workflow by:

* **Extracting** ticker metadata from Polygon’s REST API.
* **Transforming** semi-structured JSON into a structured dataset.
* **Loading** the final dataset into a CSV file for downstream use (databases, BI dashboards, ML pipelines).

---

## ⚙️ Tech Stack

* **Python 3.9+**
* [`requests`](https://pypi.org/project/requests/) → API integration
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) → secure API key management
* Built-in [`csv`](https://docs.python.org/3/library/csv.html) → writing structured data
* **Git/GitHub** → version control & collaboration

---

## 🛠️ How It Works

**1. Secure API key handling**
API key is stored in a `.env` file and loaded at runtime:

```env
POLYGON_API_KEY=your_api_key_here
```

**2. Extraction**
The script calls Polygon’s `/v3/reference/tickers` endpoint (`limit=1000` per page). Pagination is handled via `next_url`.

**3. Transformation**
Each response is parsed into structured fields:

* `ticker` (symbol)
* `name` (company/security name)
* `market` (stocks, crypto, fx)
* `primary_exchange`
* `type` (CS = common stock, ETF, etc.)
* `active` (boolean)
* `cik`, `composite_figi`, `share_class_figi`
* `last_updated_utc`

**4. Load**
All results are written to `tickers.csv`.

---

## 📊 Results

* ✅ Final dataset: **~5000 rows x 12 columns**
* ✅ Output file: `tickers.csv` (Excel/DB ready)
* ✅ Example row:

```csv
ticker,name,market,locale,primary_exchange,type,active,currency_name,cik,composite_figi,share_class_figi,last_updated_utc
AAPL,Apple Inc.,stocks,us,XNAS,CS,True,usd,0000320193,BBG000B9XRY4,BBG001S5N8V8,2025-10-01T06:06:06Z
```

---

## 🚀 Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/your-username/stock-ticker-pipeline.git
cd stock-ticker-pipeline

# 2. Create a virtual environment
python3 -m venv myenv
source myenv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key in .env
echo "POLYGON_API_KEY=your_api_key_here" > .env

# 5. Run the pipeline
python script.py
```

---

## 🛠️ Example Script

```python
import requests, os, csv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")

url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={API_KEY}"
tickers = []

while url:
    response = requests.get(url)
    data = response.json()
    tickers.extend(data.get("results", []))
    url = data.get("next_url")
    if url:
        url += f"&apiKey={API_KEY}"

fieldnames = [
    "ticker","name","market","locale","primary_exchange","type","active",
    "currency_name","cik","composite_figi","share_class_figi","last_updated_utc"
]

with open("tickers.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tickers)
```

---

## 🎯 Why This Matters for Data Engineering

This project reflects real-world **ETL (Extract, Transform, Load)** workflows:

* **Extract** → REST API integration with pagination.
* **Transform** → JSON parsing into structured schema.
* **Load** → CSV dataset ready for databases or BI.

It demonstrates:

* API-driven data ingestion.
* Secure credential management.
* Designing **scalable ingestion loops**.
* Producing datasets for downstream analytics.

---

## 🔮 Future Enhancements

* Save tickers into a **PostgreSQL / Snowflake** table instead of CSV.
* Add orchestration with **Airflow / Prefect** for scheduled runs.
* Transform CSV to **Parquet** for efficient analytics.
* Extend pipeline to collect **historical stock prices** for each ticker.

---

✨ With this project, I showcase my ability to **design and implement a real-world data pipeline** from external APIs to structured datasets — a key responsibility for Data Engineers.

---
