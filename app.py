import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Private Market Tracker", layout="wide")

st.title("📈 Private Market Tracker")
st.write("Valuation and funding history for top private tech companies — plus insights beyond PitchBook and Crunchbase.")

# ---------------------------
# Data setup
# ---------------------------
data = [
    # SpaceX
    ["SpaceX", "2002-12-18", 0.005, 0.001],
    ["SpaceX", "2005-03-09", 0.05, 0.05],
    ["SpaceX", "2008-08-01", 0.5, 0.02],
    ["SpaceX", "2010-10-28", 1.0, 0.05],
    ["SpaceX", "2015-01-20", 12.0, 1.0],
    ["SpaceX", "2017-11-27", 21.0, 0.45],
    ["SpaceX", "2018-04-01", 24.0, 0.21],
    ["SpaceX", "2019-05-24", 33.3, 0.536],
    ["SpaceX", "2020-08-18", 46.0, 1.9],
    ["SpaceX", "2021-02-16", 74.0, 0.85],
    ["SpaceX", "2022-12-01", 137.0, 0.75],
    ["SpaceX", "2023-12-01", 180.0, 0.75],
    ["SpaceX", "2024-12-01", 255.0, 1.25],
    ["SpaceX", "2025-12-01", 350.0, 0.0],

    # ByteDance
    ["ByteDance", "2012-07-01", 0.022, 0.005],
    ["ByteDance", "2014-06-01", 0.5, 0.1],
    ["ByteDance", "2016-12-01", 11.0, 0.4],
    ["ByteDance", "2018-10-01", 75.0, 3.0],
    ["ByteDance", "2020-12-01", 180.0, 1.9],
    ["ByteDance", "2021-03-01", 250.0, 2.25],
    ["ByteDance", "2024-12-01", 268.0, 0.0],
    ["ByteDance", "2025-11-17", 300.0, 0.0],

    # OpenAI
    ["OpenAI", "2015-12-01", 0.001, 0.001],
    ["OpenAI", "2019-07-22", 1.0, 1.0],
    ["OpenAI", "2023-01-23", 29.0, 10.0],
    ["OpenAI", "2024-10-02", 157.0, 6.6],
    ["OpenAI", "2025-03-31", 300.0, 40.0],
    ["OpenAI", "2025-10-01", 500.0, 6.6],

    # Databricks
    ["Databricks", "2013-09-01", 0.014, 0.014],
    ["Databricks", "2017-08-01", 0.7, 0.06],
    ["Databricks", "2019-10-22", 6.2, 0.4],
    ["Databricks", "2021-08-31", 38.0, 1.6],
    ["Databricks", "2023-09-14", 43.0, 0.5],
    ["Databricks", "2024-11-28", 62.0, 10.0],
    ["Databricks", "2025-09-08", 100.0, 1.0],

    # Anthropic
    ["Anthropic", "2021-05-01", 0.124, 0.124],
    ["Anthropic", "2023-09-01", 18.4, 3.0],
    ["Anthropic", "2024-02-01", 18.4, 2.0],
    ["Anthropic", "2025-03-01", 62.0, 3.5],
    ["Anthropic", "2025-09-01", 170.0, 5.0],
]

df = pd.DataFrame(data, columns=["company", "date", "valuation ($B)", "capital_raised ($B)"])
df["date"] = pd.to_datetime(df["date"])
df["cumulative_raised ($B)"] = df.groupby("company")["capital_raised ($B)"].cumsum()

founding_dates = {
    "SpaceX": "2002-03-14",
    "ByteDance": "2012-03-01",
    "OpenAI": "2015-12-11",
    "Databricks": "2013-01-01",
    "Anthropic": "2021-01-01"
}

