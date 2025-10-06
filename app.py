# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

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

# --- Company Descriptions ---
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

company_df = df[df["company"] == selected_company]

col1, col2 = st.columns([2, 1])

# --- Chart: Valuation over time ---
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

# --- Company Description ---
with col2:
    st.subheader(f"About {selected_company}")
    bullets = company_summaries.get(selected_company, ["No description available."])
    for point in bullets:
        st.markdown(f"- {point}")
