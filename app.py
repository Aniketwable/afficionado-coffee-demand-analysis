
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

DATA_FILE = Path(__file__).parent / "afficionado_hourly_demand_profile.csv"


@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    required = [
        "store_location",
        "hour",
        "transactions",
        "quantity_sold",
        "revenue"
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in ["hour", "transactions", "quantity_sold", "revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=required).copy()
    df["hour"] = df["hour"].astype(int)

    return df


if not DATA_FILE.exists():
    st.error("Aggregated CSV not found. Check that it is uploaded beside app.py.")
    st.stop()

try:
    hourly_df = load_data(str(DATA_FILE))
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

# Sidebar filters
st.sidebar.header("Dashboard Filters")

stores = sorted(hourly_df["store_location"].unique())
selected_store = st.sidebar.selectbox(
    "Select Store",
    ["All Stores"] + stores
)

metric_choice = st.sidebar.radio(
    "Demand Metric",
    ["Transactions", "Quantity Sold", "Revenue"]
)

if selected_store == "All Stores":
    filtered = hourly_df.copy()
else:
    filtered = hourly_df[
        hourly_df["store_location"] == selected_store
    ].copy()

# KPI cards: totals calculated from the hourly aggregates
c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Transactions",
    f"{filtered['transactions'].sum():,.0f}"
)
c2.metric(
    "Total Quantity Sold",
    f"{filtered['quantity_sold'].sum():,.0f}"
)
c3.metric(
    "Total Revenue",
    f"${filtered['revenue'].sum():,.2f}"
)

st.caption(
    "KPIs are sums of the available store-hour aggregates. "
    "Missing store-hour observations are not assumed to be zero."
)

st.divider()

# Hourly demand profile
st.subheader("Hourly Demand Profile")

metric_columns = {
    "Transactions": ("transactions", "Transactions"),
    "Quantity Sold": ("quantity_sold", "Quantity Sold"),
    "Revenue": ("revenue", "Revenue ($)")
}

column, chart_label = metric_columns[metric_choice]

hourly = (
    filtered.groupby("hour")[column]
    .sum()
    .sort_index()
)

st.bar_chart(hourly.rename(chart_label))

st.caption(
    "This chart describes observed hourly demand; it is not a forecast."
)

# Store comparison
st.subheader("Store Performance Comparison")

store_summary = (
    hourly_df.groupby("store_location")
    .agg(
        total_transactions=("transactions", "sum"),
        total_quantity=("quantity_sold", "sum"),
        total_revenue=("revenue", "sum")
    )
    .sort_values("total_revenue", ascending=False)
)

st.dataframe(store_summary.round(2), use_container_width=True)

# Product category analysis is unavailable in this aggregated file
st.info(
    "Product-category analysis is not displayed because the uploaded "
    "hourly aggregate does not contain product-category data."
)

# Peak hour for the selected store or all stores
peak_hour_data = (
    filtered.groupby("hour")["transactions"]
    .sum()
    .sort_index()
)

if not peak_hour_data.empty:
    peak_hour = int(peak_hour_data.idxmax())
    peak_transactions = int(peak_hour_data.loc[peak_hour])

    st.subheader("Peak Observed Demand")
    p1, p2 = st.columns(2)
    p1.metric("Peak Hour", f"{peak_hour:02d}:00")
    p2.metric("Transactions at Peak Hour", f"{peak_transactions:,.0f}")

# Hourly demand by store
st.subheader("Hourly Demand Distribution by Store")

hourly_chart = hourly_df.pivot(
    index="hour",
    columns="store_location",
    values="transactions"
).sort_index()

st.line_chart(hourly_chart)

st.caption(
    "Gaps represent missing store-hour observations, not confirmed zero demand."
)

# Peak demand summary
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

# Store revenue comparison
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

# Busiest and quietest observed hours
st.subheader("Busiest vs Quietest Observed Hours")

for store in sorted(hourly_df["store_location"].unique()):
    store_data = hourly_df[
        hourly_df["store_location"] == store
    ].sort_values("hour")

    if store_data.empty:
        continue

    busiest = store_data.loc[store_data["transactions"].idxmax()]
    quietest = store_data.loc[store_data["transactions"].idxmin()]

    st.write(f"**{store}**")

    c1, c2 = st.columns(2)

    c1.metric(
        "Busiest observed hour",
        f"{int(busiest['hour']):02d}:00",
        f"{busiest['transactions']:,.0f} transactions"
    )

    c2.metric(
        "Quietest recorded hour",
        f"{int(quietest['hour']):02d}:00",
        f"{quietest['transactions']:,.0f} transactions"
    )

st.info(
    "Data limitation: Actual transaction dates are unavailable. "
    "This dashboard summarizes observed hourly demand and store performance. "
    "It cannot reliably reconstruct daily or weekly trends or validate "
    "forecasts for future dates."
)

