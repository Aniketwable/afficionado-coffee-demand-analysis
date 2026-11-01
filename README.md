# ☕ Afficionado Coffee Roasters — Demand Analysis Dashboard

## Project Overview
This project analyzes coffee shop transaction data to understand observed hourly demand, compare store performance, and identify peak-demand periods. An interactive Streamlit dashboard allows users to explore transaction, quantity, and revenue metrics.

## Objectives
- Analyze coffee shop transaction data.
- Identify observed peak-demand hours.
- Compare performance across store locations.
- Visualize hourly transaction patterns.
- Build an interactive dashboard for demand analysis.
- Document the requirements for reliable future-demand forecasting.

## Tools & Technologies
- Python
- Pandas
- Streamlit
- Plotly
- Jupyter Notebook
- Git and GitHub

## Dashboard Features
- KPI cards for total transactions, quantity sold, and revenue.
- Store-location filter.
- Hourly demand analysis.
- Store revenue comparison.
- Peak-demand summary.
- Busiest and quietest recorded-hour comparison.
- Interactive visualizations.

## Key Findings
- Total transactions: 149,116.
- Total quantity sold: 214,470.
- Total revenue: $698,812.33.
- 10:00 AM was the peak observed transaction hour for all three stores in the available hourly analysis.

These findings describe the available dataset and should not be interpreted as guaranteed future demand.

## Project Structure
```text
AfficionadoProject/
├── app.py
├── afficionado_cleaned_transactions.csv
├── afficionado_hourly_demand_profile.csv
├── afficionado_top_demand_hours.csv
├── afficionado_descriptive_baseline.csv
├── afficionado_missing_hour_notes.csv
├── PROJECT_METHODOLOGY.md
├── PROJECT_LIMITATIONS.md
└── README.md
```

## How to Run the Dashboard

1. Install Python.
2. Open Command Prompt in the project folder.
3. Install the required packages:

   ```bash
   python -m pip install streamlit pandas plotly
   ```

4. Run the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

## Important Limitation
The available dataset does not contain usable transaction dates. Therefore, daily and weekly time-series forecasting, chronological model validation, and reliable future-date predictions have not yet been completed. Missing store-hour combinations are not automatically treated as zero demand.

## Future Improvements
- Obtain reliable transaction dates and timestamps.
- Prepare chronological training and testing data.
- Compare suitable forecasting models.
- Evaluate forecast performance using MAE and RMSE.
- Estimate prediction uncertainty.
- Improve the dashboard with validated forecasts when suitable data becomes available.

## Author
Data Analytics & Machine Learning Project

## License
For educational and portfolio purposes.
