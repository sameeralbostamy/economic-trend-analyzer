import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt



def read_log_file(filename):
    with open(filename, 'r') as f:
        return f.readlines() #Opens a file and returns all lines as a python list of strings
    
def count_data_lines(lines): #Iterates through ines and counts how many contai DATA
    count = 0
    for line in lines:
        if " DATA " in line:
            count +=1
    return count 

def extract_cpi(lines):
    cpi_values = []
    for line in lines:
        # normalize spacing to avoid issues like "CPI = 324.37"
        clean_line = line.replace(" ", "")
        if "CPI=" in clean_line:
            raw_value = clean_line.split("CPI=")[1].strip()
            try:
                number = float(raw_value)
                cpi_values.append(number)
            except ValueError:
                continue
    return cpi_values


def extract_gdp(lines):
    gdp_values = []
    for line in lines:
        # normalize spacing to avoid issues like "CPI = 324.37"
        clean_line = line.replace(" ", "")
        if "GDP=" in clean_line:
            raw_value = clean_line.split("GDP=")[1].strip()
            try:
                number = float(raw_value)
                gdp_values.append(number)
            except ValueError:
                continue
    return gdp_values


def extract_unemployment(lines):
    unemployment_values = []
    for line in lines:
        # normalize spacing to avoid issues like "CPI = 324.37"
        clean_line = line.replace(" ", "")
        if "Unemployment=" in clean_line:
            raw_value = clean_line.split("Unemployment=")[1].strip()
            try:
                number = float(raw_value)
                unemployment_values.append(number)
            except ValueError:
                continue
    return  unemployment_values

def last_delta(values):
    """Return the change between the last two values, or None if not enough data."""
    if len(values) < 2:
        return None
    return values[-1] - values[-2]

def save_report(content):
    """Save analysis results to a text file with timestamp."""
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{now}.txt"

    with open(filename, "w") as file:
        file.write(content)

    print(f"📝 Report saved to {filename}")


def analyze_trend(values, name):
    """
    Fits a simple linear model y=mx+b to the last N values.
    Prints slope and predicted next value
    """
    if len(values)<3:
        print(f"Not enough {name} data to analyze trend")
        return
     # use the indices 0..n-1 as x-values
    x = np.arange(len(values))
    y = np.array(values)

    # fit line: returns slope m and intercept b
    m, b = np.polyfit(x, y, 1)

    if abs(m) < 1e-4:
        trend = "stable →"
    elif m > 0:
        trend = "rising 📈"
    else:
        trend = "falling 📉"

    next_value = m * len(values) + b
    
    percent_change = ((next_value - values[-1]) / values[-1]) * 100
    print(f"Predicted change: {percent_change:.2f}%")


    print(f"{name} slope: {m:.4f}")
    print(f"Predicted next {name}: {next_value:.2f}")
    print(f"Predicted change: {percent_change:.2f}%")
    print(f"{name} trend: {trend}\n")

import io
import sys

def plot_trends(cpi_values, gdp_values, unemployment_values):
    """Plot normalized economic trends over time."""
    if not (cpi_values and gdp_values and unemployment_values):
        print("⚠️ Not enough data to plot trends.")
        return

    plt.figure(figsize=(8, 5))

    # normalize all values relative to their first data point
    cpi_norm = [v / cpi_values[0] * 100 for v in cpi_values]
    gdp_norm = [v / gdp_values[0] * 100 for v in gdp_values]
    unemp_norm = [v / unemployment_values[0] * 100 for v in unemployment_values]

    plt.plot(cpi_norm, label="CPI (Inflation)")
    plt.plot(gdp_norm, label="GDP")
    plt.plot(unemp_norm, label="Unemployment")

    plt.title("Economic Indicators Over Time (Indexed to 100)")
    plt.xlabel("Data Point Index (Time Order)")
    plt.ylabel("Index (Base = 100)")
    plt.legend()
    plt.grid(True)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"trend_plot_{now}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📈 Chart saved as {filename}")



if __name__ == "__main__":
    # capture all printed output
    buffer = io.StringIO()
    sys.stdout = buffer  # redirect print() to buffer instead of terminal

    # --- existing code ---
    lines = read_log_file("real_data.log")
    print("First 5 lines:")
    for l in lines[:5]:
        print(l.strip())

    cpi_values = extract_cpi(lines)
    gdp_values = extract_gdp(lines)
    unemployment_values = extract_unemployment(lines)

    print("CPI values:", cpi_values)
    print("GDP values:", gdp_values)
    print("Unemployment values:", unemployment_values)

    print("\n=== Economic Summary ===")
    if cpi_values:
        avg_cpi = sum(cpi_values) / len(cpi_values)
        print(f"Average CPI: {avg_cpi:.2f}")

    if gdp_values:
        avg_gdp = sum(gdp_values) / len(gdp_values)
        print(f"Average GDP: {avg_gdp:.2f}")
    
    if unemployment_values:
        latest = unemployment_values[-1]
        print(f"Latest Unemployment: {latest:.2f}")
        change = last_delta(unemployment_values)
        if change is not None:
            arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"Change since last: {change:.2f} ({arrow})")
        if latest > 5.0:
            print("⚠️  Warning: unemployment above 5%!")
        else:
            print("✅  Unemployment stable.")
    
    if cpi_values and len(cpi_values) >= 2:
        cpi_change = last_delta(cpi_values)
        if cpi_change is not None:
            arrow = "↑" if cpi_change > 0 else "↓" if cpi_change < 0 else "→"
            print(f"CPI change since last: {cpi_change:.2f} ({arrow})")
            if cpi_change > 0:
                print("📈 Inflation rising (CPI increased)")
            elif cpi_change < 0:
                print("📉 Inflation easing (CPI decreased)")
            else:
                print("→ Inflation stable.")
    
    if gdp_values and len(gdp_values) >= 2:
        gdp_change = last_delta(gdp_values)
        if gdp_change is not None:
            arrow = "↑" if gdp_change > 0 else "↓" if gdp_change < 0 else "→"
            print(f"GDP change since last: {gdp_change:.2f} ({arrow})")
            if gdp_change > 0:
                print("📈 Economic growth accelerating")
            elif gdp_change < 0:
                print("📉 Economic growth slowing")
            else:
                print("→ GDP stable.")

    print("\n=== Trend Analysis ===")
    analyze_trend(cpi_values, "CPI")
    analyze_trend(gdp_values, "GDP")
    analyze_trend(unemployment_values, "Unemployment")

    # --- end of your normal prints ---
    # restore stdout and save report
    sys.stdout = sys.__stdout__  # go back to normal printing
    report_text = buffer.getvalue()
    save_report(report_text)
    print("✅ Report written successfully.")

    analyze_trend(cpi_values, "CPI")
    analyze_trend(gdp_values, "GDP")
    analyze_trend(unemployment_values, "Unemployment")
    plot_trends(cpi_values, gdp_values, unemployment_values)







