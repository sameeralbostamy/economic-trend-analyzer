#fetch_data.py
#Fetches real economic data from FRED and writes it to a log file

from fredapi import Fred 
from datetime import datetime

API_KEY = "314349ed9f3b38d1d9003d0c1d4768a4"

def fetch_and_log():
    fred = Fred(api_key=API_KEY)

    #Fetch latest data points
    cpi= fred.get_series_latest_release('CPIAUCSL')[-1]
    gdp= fred.get_series_latest_release('GDP')[-1]
    unemployment = fred.get_series_latest_release('UNRATE')[-1]

    #Get current timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    #Write data into a log file

    with open("real_data.log", "a") as f:
        f.write(f"{now} DATA CPI={cpi:.2f}\n")
        f.write(f"{now} DATA GDP={gdp:.2f}\n")
        f.write(f"{now} DATA Unemployment={unemployment:.2f}\n")

    print("Real economic data saved to real_data.log")

if __name__ == "__main__":
    fetch_and_log()

    