# Household Energy Intelligence

## Files
- `household_energy_eda.ipynb` — project-style EDA notebook based on the supplied sample notebook's structured, step-by-step presentation.
- `dashboard.html` — separate dashboard page with inline CSS and JavaScript (Chart.js is loaded from its CDN).
- `app.py` — Flask app and JSON endpoints.
- `household_energy_consumption(1).csv` — source dataset copy.
- `requirements.txt` — Python dependencies.

## Run the dashboard
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `python -m venv .venv`, then activate the environment.
4. Run `pip install -r requirements.txt`.
5. Run `python app.py`.
6. Open `http://127.0.0.1:5000`.

The dashboard calls `/api/data`; the app reads the CSV locally. The `/api/health` and `/api/summary` endpoints can be used for quick checks.

## Run the notebook
Open `household_energy_eda.ipynb` in Jupyter Notebook or JupyterLab. Keep the CSV in the same folder and run cells from top to bottom. The notebook exports optional summaries into `eda_outputs/`.

## Notes
- The dashboard uses date, AC status and household-size filters.
- The notebook flags potential outliers for review but does not delete them automatically.
- Temperature bands follow the supplied guide's illustrative thresholds: below 15°C, 15–20°C, and 20°C or above.
- Dashboard charts use Chart.js from a CDN, so an internet connection is needed for the chart library unless you replace it with a local copy.
