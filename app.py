import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Private Market Tracker", layout="wide")

st.title("📈 Private Market Tracker")
st.write("Visualizing valuation and funding data for the biggest private companies.")

# ---------------------------
# Data setup - Complete funding history
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
    ["SpaceX", "2020-02-01", 36.0, 0.25, "Series J"],
    ["SpaceX", "2020-08-18", 46.0, 1.9, "Series J"],
    ["SpaceX", "2021-02-16", 74.0, 0.85, "Series J"],
    ["SpaceX", "2021-04-01", 74.0, 0.314, "Secondary"],
    ["SpaceX", "2022-05-01", 125.0, 1.68, "Series J"],
    ["SpaceX", "2022-07-01", 125.0, 0.25, "Series J"],
    ["SpaceX", "2022-12-01", 137.0, 0.75, "Series J"],
    ["SpaceX", "2023-01-01", 137.0, 0.75, "Secondary"],
    ["SpaceX", "2023-06-01", 150.0, 0.76, "Secondary"],
    ["SpaceX", "2023-12-01", 180.0, 0.75, "Secondary"],
    ["SpaceX", "2024-06-01", 210.0, 0, "Secondary"],
    ["SpaceX", "2024-12-01", 255.0, 1.25, "Secondary"],
    ["SpaceX", "2025-12-01", 350.0, 0, "Secondary"],

    # ByteDance
    ["ByteDance", "2012-07-01", 0.022, 0.005, "Series A"],
    ["ByteDance", "2013-09-01", 0.06, 0.01, "Series B"],
    ["ByteDance", "2014-06-01", 0.5, 0.1, "Series C"],
    ["ByteDance", "2016-12-01", 11.0, 0.4, "Series D"],
    ["ByteDance", "2017-04-01", 20.0, 1.0, "Series D"],
    ["ByteDance", "2018-10-01", 75.0, 3.0, "Series E"],
    ["ByteDance", "2018-12-01", 78.0, 1.0, "Secondary"],
    ["ByteDance", "2020-12-01", 180.0, 1.9, "Series F"],
    ["ByteDance", "2021-03-01", 250.0, 2.25, "Secondary"],
    ["ByteDance", "2023-03-15", 225.0, 0.5, "Secondary"],
    ["ByteDance", "2024-12-01", 268.0, 0, "Secondary"],
    ["ByteDance", "2025-11-17", 300.0, 0, "Secondary"],

    # OpenAI
    ["OpenAI", "2015-12-01", 0.001, 0.001, "Nonprofit Seed"],
    ["OpenAI", "2019-03-11", 0.1, 0.1, "First Investment"],
    ["OpenAI", "2019-07-22", 1.0, 1.0, "Microsoft Investment"],
    ["OpenAI", "2023-01-23", 29.0, 10.0, "Microsoft Investment"],
    ["OpenAI", "2023-04-28", 30.0, 0.3, "Series E"],
    ["OpenAI", "2024-10-02", 157.0, 6.6, "Series E"],
    ["OpenAI", "2025-03-31", 300.0, 40.0, "Series F"],
    ["OpenAI", "2025-10-01", 500.0, 6.6, "Secondary"],

    # Stripe
    ["Stripe", "2010-01-01", 0.004, 0, "Seed"],
    ["Stripe", "2011-03-28", 0.02, 0.002, "Seed"],
    ["Stripe", "2012-02-01", 0.1, 0.018, "Series A"],
    ["Stripe", "2012-07-01", 0.5, 0.02, "Series B"],
    ["Stripe", "2014-01-22", 1.75, 0.08, "Series C"],
    ["Stripe", "2014-12-02", 3.5, 0.07, "Series C-I"],
    ["Stripe", "2015-07-01", 5.0, 0.1, "Series C-II"],
    ["Stripe", "2016-11-25", 9.2, 0.15, "Series D"],
    ["Stripe", "2018-09-27", 20.0, 0.245, "Series E"],
    ["Stripe", "2019-01-01", 22.5, 0.1, "Series E"],
    ["Stripe", "2019-09-19", 35.0, 0.25, "Series F"],
    ["Stripe", "2020-03-25", 36.0, 0.6, "Series G"],
    ["Stripe", "2021-03-14", 95.0, 0.6, "Series H"],
    ["Stripe", "2023-03-15", 50.0, 6.87, "Series I"],
    ["Stripe", "2024-04-08", 65.0, 0.694, "Series I-II"],
    ["Stripe", "2024-11-01", 70.0, 0.861, "Series I-III"],
    ["Stripe", "2025-02-27", 91.5, 0, "Secondary"],

    # Databricks
    ["Databricks", "2013-09-01", 0.014, 0.014, "Series A"],
    ["Databricks", "2016-02-01", 0.2, 0.033, "Series B"],
    ["Databricks", "2017-08-01", 0.7, 0.06, "Series C"],
    ["Databricks", "2019-02-05", 2.75, 0.25, "Series D"],
    ["Databricks", "2019-10-22", 6.2, 0.4, "Series F"],
    ["Databricks", "2021-02-01", 28.0, 1.0, "Series G"],
    ["Databricks", "2021-08-31", 38.0, 1.6, "Series H"],
    ["Databricks", "2023-09-14", 43.0, 0.5, "Series I"],
    ["Databricks", "2024-11-28", 62.0, 10.0, "Series J"],
    ["Databricks", "2025-01-14", 62.0, 5.0, "Debt"],
    ["Databricks", "2025-09-08", 100.0, 1.0, "Series K"],

    # Shein
    ["Shein", "2013-10-01", 0.05, 0.005, "Seed"],
    ["Shein", "2015-01-01", 0.5, 0.03, "Series A"],
    ["Shein", "2018-01-01", 2.5, 0.2, "Series B"],
    ["Shein", "2019-01-01", 5.0, 0.5, "Series C"],
    ["Shein", "2020-08-01", 15.0, 0.55, "Series D"],
    ["Shein", "2021-08-01", 30.0, 1.0, "Series E"],
    ["Shein", "2022-04-01", 100.0, 1.5, "Series F"],
    ["Shein", "2023-05-01", 66.0, 2.0, "Series G"],

    # Canva
    ["Canva", "2012-08-01", 0.003, 0.0015, "Seed"],
    ["Canva", "2013-03-01", 0.01, 0.003, "Seed"],
    ["Canva", "2015-10-01", 0.165, 0.015, "Series A"],
    ["Canva", "2018-01-01", 1.0, 0.04, "Series B"],
    ["Canva", "2019-05-21", 2.5, 0.07, "Series C"],
    ["Canva", "2020-06-01", 6.0, 0.06, "Series D"],
    ["Canva", "2021-04-01", 15.0, 0.071, "Series E"],
    ["Canva", "2021-09-14", 40.0, 0.2, "Series F"],
    ["Canva", "2024-03-01", 26.0, 0, "Secondary"],

    # Epic Games
    ["Epic Games", "2012-07-01", 0.825, 0.33, "Series A"],
    ["Epic Games", "2018-10-01", 15.0, 1.25, "Series B"],
    ["Epic Games", "2020-04-17", 17.3, 0.75, "Series C"],
    ["Epic Games", "2020-08-06", 17.3, 1.78, "Series D"],
    ["Epic Games", "2021-04-13", 28.7, 1.0, "Series E"],
    ["Epic Games", "2022-04-11", 31.5, 2.0, "Series F"],

    # Revolut
    ["Revolut", "2015-07-01", 0.05, 0.002, "Seed"],
    ["Revolut", "2016-07-01", 0.1, 0.01, "Series A"],
    ["Revolut", "2017-07-01", 0.3, 0.066, "Series B"],
    ["Revolut", "2018-04-26", 1.7, 0.25, "Series C"],
    ["Revolut", "2020-02-24", 5.5, 0.5, "Series D"],
    ["Revolut", "2021-07-15", 33.0, 0.8, "Series E"],
    ["Revolut", "2024-08-01", 45.0, 0, "Secondary"],

    # Fanatics
    ["Fanatics", "2012-06-01", 0.22, 0.04, "Series A"],
    ["Fanatics", "2013-08-01", 0.5, 0.15, "Series B"],
    ["Fanatics", "2016-01-01", 1.0, 0.17, "Series C"],
    ["Fanatics", "2017-08-01", 4.5, 0.2, "Series D"],
    ["Fanatics", "2019-06-01", 6.2, 0.15, "Series E"],
    ["Fanatics", "2020-08-01", 6.2, 0.35, "Series F"],
    ["Fanatics", "2021-08-04", 18.0, 0.325, "Series G"],
    ["Fanatics", "2022-03-01", 27.0, 1.5, "Series H"],
    ["Fanatics", "2023-12-01", 31.0, 0.7, "Series I"],
]

