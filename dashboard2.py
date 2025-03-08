import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

df = pd.read_csv("all_df.csv")
df["dteday_x"] = pd.to_datetime(df["dteday_x"])

def daily_rentals(df):
    daily_rentals = df.resample(rule='D', on='dteday_x').agg({"cnt_x": "sum"}).reset_index()
    daily_rentals.rename(columns={"cnt_x": "rental_count"}, inplace=True)
    return daily_rentals

def rfm_analysis(df):
    rfm = df.groupby("instant").agg({
        "dteday_x": "max", 
        "cnt_x": "sum"  
    }).rename(columns={"dteday_x": "max_order_timestamp", "cnt_x": "monetary"})
    rfm.drop(columns=["max_order_timestamp"], inplace=True)
    rfm["frequency"] = df.groupby("instant")["dteday_x"].count()
    return rfm

min_date = df["dteday_x"].min()
max_date = df["dteday_x"].max()
with st.sidebar:
    start_date, end_date = st.date_input("Time Range", min_value=min_date, max_value=max_date, value=[min_date, max_date])
main_df = df[(df["dteday_x"] >= str(start_date)) & (df["dteday_x"] <= str(end_date))]
daily_rentals_df = daily_rentals(main_df)
rfm = rfm_analysis(main_df)
st.header("Bike Rentals Dashboard 🚲")
st.subheader("Daily Rentals")
col1, col2 = st.columns(2)
with col1:
    total_rentals = daily_rentals_df.rental_count.sum()
    st.metric("Total Rentals", value=total_rentals)
with col2:
    total_revenue = format_currency(rfm.monetary.sum(), "IDR", locale='id_ID')
    st.metric("Total Revenue", value=total_revenue)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rentals_df["dteday_x"], daily_rentals_df["rental_count"], marker='o', linewidth=2, color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)
