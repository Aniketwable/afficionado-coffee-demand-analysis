
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Afficionado Coffee Roasters",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Afficionado Coffee Roasters")
st.subheader("Hourly Demand Profile & Sales Analytics")

DATA_FILE = Path(__file__).parent / "afficionado_cleaned_transactions.csv"

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    required = [
        "transaction_id", "transaction_qty", "unit_price",
        "revenue", "hour", "store_location", "product_category"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in ["transaction_qty", "unit_price", "revenue", "hour"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=["transaction_qty", "revenue", "hour", "store_location"]
    )

    df["hour"] = df["hour"].astype(int)
    return df

if not DATA_FILE.exists():
    st.error("CSV file not found. Place the cleaned CSV beside app.py.")
    st.stop()

try:
    df = load_data(str(DATA_FILE))
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

stores = sorted(df["store_location"].dropna().unique())
selected_store = st.sidebar.selectbox("Select Store", ["All Stores"] + stores)

metric_choice = st.sidebar.radio(
    "Demand Metric",
    ["Transactions", "Quantity Sold", "Revenue"]
)

if selected_store == "All Stores":
    filtered = df.copy()
else:
    filtered = df[df["store_location"] == selected_store].copy()

# KPI cards
total_transactions = filtered["transaction_id"].nunique()
total_quantity = filtered["transaction_qty"].sum()
total_revenue = filtered["revenue"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Transactions", f"{total_transactions:,.0f}")
c2.metric("Total Quantity Sold", f"{total_quantity:,.0f}")
c3.metric("Total Revenue", f"${total_revenue:,.2f}")

st.divider()

# Hourly demand profile
st.subheader("Hourly Demand Profile")

metric_columns = {
    "Transactions": ("transaction_id", "Transactions"),
    "Quantity Sold": ("transaction_qty", "Quantity Sold"),
    "Revenue": ("revenue", "Revenue ($)")
}

column, chart_label = metric_columns[metric_choice]

hourly = (
    filtered.groupby("hour")
    .agg(
        total_transactions=("transaction_id", "nunique"),
        total_quantity=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum")
    )
    .reindex(range(24), fill_value=0)
)

if column == "transaction_id":
    chart_data = hourly[["total_transactions"]].rename(
        columns={"total_transactions": chart_label}
    )
elif column == "transaction_qty":
    chart_data = hourly[["total_quantity"]].rename(
        columns={"total_quantity": chart_label}
    )
else:
    chart_data = hourly[["total_revenue"]].rename(
        columns={"total_revenue": chart_label}
    )

st.bar_chart(chart_data)
st.caption(
    "These are aggregated observations from the available dataset, "
    "not forecasts for specific future dates."
)

# Store comparison
st.subheader("Store Performance Comparison")

store_summary = (
    df.groupby("store_location")
    .agg(
        total_transactions=("transaction_id", "nunique"),
        total_quantity=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)

st.dataframe(store_summary.round(2), use_container_width=True)

# Category analysis
st.subheader("Product Category Performance")

category_summary = (
    filtered.groupby("product_category")
    .agg(
        total_quantity=("transaction_qty", "sum"),
        total_revenue=("revenue", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)

st.bar_chart(category_summary[["total_revenue"]])
st.dataframe(category_summary.round(2), use_container_width=True)

# Peak hour
peak_hour = int(hourly["total_transactions"].idxmax())
peak_transactions = int(hourly.loc[peak_hour, "total_transactions"])

st.subheader("Peak Observed Demand")
p1, p2 = st.columns(2)
p1.metric("Peak Hour", f"{peak_hour:02d}:00")
p2.metric("Transactions at Peak Hour", f"{peak_transactions:,}")

st.info(
    "Data limitation: Actual transaction dates are unavailable. "
    "This dashboard describes observed hourly demand and store performance. "
    "It cannot reliably reconstruct daily or weekly trends, or validate "
    "forecasts for future dates."
)

st.subheader("Hourly Demand Distribution by Store")

hourly_df = pd.read_csv("afficionado_hourly_demand_profile.csv")

hourly_chart = hourly_df.pivot(
    index="hour",
    columns="store_location",
    values="transactions"
)

st.line_chart(hourly_chart)

st.caption(
    "Hourly transactions by store. Missing store-hour "
    "observations are not filled with zero."
)

st.subheader("Peak Demand Summary")

peak_summary = (
    hourly_df.loc[
        hourly_df.groupby("store_location")["transactions"].idxmax(),
        ["store_location", "hour", "transactions"]
    ]
    .rename(columns={
        "store_location": "Store",
        "hour": "Peak Hour (24-hour)",
        "transactions": "Peak Transactions"
    })
    .sort_values("Store")
    .reset_index(drop=True)
)

st.dataframe(peak_summary, hide_index=True, use_container_width=True)

st.subheader("Store Revenue Comparison")

store_revenue = (
    hourly_df.groupby("store_location")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

cols = st.columns(len(store_revenue))

for col, (store, revenue) in zip(cols, store_revenue.items()):
    col.metric(
        label=f"{store} Revenue",
        value=f"${revenue:,.2f}"
    )

st.subheader("Busiest vs Quietest Observed Hours")

hour_comparison = (
    hourly_df.groupby(["store_location", "hour"])["transactions"]
    .sum()
    .reset_index()
)

for store in sorted(hour_comparison["store_location"].unique()):
    store_data = hour_comparison[
        hour_comparison["store_location"] == store
    ]

    busiest = store_data.loc[store_data["transactions"].idxmax()]
    quietest = store_data.loc[store_data["transactions"].idxmin()]

    st.write(f"**{store}**")

    c1, c2 = st.columns(2)

    c1.metric(
        "Busiest observed hour",
        f"{int(busiest['hour']):02d}:00",
        f"{int(busiest['transactions']):,} transactions"
    )

    c2.metric(
        "Quietest recorded hour",
        f"{int(quietest['hour']):02d}:00",
        f"{int(quietest['transactions']):,} transactions"
    )
