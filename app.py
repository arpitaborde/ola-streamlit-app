import streamlit as st
import pandas as pd
import mysql.connector
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("OLA Ride Analytics Streamlit App🚘")
st.write(
    "This application displays ride analytics using data fetched from a MySQL database "
    "or a CSV file, with dropdown-based filters placed directly on the dashboard."
)

# =====================================================
# FILE UPLOAD OPTION
# =====================================================
st.sidebar.header("📁 Upload Your Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

# =====================================================
# DATA SOURCE SWITCH
# =====================================================
USE_MYSQL = False   # True = local MySQL | False = CSV

if uploaded_file is not None:
    # Load uploaded file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:  # Excel file
            df = pd.read_excel(uploaded_file)
        st.sidebar.success(f"✅ File uploaded: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
elif USE_MYSQL:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="powerbi",
            password="PowerBI@123",
            database="rides_data"
        )
        df = pd.read_sql("SELECT * FROM rides", conn)
    except Exception as e:
        st.error(f"MySQL connection failed: {e}")
        st.stop()
else:
    # Make sure file exists
    csv_file = "OLAdataset.csv"
    if not os.path.exists(csv_file):
        st.error(f"CSV file '{csv_file}' not found. Upload it in the app folder or repo.")
        st.stop()
    df = pd.read_csv(csv_file)

# ---------------- FILTER SECTION ----------------
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
        filtered_df["Booking_ID"].astype(str).str.contains(search_booking, na=False)
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
    len(filtered_df[
        filtered_df["Booking_Status"]
        .fillna("")
        .str.contains("Cancel", case=False)
    ])
)

c4.metric(
    "Total Revenue",
    f"₹ {filtered_df['Booking_Value'].sum():,.2f}"
)

# ---------------- DATA TABLE ----------------
st.subheader("Filtered Ride Data")
st.dataframe(filtered_df, use_container_width=True)
