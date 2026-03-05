import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Analyst", page_icon="📊", layout="wide")
st.title("📊 Data Analyst")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is None:
 st.info("Upload a CSV file to start.")
else:
 df = pd.read_csv(file)
 st.subheader("Preview")
 st.dataframe(df, use_container_width=True)
 st.subheader("Summary")
 st.dataframe(df.describe(include="all").fillna(""), use_container_width=True)
 num = df.select_dtypes(include="number")
 st.subheader("Numeric Chart")
 st.line_chart(num)
