import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Private Market Tracker", layout="wide")

st.title("📈 Private Market Tracker")
st.write("Visualizing valuation and funding data for the 10 biggest private companies.")

# ---------------------------
# Data setup
# ---------------------------
data = [
    # SpaceX
    ["SpaceX", "2015-01-01", 12, 1],
    ["SpaceX", "2017-12-01", 21, 1.2],
    ["SpaceX", "2020-08-01", 46, 2.1],
    ["SpaceX", "2023-12-01", 150, 2.5],

    # Stripe
    ["Stripe", "2016-01-01", 5, 0.5],
    ["Stripe", "2018-09-01", 20, 0.8],
    ["Stripe", "2021-03-01", 95, 2],
    ["Stripe", "2023-12-01", 65, 0.3],

    # OpenAI
    ["OpenAI", "2018-01-01", 1, 1],
    ["OpenAI", "2021-01-01", 14, 1],
    ["OpenAI", "2023-12-01", 80, 10],

    # ByteDance
    ["ByteDance", "2017-04-01", 11, 1],
    ["ByteDance", "2018-10-01", 75, 3],
    ["ByteDance", "2020-03-01", 140, 5],
    ["ByteDance", "2023-12-01", 268, 2],

    # Shein
    ["Shein", "2018-06-01", 2.5, 0.3],
    ["Shein", "2020-08-01", 15, 0.5],
    ["Shein", "2022-05-01", 100, 1],
    ["Shein", "2023-12-01", 66, 0.5],

    # Canva
    ["Canva", "2018-01-01", 1, 0.04],
    ["Canva", "2020-06-01", 6, 0.06],
    ["Canva", "2021-09-01", 40, 0.2],
    ["Canva", "2023-12-01", 26, 0.1],

    # Databricks
    ["Databricks", "2019-02-01", 2.8, 0.25],
    ["Databricks", "2020-10-01", 6.2, 0.5],
    ["Databricks", "2021-09-01", 38, 1.6],
    ["Databricks", "2023-09-01", 43, 0.5],

    # Epic Games
    ["Epic Games", "2018-10-01", 15, 1.25],
    ["Epic Games", "2020-08-01", 17.3, 1.8],
    ["Epic Games", "2022-04-01", 32, 2],
    ["Epic Games", "2023-12-01", 31.5, 0.5],

    # Revolut
    ["Revolut", "2018-04-01", 1.7, 0.25],
    ["Revolut", "2020-07-01", 5.5, 0.5],
    ["Revolut", "2021-07-01", 33, 0.8],
    ["Revolut", "2023-12-01", 25.7, 0.3],

    # Reddit
    ["Reddit", "2017-02-01", 1.8, 0.2],
    ["Reddit", "2019-02-01", 3, 0.3],
    ["Reddit", "2021-08-01", 10, 0.7],
    ["Reddit", "2023-12-01", 6.6, 0.2]
]

df = pd.DataFrame(data, columns=["company", "date", "valuation ($B)", "capital_raised ($B)"])
df["date"] = pd.to_datetime(df["date"])
df["valuation ($B)"] = pd.to_numeric(df["valuation ($B)"], errors="coerce")
df["capital_raised ($B)"] = pd.to_numeric(df["capital_raised ($B)"], errors="coerce")

# Compute cumulative capital raised
df["cumulative_raised ($B)"] = df.groupby("company")["capital_raised ($B)"].cumsum()

# ---------------------------
# Company descriptions
# ---------------------------
company_info = {
    "SpaceX": [
        "Founded by Elon Musk in 2002, focused on space transport and satellite internet.",
        "Operates Starlink, Falcon, and Starship programs.",
        "Valuation growth tied to launch cadence and Starlink expansion."
    ],
    "Stripe": [
        "Payment infrastructure company powering online transactions globally.",
        "Expanding into financial services: issuing, lending, and banking APIs.",
        "Revenue driven by e-commerce and SaaS adoption."
    ],
    "OpenAI": [
        "AI research and deployment company behind GPT models and ChatGPT.",
        "Transitioned from non-profit to capped-profit in 2019.",
        "Major funding from Microsoft and other strategic investors."
    ],
    "ByteDance": [
        "Chinese tech giant and parent of TikTok and Douyin.",
        "Generates large advertising revenue from short-form content.",
        "Exploring AI, gaming, and productivity software verticals."
    ],
    "Shein": [
        "Fast-fashion e-commerce giant headquartered in Singapore.",
        "Leverages data-driven supply chain and influencer marketing.",
        "Facing scrutiny over labor and sustainability practices."
    ],
    "Canva": [
        "Australian design platform democratizing visual content creation.",
        "Serves individuals, small businesses, and enterprises.",
        "Growth driven by education and team collaboration tools."
    ],
    "Databricks": [
        "Data and AI platform built on Apache Spark architecture.",
        "Helps enterprises unify data engineering, analytics, and ML workflows.",
        "Strong enterprise adoption; competitor to Snowflake."
    ],
    "Epic Games": [
        "Creator of Fortnite and Unreal Engine.",
        "Diversified across gaming, developer tools, and metaverse infrastructure.",
        "Valuation supported by strong IP and ecosystem."
    ],
    "Revolut": [
        "UK-based neobank offering multi-currency accounts and financial services.",
        "Expanding globally with investments, crypto, and banking products.",
        "Monetization from premium tiers and interchange fees."
    ],
    "Reddit": [
        "Online discussion and community platform.",
        "Revenue from ads and premium subscriptions.",
        "Considering IPO and building new monetization streams."
    ]
}

# ---------------------------
# Streamlit app layout
# ---------------------------
st.sidebar.header("Private Company Tracker")
company_list = sorted(df["company"].unique())
selected_company = st.sidebar.selectbox("Select a company:", company_list)

company_df = df[df["company"] == selected_company].sort_values("date")

# Ensure numeric data is clean
company_df["valuation ($B)"] = pd.to_numeric(company_df["valuation ($B)"], errors="coerce")
company_df["cumulative_raised ($B)"] = pd.to_numeric(company_df["cumulative_raised ($B)"], errors="coerce")

max_raise = float(company_df["cumulative_raised ($B)"].fillna(0).max() or 1)
max_valuation = float(company_df["valuation ($B)"].fillna(0).max() or 1)

# ---------------------------
# Plot
# ---------------------------
fig = go.Figure()

# Valuation line
fig.add_trace(go.Scatter(
    x=company_df["date"],
    y=company_df["valuation ($B)"],
    mode="lines+markers",
    name="Valuation ($B)",
    line=dict(color="royalblue", width=3)
))

# Cumulative capital raised line
fig.add_trace(go.Scatter(
    x=company_df["date"],
    y=company_df["cumulative_raised ($B)"],
    mode="lines+markers",
    name="Cumulative Raised ($B)",
    yaxis="y2",
    line=dict(color="orange", width=3, dash="dot")
))

fig.update_layout(
    title=f"{selected_company} — Valuation and Cumulative Capital Raised Over Time",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Valuation ($B)", range=[0, max_valuation * 1.2]),
    yaxis2=dict(
        title="Cumulative Raised ($B)",
        overlaying="y",
        side="right",
        range=[0, max_raise * 1.2]
    ),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=600,
    template="plotly_dark"
)

# ---------------------------
# Display
# ---------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"### {selected_company}")
    for point in company_info.get(selected_company, []):
        st.markdown(f"- {point}")
