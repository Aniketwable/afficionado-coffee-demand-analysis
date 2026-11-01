# Project Limitations
## Afficionado Coffee Roasters

### 1. Missing Transaction Dates
The available dataset does not contain usable transaction dates. Consequently, daily, weekly, and seasonal demand trends cannot be established reliably.

### 2. Forecasting Constraints
Reliable future-demand forecasting requires chronological observations. Without transaction dates, a time-based training and testing process cannot be performed correctly, and future forecasting accuracy cannot be validated.

### 3. Missing Store-Hour Combinations
Some store-hour combinations have no recorded transactions. These combinations are treated as missing observations rather than automatically being assigned zero demand or classified as store closures.

### 4. Observed Peak Hours
The analysis identifies peak hours from the records available in the dataset. These findings should not be interpreted as guaranteed daily demand patterns or forecasts of future demand.

### 5. Future Improvements
To improve the project:
- Obtain transaction dates and timestamps.
- Confirm store operating hours and closure periods.
- Build chronological training and testing datasets.
- Compare suitable forecasting models.
- Evaluate forecasts using MAE, RMSE, and other appropriate metrics.
- Quantify forecast uncertainty where sufficient data is available.

### Conclusion
The current project provides descriptive demand analysis and an interactive dashboard. Reliable future-demand prediction remains a future enhancement that depends on obtaining suitable time-stamped transaction data.
