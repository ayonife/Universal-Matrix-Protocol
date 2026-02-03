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
from core.energy import EnergyGrid  # <--- NEW AGENT

# --- CONFIGURATION ---
st.set_page_config(page_title="UNIVERSAL MATRIX PROTOCOL", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    div[data-testid="stMetricValue"] {color: #ff4444; font-family: 'Courier New', monospace;}
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid()

grok, deepseek, midas, nepa = load_agents() # 'nepa' is our new agent

# --- SIDEBAR ---
st.sidebar.title("🎛️ CALIBRATION")
scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Lekki-Epe Expressway")
fuel_price = st.sidebar.number_input("Fuel Price (₦/L)", value=1250)
refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- MAIN DASHBOARD ---
st.title(":: UNIVERSAL MATRIX PROTOCOL ::")

# Create 4 Columns now (Traffic, Finance, Energy, Map)
col1, col2, col3 = st.columns(3)
col_energy, col_map = st.columns([1, 2]) # Energy gets 1/3, Map gets 2/3 of bottom row

# ROW 1 CONTAINERS
with col1:
    st.markdown("### 🚦 TRAFFIC")
    traffic_load = st.empty()
    traffic_burn = st.empty()
    
with col2:
    st.markdown("### 💰 FINANCE")
    finance_price = st.empty()
    finance_panic = st.empty()

with col3:
    st.markdown("### ⚡ POWER GRID")
    energy_status = st.empty()
    energy_burn = st.empty()

# ROW 2 CONTAINER
with col_map:
    map_display = st.empty()

# --- LIVE ENGINE ---
if st.button("🚀 ACTIVATE SYSTEM"):
    while True:
        # 1. TRAFFIC
        target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe Expressway"
        search_term = target if "lagos" in target.lower() else target + " Lagos"
        try:
            lat, lng, addr = grok.find_coordinates(search_term)
            if lat:
                data = grok.get_traffic_data(lat, lng)
                metrics = deepseek.compute_precise_loss(target, data['congestion'], fuel_price)
                
                traffic_load.metric("Congestion", f"{int(data['congestion']*100)}%", delta=f"{metrics['cars_stuck']:,} Cars")
                traffic_burn.metric("Traffc Burn", f"₦ {metrics['total_burn']:,.0f}/hr", delta_color="inverse")
                
                map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
                map_display.map(map_data, zoom=12)
        except: pass

        # 2. FINANCE
        try:
            market = midas.get_asset_health("BTC-USD")
            finance_price.metric("BTC Price", f"${market['price']:,.0f}")
            finance_panic.metric("Panic Score", f"{market['panic_score']:.1f}%", delta="CRASH WARNING" if market['panic_score']>80 else "STABLE")
        except: pass

        # 3. ENERGY (NEW)
        try:
            status = nepa.check_grid_status() # Checks if Light is ON or OFF
            power_data = nepa.calculate_burn_rate(status)
            
            # If Blackout, show Red. If Light, show Green.
            color = "inverse" if status == "OFF" else "normal"
            
            energy_status.metric("Grid Status", power_data['status'])
            energy_burn.metric(
                "Generator Burn Rate", 
                f"₦ {power_data['burn_rate']:,.0f}/hr",
                delta=f"{power_data['generators_on']:,} Gens Active",
                delta_color=color
            )
        except Exception as e:
            energy_status.error(f"Grid Error: {e}")

        time.sleep(refresh_rate)