import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Company Killer - KPI Dashboard", layout="wide")
st.title("📊 Company Killer — KPI Dashboard")

@st.cache_data
def load_data():
 return pd.read_csv("data/sales.csv", parse_dates=["date"])

df = load_data()

revenue = df["revenue"].sum()
orders = df["orders"].sum()
aov = revenue / orders if orders else 0
customers = df["customers"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Orders", f"{orders:,.0f}")
c3.metric("Avg Order Value", f"${aov:,.2f}")
c4.metric("Customers", f"{customers:,.0f}")

st.divider()

daily = df.groupby("date", as_index=False)[["revenue", "orders", "customers"]].sum()
st.plotly_chart(px.line(daily, x="date", y="revenue", title="Revenue Over Time"), use_container_width=True)
st.plotly_chart(px.bar(daily, x="date", y="orders", title="Orders Over Time"), use_container_width=True)

by_cat = df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
st.plotly_chart(px.pie(by_cat, names="category", values="revenue", title="Revenue by Category"), use_container_width=True)

st.dataframe(df.tail(20), use_container_width=True)
