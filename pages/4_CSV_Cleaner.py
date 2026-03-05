import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Cleaner", page_icon="🧹", layout="wide")
st.title("🧹 CSV Cleaner → date, category, revenue, orders, customers")

f = st.file_uploader("Upload CSV", type=["csv"])
df = pd.read_csv(f) if f is not None else pd.DataFrame()
_ = st.info("Upload a CSV file to start.") if f is None else st.write("")

cols = ["-- none --"] + list(df.columns) if len(df.columns) > 0 else ["-- none --"]

date_col = st.selectbox("Map to date", cols)
category_col = st.selectbox("Map to category", cols)
revenue_col = st.selectbox("Map to revenue", cols)
orders_col = st.selectbox("Map to orders", cols)
customers_col = st.selectbox("Map to customers", cols)

out = pd.DataFrame()
out["date"] = pd.to_datetime(df[date_col], errors="coerce").dt.date if date_col != "-- none --" else pd.Series([pd.NA] * len(df))
out["category"] = df[category_col].astype("string").fillna("") if category_col != "-- none --" else pd.Series([""] * len(df))
out["revenue"] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0.0) if revenue_col != "-- none --" else pd.Series([0.0] * len(df))
out["orders"] = pd.to_numeric(df[orders_col], errors="coerce").fillna(0).astype(int) if orders_col != "-- none --" else pd.Series([0] * len(df))
out["customers"] = pd.to_numeric(df[customers_col], errors="coerce").fillna(0).astype(int) if customers_col != "-- none --" else pd.Series([0] * len(df))

st.subheader("Standardized Output")
st.dataframe(out, use_container_width=True)

csv_out = out.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download standardized.csv", data=csv_out, file_name="standardized.csv", mime="text/csv")
