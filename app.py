import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Key Performance Indicator", layout="wide")

with open("auth.yaml") as f:
 config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
 config["credentials"],
 config["cookie"]["name"],
 config["cookie"]["key"],
 config["cookie"]["expiry_days"],
)

try:
 login_result = authenticator.login(location="main")
except TypeError:
 login_result = authenticator.login("Login", "main")

if isinstance(login_result, tuple):
 name, authentication_status, username = login_result
else:
 authentication_status = st.session_state.get("authentication_status")
 name = st.session_state.get("name")
 username = st.session_state.get("username")

if authentication_status is False:
 st.error("Username/password is incorrect")
 st.stop()
elif authentication_status is None:
 st.warning("Please enter your username and password")
 st.stop()

st.sidebar.success(f"Logged in as {name}")
try:
 authenticator.logout("Logout", "sidebar")
except TypeError:
 authenticator.logout(location="sidebar")

st.title("📊 Key Performance Indicator")

@st.cache_data
def load_csv(path: str):
 df = pd.read_csv(path)
 df["date"] = pd.to_datetime(df["date"])
 return df

uploaded = st.file_uploader("Upload CSV (date,category,revenue,orders,customers)", type=["csv"])
if uploaded is not None:
 df = pd.read_csv(uploaded)
 df["date"] = pd.to_datetime(df["date"])
else:
 df = load_csv("data/sales.csv")

st.sidebar.header("Filters")
min_d, max_d = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
all_categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)

if isinstance(date_range, tuple) and len(date_range) == 2:
 start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
 start_date = end_date = pd.to_datetime(date_range)

fdf = df[(df["date"] >= start_date) & (df["date"] <= end_date) & (df["category"].isin(selected_categories))].copy()
if fdf.empty:
 st.warning("No data for selected filters.")
 st.stop()

revenue = fdf["revenue"].sum()
orders = fdf["orders"].sum()
aov = revenue / orders if orders else 0
customers = fdf["customers"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${revenue:,.0f}")
c2.metric("Orders", f"{orders:,.0f}")
c3.metric("Avg Order Value", f"${aov:,.2f}")
c4.metric("Customers", f"{customers:,.0f}")

st.divider()
daily = fdf.groupby("date", as_index=False)[["revenue", "orders", "customers"]].sum()
st.plotly_chart(px.line(daily, x="date", y="revenue", title="Revenue Over Time"), width="stretch")
st.plotly_chart(px.bar(daily, x="date", y="orders", title="Orders Over Time"), width="stretch")
by_cat = fdf.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
st.plotly_chart(px.pie(by_cat, names="category", values="revenue", title="Revenue by Category"), width="stretch")
st.dataframe(fdf.sort_values("date", ascending=False), width="stretch")