df = pd.DataFrame(data, columns=["company", "date", "valuation ($B)", "capital_raised ($B)", "funding_round"])
df["date"] = pd.to_datetime(df["date"])
df["valuation ($B)"] = pd.to_numeric(df["valuation ($B)"], errors="coerce")
df["capital_raised ($B)"] = pd.to_numeric(df["capital_raised ($B)"], errors="coerce")
df["cumulative_raised ($B)"] = df.groupby("company")["capital_raised ($B)"].cumsum()

# ---------------------------
# Company founding dates
# ---------------------------
founding_dates = {
    "SpaceX": "2002-03-14",
    "Stripe": "2009-01-01",
    "OpenAI": "2015-12-11",
    "ByteDance": "2012-03-01",
    "Shein": "2008-10-01",
    "Canva": "2012-01-01",
    "Databricks": "2013-01-01",
    "Epic Games": "1991-01-01",
    "Revolut": "2015-07-01",
    "Fanatics": "2011-01-01"
}

# ---------------------------
# Company info
# ---------------------------
company_info = {
    "SpaceX": [
        "Founded by Elon Musk in 2002, focused on space transport and satellite internet.",
        "Operates Starlink, Falcon, and Starship programs.",
        "Current valuation: $350B (Dec 2025) - 2nd most valuable private company."
    ],
    "Stripe": [
        "Payment infrastructure company powering online transactions globally.",
        "Expanding into financial services: issuing, lending, and banking APIs.",
        "Current valuation: $91.5B (Feb 2025) - processing $1.4T annually."
    ],
    "OpenAI": [
        "AI research and deployment company behind GPT models and ChatGPT.",
        "Raised record $40B in March 2025 - largest private tech round ever.",
        "Current valuation: $500B (Oct 2025) - world's most valuable private company."
    ],
    "ByteDance": [
        "Chinese tech giant and parent of TikTok and Douyin.",
        "Generates large advertising revenue from short-form content.",
        "Current valuation: $300B (Nov 2025) - 3rd most valuable private company."
    ],
    "Shein": [
        "Fast-fashion e-commerce giant headquartered in Singapore.",
        "Leverages data-driven supply chain and influencer marketing.",
        "Current valuation: $66B (May 2023) - facing IPO challenges."
    ],
    "Canva": [
        "Australian design platform democratizing visual content creation.",
        "Most valuable female-led startup globally.",
        "Current valuation: $26B (Mar 2024) - down from $40B peak."
    ],
    "Databricks": [
        "Data and AI platform built on Apache Spark architecture.",
        "Raised massive $10B Series J in Nov 2024.",
        "Current valuation: $100B (Sep 2025) - first time FCF positive."
    ],
    "Epic Games": [
        "Creator of Fortnite and Unreal Engine.",
        "Diversified across gaming, developer tools, and metaverse infrastructure.",
        "Current valuation: $31.5B (Apr 2022) - strong IP portfolio."
    ],
    "Revolut": [
        "UK-based neobank offering multi-currency accounts and financial services.",
        "First profit of $1.5B in 2024, preparing for UK banking license.",
        "Current valuation: $45B (Aug 2024) - fastest growing finance app."
    ],
    "Fanatics": [
        "Sports merchandise and memorabilia platform.",
        "Expanding into sports betting and trading cards.",
        "Current valuation: $31B (Dec 2023) - serves major sports leagues."
    ]
}

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.header("Private Company Tracker")
st.sidebar.subheader("Top 10 by Valuation:")
st.sidebar.write("1. OpenAI - $500B")
st.sidebar.write("2. SpaceX - $350B")
st.sidebar.write("3. ByteDance - $300B")
st.sidebar.write("4. Databricks - $100B")
st.sidebar.write("5. Stripe - $91.5B")
st.sidebar.write("6. Shein - $66B")
st.sidebar.write("7. Revolut - $45B")
st.sidebar.write("8. Fanatics - $31B")
st.sidebar.write("9. Epic Games - $31.5B")
st.sidebar.write("10. Canva - $26B")
st.sidebar.markdown("---")

