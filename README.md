# 🧠 Economic Trend Analyzer

Automated Python system that fetches live U.S. macroeconomic data (CPI, GDP, and Unemployment) from the Federal Reserve API, analyzes recent trends, and generates timestamped daily reports.

---

## 📊 Features
- **Real data:** Uses the Federal Reserve’s FRED API for CPI, GDP, and Unemployment.
- **Automated workflow:** One run fetches, analyzes, and saves a report automatically.
- **Report generation:** Creates timestamped `.txt` reports summarizing trends and changes.
- **Trend detection:** Uses NumPy regression to estimate future direction (rising, stable, or falling).
- **Optional visualization:** Generates `matplotlib` line charts of all indicators.
- **Daily scheduling:** (Optional) Uses Python’s `schedule` library to auto-run the pipeline daily.

---

## 🧩 Tech Stack
- **Language:** Python 3.10+
- **Libraries:** `fredapi`, `numpy`, `matplotlib`, `schedule`, `certifi`
- **Concepts:** API integration, file I/O, automation, data analysis, linear regression

---

## 🚀 How It Works
1. `fetch_data.py` pulls CPI, GDP, and Unemployment data from the FRED API and logs them to `real_data.log`.
2. `main.py` reads that log, analyzes averages and trends, and writes a daily text report.
3. (Optional) `auto_run.py` automates the full process to run once a day.

Example output:
