import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Private Market Tracker", layout="wide")

st.title("📈 Private Market Tracker")
st.write("Visualizing valuation and funding data for leading private companies in AI and technology.")

# ---------------------------
# Data setup
# ---------------------------
data = [
    # SpaceX
    ["SpaceX", "2002-12-18", 0.005, 0.001, "Seed"],
    ["SpaceX", "2005-03-09", 0.05, 0.05, "Series B"],
    ["SpaceX", "2008-08-01", 0.5, 0.02, "Series D"],
    ["SpaceX", "2010-10-28", 1.0, 0.05, "Series E"],
    ["SpaceX", "2015-01-20", 12.0, 1.0, "Series F"],
    ["SpaceX", "2017-11-27", 21.0, 0.45, "Series H"],
    ["SpaceX", "2018-04-01", 24.0, 0.21, "Series I"],
    ["SpaceX", "2019-05-24", 33.3, 0.536, "Series J"],
    ["SpaceX", "2020-08-18", 46.0, 1.9, "Series J"],
    ["SpaceX", "2021-02-16", 74.0, 0.85, "Series J"],
    ["SpaceX", "2022-12-01", 137.0, 0.75, "Series J"],
    ["SpaceX", "2023-12-01", 180.0, 0.75, "Secondary"],
    ["SpaceX", "2024-12-01", 255.0, 1.25, "Secondary"],
    ["SpaceX", "2025-12-01", 350.0, 0, "Secondary"],

    # ByteDance
    ["ByteDance", "2012-07-01", 0.022, 0.005, "Series A"],
    ["ByteDance", "2014-06-01", 0.5, 0.1, "Series C"],
    ["ByteDance", "2016-12-01", 11.0, 0.4, "Series D"],
    ["ByteDance", "2018-10-01", 75.0, 3.0, "Series E"],
    ["ByteDance", "2020-12-01", 180.0, 1.9, "Series F"],
    ["ByteDance", "2021-03-01", 250.0, 2.25, "Secondary"],
    ["ByteDance", "2024-12-01", 268.0, 0, "Secondary"],
    ["ByteDance", "2025-11-17", 300.0, 0, "Secondary"],

    # OpenAI
    ["OpenAI", "2015-12-01", 0.001, 0.001, "Nonprofit Seed"],
    ["OpenAI", "2019-07-22", 1.0, 1.0, "Microsoft Investment"],
    ["OpenAI", "2023-01-23", 29.0, 10.0, "Microsoft Investment"],
    ["OpenAI", "2024-10-02", 157.0, 6.6, "Series E"],
    ["OpenAI", "2025-03-31", 300.0, 40.0, "Series F"],
    ["OpenAI", "2025-10-01", 500.0, 6.6, "Secondary"],

    # Databricks
    ["Databricks", "2013-09-01", 0.014, 0.014, "Series A"],
    ["Databricks", "2017-08-01", 0.7, 0.06, "Series C"],
    ["Databricks", "2019-10-22", 6.2, 0.4, "Series F"],
    ["Databricks", "2021-08-31", 38.0, 1.6, "Series H"],
    ["Databricks", "2023-09-14", 43.0, 0.5, "Series I"],
    ["Databricks", "2024-11-28", 62.0, 10.0, "Series J"],
    ["Databricks", "2025-09-08", 100.0, 1.0, "Series K"],

    # Anthropic
    ["Anthropic", "2021-05-01", 0.124, 0.124, "Series A"],
    ["Anthropic", "2023-09-01", 18.4, 3.0, "Series C"],
    ["Anthropic", "2024-02-01", 18.4, 2.0, "Series C"],
    ["Anthropic", "2025-03-01", 62.0, 3.5, "Series E"],
    ["Anthropic", "2025-09-01", 170.0, 5.0, "Series F"],
]

df = pd.DataFrame(data, columns=["company", "date", "valuation ($B)", "capital_raised ($B)", "funding_round"])
df["date"] = pd.to_datetime(df["date"])
df["valuation ($B)"] = pd.to_numeric(df["valuation ($B)"], errors="coerce")
df["capital_raised ($B)"] = pd.to_numeric(df["capital_raised ($B)"], errors="coerce")
df["cumulative_raised ($B)"] = df.groupby("company")["capital_raised ($B)"].cumsum()

