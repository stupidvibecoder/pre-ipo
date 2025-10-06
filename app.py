# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Private Market Tracker", page_icon="💼", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("companies.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# --- Sidebar ---
st.sidebar.title("Private Company Tracker")
companies = df["company"].unique()
selected_company = st.sidebar.selectbox("Select a company:", companies)

# --- Main View ---
st.title("💼 Private Market Tracker")
st.markdown("Visualizing valuation and capital raised for the 10 biggest private companies.")

company_df = df[df["company"] == selected_company]

col1, col2 = st.columns([2, 1])

# --- Plot ---
with col1:
    fig = px.line(
        company_df,
        x="date",
        y="valuation ($B)",
        markers=True,
        title=f"{selected_company} Valuation Over Time",
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Valuation ($B)")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        company_df,
        x="date",
        y="capital_raised ($B)",
        title=f"{selected_company} Capital Raised Per Round",
    )
    fig2.update_layout(xaxis_title="Date", yaxis_title="Capital Raised ($B)")
    st.plotly_chart(fig2, use_container_width=True)

# --- Personal Take ---
with col2:
    st.subheader("📝 Your Take")
    take = st.text_area(f"Your view on {selected_company}:", height=200)
    if st.button("Save Note"):
        st.success("Note saved (local only for now).")
        st.session_state[selected_company] = take

if selected_company in st.session_state:
    st.info(f"Your previous take: {st.session_state[selected_company]}")
