import sys
import os
# 🛠️ PATH PATCH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle

# --- CONFIGURATION ---
st.set_page_config(
    page_title="UNIVERSAL MATRIX PROTOCOL",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cyberpunk Styling
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    div[data-testid="stMetricValue"] {color: #ff4444; font-family: 'Courier New', monospace;}
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle()

grok, deepseek, midas = load_agents()

# --- SIDEBAR: CALIBRATION CONTROLS ---
st.sidebar.title("🎛️ CALIBRATION")
st.sidebar.markdown("---")

# 1. SCAN CONTROLS
scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Lekki-Epe Expressway")

# 2. ECONOMIC VARIABLES (THE UPGRADE)
st.sidebar.markdown("---")
st.sidebar.subheader("⛽ ECONOMIC INPUTS")
fuel_price = st.sidebar.number_input("Current Fuel Price (₦/L)", value=1250, step=10)
# We removed the generic "Car Count" slider because the Physics Engine now calculates it automatically!

refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- MAIN DASHBOARD ---
st.title(":: UNIVERSAL MATRIX PROTOCOL ::")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚦 TRAFFIC SECTOR")
    traffic_loc = st.empty()
    traffic_load = st.empty()
    traffic_burn = st.empty()
    
with col2:
    st.markdown("### 💰 FINANCIAL SECTOR")
    finance_asset = st.empty()
    finance_price = st.empty()
    finance_panic = st.empty()

with col3:
    st.markdown("### 🗺️ LIVE TRACKING")
    map_display = st.empty()

# --- LIVE ENGINE ---
if st.button("🚀 ACTIVATE SYSTEM"):
    while True:
        # TRAFFIC LOGIC
        target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe Expressway"
        search_term = target if "lagos" in target.lower() else target + " Lagos"
        
        try:
            lat, lng, address = grok.find_coordinates(search_term)
            if lat:
                data = grok.get_traffic_data(lat, lng)
                
                # --- ✅ THE FIX IS HERE ---
                # We now call 'compute_precise_loss' instead of the old function
                metrics = deepseek.compute_precise_loss(
                    road_name=target, 
                    congestion=data['congestion'], 
                    fuel_price=fuel_price
                )
                
                # Update GUI
                traffic_loc.info(f"📍 {address}")
                
                # Show Car Count (Real Physics)
                traffic_load.metric("Congestion & Volume", 
                                  f"{int(data['congestion']*100)}%",
                                  delta=f"{metrics['cars_stuck']:,} Vehicles Stuck")
                
                # Show The Precise Burn Rate
                traffic_burn.metric(
                    "Total Economic Burn", 
                    f"₦ {metrics['total_burn']:,.0f}/hr", 
                    delta=f"Fuel Waste: ₦{metrics['fuel_loss']:,.0f}/hr",
                    delta_color="off"
                )
                
                map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
                map_display.map(map_data, zoom=12)
                
        except Exception as e:
            traffic_loc.error(f"Signal Lost: {e}")

        # FINANCE LOGIC (Unchanged)
        try:
            asset = "BTC-USD"
            market_data = midas.get_asset_health(asset)
            if market_data:
                finance_asset.info(f"🪙 {asset}")
                finance_price.metric("Price", f"${market_data['price']:,.2f}")
                
                panic_val = market_data['panic_score']
                label = "CRASH WARNING" if panic_val > 80 else "STABLE"
                finance_panic.metric("Panic Score", f"{panic_val:.1f}%", delta=label, delta_color="inverse")
        except:
            finance_asset.error("Market Offline")

        time.sleep(refresh_rate)