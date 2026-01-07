import streamlit as st
import pandas as pd
import mysql.connector

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("OLA Ride Analytics Streamlit App🚘")
st.write(
    "This application displays ride analytics using data fetched from a MySQL database "
    "with dropdown-based filters placed directly on the dashboard."
)

# ---------------- MYSQL CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="powerbi",
    password="PowerBI@123",
    database="rides_data"
)

df = pd.read_sql("SELECT * FROM rides", conn)

# ---------------- FILTER SECTION (TOP OF PAGE) ----------------
st.subheader("Filters")

f1, f2, f3, f4 = st.columns(4)

with f1:
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["All"] + sorted(df["Vehicle_Type"].dropna().unique().tolist())
    )

with f2:
    pickup_location = st.selectbox(
        "Pickup Location",
        ["All"] + sorted(df["Pickup_Location"].dropna().unique().tolist())
    )

with f3:
    booking_status = st.selectbox(
        "Booking Status",
        ["All"] + sorted(df["Booking_Status"].dropna().unique().tolist())
    )

with f4:
    search_booking = st.text_input("Search Booking ID")

# ---------------- APPLY FILTERS ----------------
filtered_df = df.copy()

if vehicle_type != "All":
    filtered_df = filtered_df[filtered_df["Vehicle_Type"] == vehicle_type]

if pickup_location != "All":
    filtered_df = filtered_df[filtered_df["Pickup_Location"] == pickup_location]

if booking_status != "All":
    filtered_df = filtered_df[filtered_df["Booking_Status"] == booking_status]

if search_booking:
    filtered_df = filtered_df[
        filtered_df["Booking_ID"].astype(str).str.contains(search_booking)
    ]

# ---------------- KPI SECTION ----------------
st.subheader("Key Ride Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Rides", len(filtered_df))
c2.metric(
    "Completed Rides",
    len(filtered_df[filtered_df["Booking_Status"] == "Success"])
)
c3.metric(
    "Cancelled Rides",
    len(filtered_df[filtered_df["Booking_Status"].str.contains("Cancel")])
)
c4.metric(
    "Total Revenue",
    f"₹ {filtered_df['Booking_Value'].sum():,.2f}"
)

# ---------------- DATA TABLE ----------------
st.subheader("Filtered Ride Data")
st.dataframe(filtered_df, use_container_width=True)