company_info = {
    "OpenAI": [
        "AI research and deployment company behind GPT models and ChatGPT.",
        "Raised $40B in 2025 — largest private tech round ever.",
        "Current valuation: $500B (Oct 2025)."
    ],
    "SpaceX": [
        "Founded by Elon Musk in 2002, focused on space transport and Starlink.",
        "Operates Falcon, Starship, and satellite programs.",
        "Current valuation: $350B (Dec 2025)."
    ],
    "ByteDance": [
        "Parent company of TikTok and Douyin.",
        "Dominates global short-form video and digital advertising.",
        "Current valuation: $300B (Nov 2025)."
    ],
    "Anthropic": [
        "AI safety company founded by ex-OpenAI team, creators of Claude.",
        "Backed by Google ($3B+) and Amazon ($8B).",
        "Current valuation: $170B (Sep 2025)."
    ],
    "Databricks": [
        "Data and AI platform built on Apache Spark architecture.",
        "Raised $10B Series J in 2024.",
        "Current valuation: $100B (Sep 2025)."
    ]
}

# ---------------------------
# Helper: company analytics
# ---------------------------
def compute_metrics(company_df):
    start_row = company_df.iloc[0]
    end_row = company_df.iloc[-1]
    years = (end_row["date"] - start_row["date"]).days / 365
    if years <= 0:
        return None

    cagr = ((end_row["valuation ($B)"] / start_row["valuation ($B)"]) ** (1 / years) - 1) * 100
    total_raise = end_row["cumulative_raised ($B)"]
    val_efficiency = end_row["valuation ($B)"] / total_raise if total_raise > 0 else None

    # "Expected" valuation assuming a standard 40% annual growth (proxy for market expectation)
    expected_val = start_row["valuation ($B)"] * (1.4 ** years)
    performance_delta = (end_row["valuation ($B)"] - expected_val) / expected_val * 100

    return {
        "years": years,
        "CAGR": cagr,
        "Valuation Efficiency": val_efficiency,
        "Performance Delta": performance_delta,
        "Expected Valuation": expected_val
    }

# ---------------------------
# Helper: chart builder
# ---------------------------
def plot_company(company):
    company_df = df[df["company"] == company].sort_values("date")
    metrics = compute_metrics(company_df)

    founding_date = pd.to_datetime(founding_dates[company])
    today = pd.to_datetime(datetime.today().date())

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["valuation ($B)"],
        mode="lines+markers",
        name="Valuation ($B)",
        line=dict(color="royalblue", width=3),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["cumulative_raised ($B)"],
        mode="lines+markers",
        name="Cumulative Raised ($B)",
        yaxis="y2",
        line=dict(color="orange", width=3, dash="dot"),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=f"{company}: Valuation & Capital Raised Over Time",
        xaxis=dict(title="Date", range=[founding_date, today]),
        yaxis=dict(title="Valuation ($B)"),
        yaxis2=dict(title="Cumulative Raised ($B)", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h"),
        template="plotly_dark",
        hovermode="x unified",
        height=550
    )
    return fig, metrics

# ---------------------------
# Main app tabs
# ---------------------------
tabs = st.tabs(["OpenAI", "SpaceX", "ByteDance", "Anthropic", "Databricks"])

for i, company in enumerate(["OpenAI", "SpaceX", "ByteDance", "Anthropic", "Databricks"]):
    with tabs[i]:
        fig, metrics = plot_company(company)
        col1, col2 = st.columns([3, 1])

        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"### About {company}")
            for point in company_info[company]:
                st.markdown(f"- {point}")

            st.divider()
            if metrics:
                st.markdown("### ⚙️ Capital Efficiency")
                st.metric("Valuation-to-Capital Multiple", f"{metrics['Valuation Efficiency']:.1f}×")
                st.metric("Valuation CAGR", f"{metrics['CAGR']:.1f}% / yr")

                if metrics["Performance Delta"] > 0:
    st.metric(
        "Valuation vs. Expected (40% CAGR baseline)",
        f"{metrics['Performance Delta']:+.1f}%",
        delta="Above expected",
        delta_color="normal"
    )
else:
    st.metric(
        "Valuation vs. Expected (40% CAGR baseline)",
        f"{metrics['Performance Delta']:+.1f}%",
        delta="Below expected",
        delta_color="inverse"
    )


            st.markdown("### 🧠 Consensus’s Take")
            st.text_area(f"Consensus view on {company}", key=f"{company}_consensus")

            st.markdown("### 💭 My Take")
            st.text_area(f"My view on {company}", key=f"{company}_mytake")

st.caption("Data aggregated from public/private sources; valuation estimates as of 2025.")
