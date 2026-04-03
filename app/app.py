import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.data_preprocessing import load_data, preprocess_data
from src.feature_engineering import create_features
from src.model import train_model
from src.predict import make_prediction
from src.risk_analysis import get_risk_level
from src.heatmap import create_heatmap
from src.simulator import simulate_cases

# ------------------ UI STYLING ------------------
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# ------------------ THEME TOGGLE ------------------
st.sidebar.markdown("### 🎨 Theme")

theme = st.sidebar.radio(
    "Choose Mode",
    ["Light ☀️", "Dark 🌑"],
    key="theme_selector"   # 🔥 THIS FIXES IT
)


if theme == "Dark 🌑":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)



st.markdown("""
    <style>

    /* Page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Titles */
    h1 {
        font-size: 48px !important;
        color: #00ffe1;
        text-align: center;
        margin-bottom: 10px;
    }

    h2 {
        font-size: 32px !important;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    h3 {
        font-size: 24px !important;
        margin-top: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
    }

    /* Add spacing between sections */
    .element-container {
        margin-bottom: 25px;
    }

    </style>
""", unsafe_allow_html=True)



# ------------------ TITLE ------------------
title_color = "#00ffe1" if theme == "Dark 🌑" else "#007acc"

st.markdown(f"<h1 style='color:{title_color}'>🦠 EpiGuard AI</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Epidemic Spread Prediction & Risk Intelligence System</h3>", unsafe_allow_html=True)

st.info("📌 This dashboard predicts epidemic spread using AI-based time series modeling.")



# ------------------ LOAD DATA ------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "raw", "time_series_covid19_confirmed_global.csv")

df = load_data(file_path)
df = preprocess_data(df)


# ------------------ FEATURES ------------------
daily, growth, rolling = create_features(df)


# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Controls")
country = st.sidebar.selectbox("🌍 Select Country", df.columns)

series = df[country]



# ------------------ MODEL ------------------
model = train_model(series)
forecast = make_prediction(model)



# ------------------ METRICS ------------------
latest_cases = int(series.iloc[-1])
latest_daily = int(daily[country].iloc[-1])

col1, col2 = st.columns(2)

with col1:
    st.metric("📊 Total Cases", latest_cases)

with col2:
    st.metric("📈 Daily Cases", latest_daily)



# ------------------ RISK LEVEL ------------------
risk = get_risk_level(daily[country])

st.markdown("### ⚠️ Risk Level")

if "High" in risk:
    st.error(f"🚨 {risk} - Immediate attention needed!")
elif "Medium" in risk:
    st.warning(f"⚠️ {risk} - Situation should be monitored.")
else:
    st.success(f"✅ {risk} - Situation under control.")



# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Total Cases Over Time")
    st.line_chart(series, use_container_width=True)

with col2:
    st.subheader("📈 Daily New Cases Trend")
    st.area_chart(daily[country])

col3, col4 = st.columns(2)

with col3:
    st.subheader("📉 7-Day Rolling Average")
    st.line_chart(rolling[country])

with col4:
    st.subheader("🔮 AI Forecast (Next 30 Days)")

    forecast_df = forecast[['ds', 'yhat']].set_index('ds')

    st.line_chart(forecast_df)
    st.success("Prediction shows expected trend of future cases 📈")



# ------------------ HEATMAP ------------------

st.markdown("---")
st.subheader("🌍 Global Risk Heatmap")

heatmap_fig = create_heatmap(df, daily)
st.plotly_chart(heatmap_fig, use_container_width=True)

# ------------------ RAW DATA ------------------
if st.checkbox("Show Raw Data"):
    st.write(df.tail())



# ------------------ WHAT-IF SIMULATOR ------------------

st.markdown("---")
st.subheader("⚙️ What-if Simulator")

st.write("Adjust spread factor to simulate different scenarios")

factor = st.slider(
    "Spread Factor (0.5 = control, 1 = normal, 2 = outbreak)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

simulated_series = simulate_cases(series, factor)

st.subheader("📊 Simulated Cases")
st.line_chart(simulated_series)


# Insight message
if factor > 1.5:
    st.error("🚨 High spread scenario! Cases may rise rapidly.")
elif factor < 0.8:
    st.success("✅ Controlled scenario. Spread is reduced.")
else:
    st.info("ℹ️ Moderate scenario.")