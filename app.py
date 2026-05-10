import streamlit as st
from utils.fetch_data import get_stock_data
from utils.process_data import clean_data
from utils.visualize import plot_stock
import pandas as pd


st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)


st.markdown("""
    <style>

    /* FORCE FULL PAGE BACKGROUND */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #000000, #1a0033, #2b004f) !important;
        color: white !important;
    }

    /* REMOVE WHITE TOP HEADER (THIS IS YOUR MAIN ISSUE) */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* MAIN APP CONTAINER */
    .stApp {
        background: linear-gradient(135deg, #000000, #1a0033, #2b004f) !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a001a, #1a0033) !important;
    }

    /* REMOVE WHITE BLOCKS */
    .block-container {
        background: transparent !important;
    }

    /* KPI CARDS */
    div[style*="background-color:#1c1f26"] {
        background: linear-gradient(135deg, #14001f, #2a0040) !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 20px rgba(128, 0, 255, 0.25);
    }

    /* TEXT COLORS */
    h1, h2, h3, h4 {
        color: #e0ccff !important;
    }

   p, label {
    color: #c2b3ff !important;
}

    /* INPUT BOX */
    input {
        background-color: #1a0033 !important;
        color: white !important;
        border: 1px solid #6600cc !important;
    }

    /* SELECT BOX */
    div[data-baseweb="select"] > div {
        background-color: #1a0033 !important;
        color: white !important;
    }

    </style>
""", unsafe_allow_html=True)


st.sidebar.title("📊 Stock Dashboard")

symbol = st.sidebar.text_input("Stock Symbol", "AAPL")

period = st.sidebar.selectbox(
    "Select Time Period",
    ["7d", "1mo", "3mo", "6mo", "1y"]
)

show_data = st.sidebar.checkbox("Show Raw Data")


st.title("📈 Stock Market Analysis")


result = get_stock_data(symbol, period)

if result is None:
    st.error("❌ Invalid stock symbol or data unavailable")
    st.stop()

df = clean_data(result["data"])


col1, col2, col3 = st.columns(3)

current_price = df["Close"].iloc[-1]
previous_price = df["Close"].iloc[-2]

change = current_price - previous_price
change_percent = (change / previous_price) * 100



with col1:
    st.markdown(f"""
        <div style='background-color:#1c1f26;padding:20px;border-radius:10px'>
            <h4 style='margin:0;color:gray'>Current Price</h4>
            <h2 style='margin:0'>${current_price:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    color = "green" if change > 0 else "red"

    st.markdown(f"""
        <div style='background-color:#1c1f26;padding:20px;border-radius:10px'>
            <h4 style='margin:0;color:gray'>Change</h4>
            <h2 style='margin:0'>
                {change:.2f}
                <span style='float:right;font-size:16px;color:{color}'>
                    {change_percent:.2f}%
                </span>
            </h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style='background-color:#1c1f26;padding:20px;border-radius:10px'>
            <h4 style='margin:0;color:gray'>Volume</h4>
            <h2 style='margin:0'>{df['Volume'].iloc[-1]:,.0f}</h2>
        </div>
    """, unsafe_allow_html=True)


st.markdown(f"""
    <h2 style='margin-top:20px'>
        {result["name"]} 
        <span style='color:gray;font-size:18px'>({symbol.upper()})</span>
    </h2>
""", unsafe_allow_html=True)

st.subheader("📊 Price Trend")

fig = plot_stock(df)
st.plotly_chart(fig, use_container_width=True)


st.subheader("📉 Moving Average")

df["MA20"] = df["Close"].rolling(window=20).mean()

st.line_chart(df[["Close", "MA20"]])


if show_data:
    st.subheader("📄 Raw Data")
    st.dataframe(df)