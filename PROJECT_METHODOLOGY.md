# Afficionado Coffee Roasters
## Project Methodology

### 1. Project Objective
The objective of this project is to analyze coffee shop transaction data, understand store-level and hourly demand patterns, identify observed peak-demand hours, and develop an interactive dashboard to support demand planning.

### 2. Data Preparation
The transaction dataset was inspected and cleaned before analysis. Data types, missing values, duplicate transaction identifiers, and revenue calculations were checked. A cleaned dataset was saved for further analysis.

### 3. Exploratory Data Analysis (EDA)
The analysis examined:
- Total transactions
- Total quantity sold
- Total revenue
- Store-level performance
- Hourly transaction patterns
- Peak observed demand hours
- Differences between stores

### 4. Hourly Demand Analysis
Transactions were grouped by store and hour to create an hourly demand profile. Store-level summaries were also generated to compare average observed hourly transactions, total revenue, and peak observed hours.

The analysis identified 10:00 AM as the peak observed transaction hour for each of the three stores in the available data.

### 5. Missing-Date Limitation
The available dataset does not contain usable transaction dates. Therefore, genuine daily or weekly time series could not be constructed, and future-date forecasting models could not be reliably trained or evaluated.

Missing store-hour combinations were not automatically treated as zero demand or proof that a store was closed. The findings describe observed records only.

### 6. Interactive Dashboard
A Streamlit dashboard was developed to display:
- Overall transaction, quantity, and revenue KPIs
- Store filtering
- Hourly demand patterns
- Store performance comparisons
- Peak-demand summaries
- Busiest and quietest recorded hours
- Store revenue comparisons

### 7. Next Steps
To develop and evaluate reliable demand forecasts, obtain transaction-level data containing valid dates and times. Then prepare a chronological dataset, create time-based training and testing sets, compare suitable forecasting models, evaluate forecast errors, and estimate prediction uncertainty.

### 8. Conclusion
The project establishes a descriptive foundation for understanding observed coffee shop demand. The interactive dashboard makes the available transaction patterns easier to explore. Reliable future-demand forecasting remains dependent on obtaining suitable date-enabled data.
