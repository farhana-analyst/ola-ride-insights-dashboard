import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="OLA Ride Insights Dashboard",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_excel("OLA_DataSet (1).xlsx")

df = load_data()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("Filters")

vehicle = st.sidebar.selectbox(
    "Vehicle Type",
    ["All"] + list(df["Vehicle_Type"].dropna().unique())
)

payment = st.sidebar.selectbox(
    "Payment Method",
    ["All"] + list(df["Payment_Method"].dropna().unique())
)

filtered_df = df.copy()

if vehicle != "All":
    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"] == vehicle
    ]

if payment != "All":
    filtered_df = filtered_df[
        filtered_df["Payment_Method"] == payment
    ]

# ---------------------------
# TITLE
# ---------------------------
st.title("🚖 OLA Ride Insights Dashboard")

# ---------------------------
# KPI CARDS
# ---------------------------
total_rides = len(filtered_df)

total_revenue = filtered_df["Booking_Value"].sum()

avg_driver_rating = filtered_df["Driver_Ratings"].mean()

avg_customer_rating = filtered_df["Customer_Rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rides", f"{total_rides:,}")
col2.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col3.metric("Avg Driver Rating", f"{avg_driver_rating:.2f}")
col4.metric("Avg Customer Rating", f"{avg_customer_rating:.2f}")

st.divider()

# ---------------------------
# DATA PREVIEW
# ---------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))

# ---------------------------
# RIDE VOLUME OVER TIME
# ---------------------------
st.subheader("Ride Volume Over Time")

ride_volume = (
    filtered_df.groupby("Date")
    .size()
)

st.line_chart(ride_volume)

# ---------------------------
# BOOKING STATUS BREAKDOWN
# ---------------------------
st.subheader("Booking Status Breakdown")

booking_status = (
    filtered_df["Booking_Status"]
    .value_counts()
)

st.bar_chart(booking_status)

# ---------------------------
# TOP VEHICLE TYPES
# ---------------------------
st.subheader("Top Vehicle Types by Ride Distance")

vehicle_distance = (
    filtered_df.groupby("Vehicle_Type")["Ride_Distance"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(vehicle_distance)

# ---------------------------
# REVENUE BY PAYMENT METHOD
# ---------------------------
st.subheader("Revenue by Payment Method")

revenue = (
    filtered_df.groupby("Payment_Method")["Booking_Value"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(revenue)

# ---------------------------
# TOP 5 CUSTOMERS
# ---------------------------
st.subheader("Top 5 Customers by Booking Value")

top_customers = (
    filtered_df.groupby("Customer_ID")["Booking_Value"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_customers)

# ---------------------------
# CUSTOMER CANCELLATION REASONS
# ---------------------------
if "Canceled_Rides_by_Customer" in filtered_df.columns:

    st.subheader("Customer Cancellation Reasons")

    customer_cancel = (
        filtered_df["Canceled_Rides_by_Customer"]
        .value_counts()
    )

    st.bar_chart(customer_cancel)

# ---------------------------
# DRIVER CANCELLATION REASONS
# ---------------------------
if "Canceled_Rides_by_Driver" in filtered_df.columns:

    st.subheader("Driver Cancellation Reasons")

    driver_cancel = (
        filtered_df["Canceled_Rides_by_Driver"]
        .value_counts()
    )

    st.bar_chart(driver_cancel)

# ---------------------------
# DRIVER RATINGS
# ---------------------------
st.subheader("Driver Ratings Distribution")

driver_rating = (
    filtered_df["Driver_Ratings"]
    .value_counts()
    .sort_index()
)

st.bar_chart(driver_rating)

# ---------------------------
# CUSTOMER RATINGS
# ---------------------------
st.subheader("Customer Ratings Distribution")

customer_rating = (
    filtered_df["Customer_Rating"]
    .value_counts()
    .sort_index()
)

st.bar_chart(customer_rating)

# ---------------------------
# RIDE DISTANCE
# ---------------------------
st.subheader("Ride Distance Distribution")

ride_distance = (
    filtered_df.groupby("Date")["Ride_Distance"]
    .sum()
)

st.line_chart(ride_distance)

# ---------------------------
# DOWNLOAD DATA
# ---------------------------
st.subheader("Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="ola_filtered_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.markdown(
    "### OLA Ride Analytics Dashboard | Streamlit + Python"
)