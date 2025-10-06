# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# --- Company Summaries ---
company_summaries = {
    "SpaceX": [
        "Founded by Elon Musk in 2002; leading private space company.",
        "Operates reusable rocket systems (Falcon 9, Starship).",
        "Major contracts with NASA and Starlink satellite expansion.",
        "Valuation growth driven by Starlink's broadband potential."
    ],
    "Stripe": [
        "Fintech platform enabling online payments and commerce infrastructure.",
        "Serves millions of businesses globally (Shopify, Amazon, etc.).",
        "Diversifying into lending, banking, and identity tools.",
        "Valuation volatility reflects fintech multiple compression."
    ],
    "OpenAI": [
        "AI research and product company behind ChatGPT and GPT models.",
        "Backed by Microsoft with multi-billion-dollar investment.",
        "Revenue model driven by API usage and enterprise partnerships.",
        "Seen as a key leader in generative AI."
    ],
    "ByteDance": [
        "Parent company of TikTok and Douyin.",
        "One of the most valuable startups globally.",
        "Expanding into productivity (Lark), gaming, and AI tools.",
        "IPO prospects watched closely amid China regulatory pressures."
    ],
    "Databricks": [
        "Enterprise data platform built on Apache Spark and lakehouse architecture.",
        "Used by Fortune 500 firms for AI and analytics workloads.",
        "Competes with Snowflake and AWS in data infrastructure.",
        "IPO expected once markets stabilize."
    ],
    "Canva": [
        "Design platform simplifying creative work for non-designers.",
        "Used by over 100M users globally across education and business.",
        "Expanding into enterprise productivity and team collaboration.",
        "High retention driven by product-led growth model."
    ],
    "Shein": [
        "China-founded fast fashion e-commerce giant.",
        "Known for ultra-fast design-to-market cycles and social media virality.",
        "Strong global sales, especially in U.S. and Europe.",
        "Facing scrutiny over labor and sustainability practices."
    ],
    "Epic Games": [
        "Developer of Fortnite and Unreal Engine.",
        "Unreal Engine is core tech for gaming, film, and metaverse tools.",
        "Backed by Sony and Tencent with major strategic stakes.",
        "Epic Store expanding as alternative to Steam."
    ],
    "Revolut": [
        "UK-based neobank offering payments, trading, and crypto services.",
        "Over 30M users across Europe and expanding into the U.S.",
        "Revenue driven by interchange, subscriptions, and FX fees.",
        "IPO plans delayed pending regulatory approvals."
    ],
    "Fanatics": [
        "Sports merchandise and collectibles platform.",
        "Exclusive licensing with NFL, NBA, MLB, and NCAA.",
        "Expanding into trading cards (Topps) and sports betting.",
        "Building integrated digital fan experience ecosystem."
    ],
    "Anthropic": [
        "AI safety and research company focused on alignment.",
        "Developer of Claude AI models, rival to OpenAI’s GPT series.",
        "Backed by Amazon, Google, and Salesforce.",
        "Positioned as a major enterprise AI alternative."
    ],
    "Reddit": [
        "Social aggregation and community discussion platform.",
        "Over 100K active communities and 70M+ daily users.",
        "Revenue from ads and premium memberships.",
        "IPO in progress as it scales global monetization."
    ]
}

# --- Main View ---
st.title("💼 Private Market Tracker")
st.markdown("Visualizing valuation and funding data for the 10 biggest private companies.")

company_df = df[df["company"] == selected_company].sort_values("date")
company_df["cumulative_raised ($B)"] = company_df["capital_raised ($B)"].cumsum()

col1, col2 = st.columns([2, 1])

# --- Combined Chart: Valuation + Cumulative Capital Raised ---
with col1:
    fig = go.Figure()

    # Primary axis: Valuation
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["valuation ($B)"],
        name="Valuation ($B)",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
        yaxis="y1"
    ))

    # Secondary axis: Cumulative capital raised
    fig.add_trace(go.Scatter(
        x=company_df["date"],
        y=company_df["cumulative_raised ($B)"],
        name="Cumulative Capital Raised ($B)",
        mode="lines+markers",
        line=dict(color="#ff7f0e", width=3, dash="dot"),
        yaxis="y2"
    ))

    # Clean dual-axis layout
    fig.update_layout(
        title=f"{selected_company}: Valuation vs. Cumulative Capital Raised",
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="rgba(200,200,200,0.1)"
        ),
        yaxis=dict(
            title="Valuation ($B)",
            side="left",
            showgrid=True,
            gridcolor="rgba(200,200,200,0.1)",
            zeroline=False
        ),
        yaxis2=dict(
    title="Cumulative Capital Raised ($B)",
    side="right",
    overlaying="y",
    showgrid=False,
    zeroline=False,
    range=[0, float(company_df["cumulative_raised ($B)"].fillna(0).astype(float).max()) * 1.2 if not company_df.empty else 1]
),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Company Description ---
with col2:
    st.subheader(f"About {selected_company}")
    bullets = company_summaries.get(selected_company, ["No description available."])
    for point in bullets:
        st.markdown(f"- {point}")
