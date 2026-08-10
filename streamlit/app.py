import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Retail Business Intelligence",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "data/cleaned/cleaned_superstore.csv"
    )


df = load_data()


# -----------------------------
# Title
# -----------------------------
st.title("📊 Retail Business Intelligence Platform")
st.markdown(
    "Interactive retail sales analysis using Python and Streamlit."
)


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

# State filter
if "State" in df.columns:
    states = sorted(df["State"].dropna().unique())

    selected_states = st.sidebar.multiselect(
        "Select State",
        states,
        default=states
    )

    filtered_df = df[df["State"].isin(selected_states)]
else:
    filtered_df = df.copy()


# Category filter
if "Category" in df.columns:
    categories = sorted(df["Category"].dropna().unique())

    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )

    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]


# -----------------------------
# KPI Calculations
# -----------------------------
total_sales = (
    filtered_df["Sales"].sum()
    if "Sales" in filtered_df.columns
    else 0
)

total_profit = (
    filtered_df["Profit"].sum()
    if "Profit" in filtered_df.columns
    else 0
)

total_orders = (
    filtered_df["Order ID"].nunique()
    if "Order ID" in filtered_df.columns
    else len(filtered_df)
)

total_customers = (
    filtered_df["Customer ID"].nunique()
    if "Customer ID" in filtered_df.columns
    else 0
)


# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Customers",
    f"{total_customers:,}"
)


st.divider()


# -----------------------------
# Sales by Category
# -----------------------------
if "Category" in filtered_df.columns and "Sales" in filtered_df.columns:

    st.subheader("📈 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)


# -----------------------------
# Profit by Category
# -----------------------------
if "Category" in filtered_df.columns and "Profit" in filtered_df.columns:

    st.subheader("💰 Profit by Category")

    category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_profit)


# -----------------------------
# Top 10 States by Sales
# -----------------------------
if "State" in filtered_df.columns and "Sales" in filtered_df.columns:

    st.subheader("🏆 Top 10 States by Sales")

    top_states = (
        filtered_df
        .groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_states)


# -----------------------------
# Sales Trend
# -----------------------------
if "Order Date" in filtered_df.columns and "Sales" in filtered_df.columns:

    st.subheader("📅 Sales Trend")

    trend_df = filtered_df.copy()

    trend_df["Order Date"] = pd.to_datetime(
        trend_df["Order Date"],
        errors="coerce"
    )

    trend_df = (
        trend_df
        .dropna(subset=["Order Date"])
        .set_index("Order Date")
        .resample("ME")["Sales"]
        .sum()
    )

    st.line_chart(trend_df)


# -----------------------------
# Raw Data
# -----------------------------
with st.expander("📋 View Filtered Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


st.success("Dashboard loaded successfully!")