# Founding dates
founding_dates = {
    "SpaceX": "2002-03-14",
    "ByteDance": "2012-03-01",
    "OpenAI": "2015-12-11",
    "Databricks": "2013-01-01",
    "Anthropic": "2021-01-01"
}

# Company info
company_info = {
    "OpenAI": [
        "AI research and deployment company behind GPT models and ChatGPT.",
        "Raised record $40B in March 2025 — largest private tech round ever.",
        "Current valuation: $500B (Oct 2025) — world’s most valuable private company."
    ],
    "SpaceX": [
        "Founded by Elon Musk in 2002, focused on space transport and satellite internet.",
        "Operates Starlink, Falcon, and Starship programs.",
        "Current valuation: $350B (Dec 2025)."
    ],
    "ByteDance": [
        "Parent company of TikTok and Douyin.",
        "Dominates global short-form video and digital advertising.",
        "Current valuation: $300B (Nov 2025)."
    ],
    "Anthropic": [
        "AI safety company founded by ex-OpenAI team, creators of Claude.",
        "Backed by Google and Amazon.",
        "Current valuation: $170B (Sep 2025)."
    ],
    "Databricks": [
        "Data and AI platform built on Apache Spark architecture.",
        "Raised $10B Series J in Nov 2024.",
        "Current valuation: $100B (Sep 2025)."
    ]
}

# ---------------------------
# Helper: plot generator
# ---------------------------
def plot_company(company):
    company_df = df[df["company"] == company].sort_values("date")
    company_df["valuation ($B)"] = pd.to_numeric(company_df["valuation ($B)"], errors="coerce")
    company_df["cumulative_raised ($B)"] = pd.to_numeric(company_df["cumulative_raised ($B)"], errors="coerce")

    max_raise = float(company_df["cumulative_raised ($B)"].fillna(0).max() or 1)
    max_val = float(company_df["valuation ($B)"].fillna(0).max() or 1)

    founding_date = pd.to_datetime(founding_dates[company])
    today = pd.to_datetime(datetime.today().date())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["valuation ($B)"],
        mode="lines+markers",
        name="Valuation ($B)",
        line=dict(color="royalblue", width=3),
        marker=dict(size=8),
        hovertemplate="<b>%{text}</b><br>Date: %{x}<br>Valuation: $%{y}B<extra></extra>",
        text=company_df["funding_round"]
    ))
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["cumulative_raised ($B)"],
        mode="lines+markers",
        name="Cumulative Raised ($B)",
        yaxis="y2",
        line=dict(color="orange", width=3, dash="dot"),
        marker=dict(size=8),
        hovertemplate="<b>%{text}</b><br>Date: %{x}<br>Total Raised: $%{y}B<extra></extra>",
        text=company_df["funding_round"]
    ))
    fig.update_layout(
        title=f"{company} — Valuation and Capital Raised Over Time",
        xaxis=dict(title="Date", range=[founding_date, today]),
        yaxis=dict(title="Valuation ($B)", range=[0, max_val * 1.2]),
        yaxis2=dict(title="Cumulative Raised ($B)", overlaying="y", side="right", range=[0, max_raise * 1.2]),
        legend=dict(x=0, y=1.1, orientation="h"),
        height=600,
        template="plotly_dark",
        hovermode="x unified"
    )
    return fig, company_df

# ---------------------------
# Tabs for each company
# ---------------------------
tabs = st.tabs(["OpenAI", "SpaceX", "ByteDance", "Anthropic", "Databricks"])

for i, company in enumerate(["OpenAI", "SpaceX", "ByteDance", "Anthropic", "Databricks"]):
    with tabs[i]:
        fig, company_df = plot_company(company)
        col1, col2 = st.columns([3, 1])

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"### About {company}")
            for point in company_info[company]:
                st.markdown(f"- {point}")

            latest = company_df.iloc[-1]
            st.metric("Valuation", f"${latest['valuation ($B)']}B")
            st.metric("Total Raised", f"${latest['cumulative_raised ($B)']:.2f}B")
            st.metric("Latest Round", latest["funding_round"])

st.markdown("---")
st.caption("Data aggregated from public/private market estimates, press releases, and secondary transactions.")