company_list = sorted(df["company"].unique())
selected_company = st.sidebar.selectbox("Select a company:", company_list)

company_df = df[df["company"] == selected_company].sort_values("date")

# Clean data
company_df["valuation ($B)"] = pd.to_numeric(company_df["valuation ($B)"], errors="coerce")
company_df["cumulative_raised ($B)"] = pd.to_numeric(company_df["cumulative_raised ($B)"], errors="coerce")

max_raise = float(company_df["cumulative_raised ($B)"].fillna(0).max() or 1)
max_valuation = float(company_df["valuation ($B)"].fillna(0).max() or 1)

# ---------------------------
# Dynamic x-axis range
# ---------------------------
founding_date = pd.to_datetime(founding_dates.get(selected_company, company_df["date"].min()))
today = pd.to_datetime(datetime.today().date())

# ---------------------------
# Plot
# ---------------------------
fig = go.Figure()

# Add valuation line
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

# Add cumulative raised line
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
    title=f"{selected_company} — Valuation and Cumulative Capital Raised Over Time",
    xaxis=dict(title="Date", range=[founding_date, today]),
    yaxis=dict(title="Valuation ($B)", range=[0, max_valuation * 1.2]),
    yaxis2=dict(
        title="Cumulative Raised ($B)",
        overlaying="y",
        side="right",
        range=[0, max_raise * 1.2]
    ),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=600,
    template="plotly_dark",
    hovermode="x unified"
)

# ---------------------------
# Display
# ---------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"### About {selected_company}")
    for point in company_info.get(selected_company, []):
        st.markdown(f"- {point}")
    
    st.markdown("### Latest Round")
    latest = company_df.iloc[-1]
    st.metric("Valuation", f"${latest['valuation ($B)']}B")
    st.metric("Total Raised", f"${latest['cumulative_raised ($B)']:.2f}B")
    st.metric("Latest Round", latest["funding_round"])


