from pathlib import Path
import pandas as pd
from flask import Flask, jsonify, render_template

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "household_energy_consumption(1).csv"
if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR / "household_energy_consumption.csv"

app = Flask(__name__, template_folder=".")

def load_dataset():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. Put the CSV next to app.py."
        )
    frame = pd.read_csv(DATA_PATH)
    required = {
        "Household_ID", "Date", "Energy_Consumption_kWh", "Household_Size",
        "Avg_Temperature_C", "Has_AC", "Peak_Hours_Usage_kWh"
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    for col in ["Energy_Consumption_kWh", "Household_Size",
                "Avg_Temperature_C", "Peak_Hours_Usage_kWh"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame["Has_AC"] = frame["Has_AC"].astype("string").str.strip().str.title()
    return frame

@app.get("/")
def dashboard():
    return render_template("dashboard.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "dataset": DATA_PATH.name})

@app.get("/api/data")
def data():
    frame = load_dataset()
    frame["Date"] = frame["Date"].dt.strftime("%Y-%m-%d")
    # Convert missing values to JSON nulls after casting to object; this keeps
    # the response valid JSON for browser clients.
    frame = frame.astype(object).where(pd.notna(frame), None)
    return jsonify({"rows": frame.to_dict(orient="records"), "count": len(frame)})

@app.get("/api/summary")
def summary():
    frame = load_dataset()
    energy = frame["Energy_Consumption_kWh"]
    peak = frame["Peak_Hours_Usage_kWh"]
    return jsonify({
        "records": int(len(frame)),
        "households": int(frame["Household_ID"].nunique()),
        "total_consumption_kwh": round(float(energy.sum()), 2),
        "average_consumption_kwh": round(float(energy.mean()), 3),
        "average_peak_usage_pct": round(float((peak[energy > 0] / energy[energy > 0]).mean() * 100), 2)
    })

if __name__ == "__main__":
    # Local development server. Do not use debug mode in production.
    app.run(host="127.0.0.1", port=5000, debug=True)
