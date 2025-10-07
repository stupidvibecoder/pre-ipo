import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Private Market Tracker",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Private Market Tracker")
st.markdown("Visualizing valuation and funding data for the 5 biggest private companies.")

# -----------------------------
# Company Data
# -----------------------------
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
    ["ByteDance", "2014-01-01", 5, 0.3],
    ["ByteDance", "2017-04-01", 20, 2],
    ["ByteDance", "2018-10-01", 75, 3],
    ["ByteDance", "2021-03-01", 140, 5],
    ["ByteDance", "2024-06-01", 275, 8],

    # Shein
    ["Shein", "2018-01-01", 2, 0.3],
    ["Shein", "2020-08-01", 15, 0.5],
    ["Shein", "2022-04-01", 100, 1],
    ["Shein", "2024-06-01", 66, 1],
]

df = pd.DataFrame(data, columns=["Company", "Date", "Valuation ($B)", "Capital Raised ($B)"])
df["Date"] = pd.to_datetime(df["Date"])
df["Capital Raised ($B)"] = pd.to_numeric(df["Capital Raised ($B)"], errors="coerce")

# -----------------------------
# Descriptions
# -----------------------------
descriptions = {
    "SpaceX": [
        "Develops and launches rockets and satellites.",
        "Leader in commercial space and Starlink internet.",
        "Valuation surge tied to Starlink and Mars ambitions.",
        "IPO timeline uncertain but highly anticipated."
    ],
    "Stripe": [
        "Fintech infrastructure for online payments.",
        "Backbone for thousands of digital-first companies.",
        "Valuation peaked in 2021; down amid fintech slowdown.",
        "IPO expected after profitability stabilizes."
    ],
    "OpenAI": [
        "AI research and product company behind ChatGPT.",
        "Massive valuation increase post-GPT-4 launch.",
        "Microsoft partnership adds distribution moat.",
        "Revenue growth driven by API and enterprise deals."
    ],
    "ByteDance": [
        "Parent company of TikTok and Douyin.",
        "Global leader in short-form video content.",
        "Diversifying into productivity, AI, and gaming.",
        "IPO delayed amid Chinese regulatory pressures."
    ],
    "Shein": [
        "Global fast-fashion e-commerce giant.",
        "Known for rapid trend cycles and low-cost supply chain.",
        "Exploring IPO in London or New York.",
        "Facing ESG and labor scrutiny but massive user growth."
    ]
}

# Founding years for x-axis start
founding_years = {
    "SpaceX": 2002,
    "Stripe": 2010,
    "OpenAI": 2015,
    "ByteDance": 2012,
    "Shein": 2008
}

# -----------------------------
# Sidebar selection
# -----------------------------
company = st.sidebar.selectbox("Select a company:", df["Company"].unique())

company_df = df[df["Company"] == company].sort_values("Date").copy()
company_df["cumulative_raised ($B)"] = company_df["Capital Raised ($B)"].cumsum()

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns([2, 1])

# -----------------------------
# Plotly Chart
# -----------------------------
with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=company_df["Date"],
        y=company_df["Valuation ($B)"],
        name="Valuation ($B)",
        mode="lines+markers",
        line=dict(color="deepskyblue", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=company_df["Date"],
        y=company_df["cumulative_raised ($B)"],
        name="Cumulative Capital Raised ($B)",
        mode="lines+markers",
        line=dict(color="orange", width=3, dash="dot"),
        yaxis="y2"
    ))

    # X-axis range from founding date to today
    start_date = datetime(founding_years[company], 1, 1)
    end_date = datetime.today()

    fig.update_layout(
        title=f"{company}: Valuation vs. Cumulative Capital Raised",
        xaxis=dict(title="Date", range=[start_date, end_date]),
        yaxis=dict(title="Valuation ($B)"),
        yaxis2=dict(
            title="Cumulative Capital Raised ($B)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        template="plotly_dark",
        legend=dict(x=0.01, y=0.99)
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Company Info
# -----------------------------
with col2:
    st.markdown(f"### About {company}")
    for bullet in descriptions[company]:
        st.markdown(f"- {bullet}")

# -----------------------------
# Expectation vs. Reality Section
# -----------------------------
st.markdown("---")
st.header("📈 Expectation vs. Reality")

# Compute expected valuation given CAGR baseline
latest_row = company_df.iloc[-1]
first_row = company_df.iloc[0]
years = (latest_row["Date"] - first_row["Date"]).days / 365

expected_cagr = 0.40  # 40% baseline
expected_val = first_row["Valuation ($B)"] * ((1 + expected_cagr) ** years)
actual_val = latest_row["Valuation ($B)"]

performance_delta = (actual_val - expected_val) / expected_val * 100
delta_label = "Above expected" if performance_delta > 0 else "Below expected"
delta_color = "normal" if performance_delta > 0 else "inverse"

st.metric(
    "Valuation vs. Expected (40% CAGR baseline)",
    f"{performance_delta:+.1f}%",
    delta=delta_label,
    delta_color=delta_color
)

# -----------------------------
# Consensus + My Take sections
# -----------------------------
st.markdown("---")
st.subheader("🧭 Consensus View")
st.markdown(
    """
    _How the market generally views this company:_
    - Key valuation drivers
    - Growth narrative and investor sentiment
    - Implied expectations behind valuation multiples
    """
)

st.subheader("💡 My Take")
st.markdown(
    """
    _Your personal insight, variant perception, or counter-view:_
    - What the market might be missing
    - Leading indicators or red flags
    - What could change your thesis
    """
)
