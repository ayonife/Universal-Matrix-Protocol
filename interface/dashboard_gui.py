import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
import numpy as np
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor

# --- CONFIGURATION ---
st.set_page_config(page_title="OMNIX PROTOCOL", page_icon="👁️", layout="wide", initial_sidebar_state="expanded")

# --- CYBERPUNK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    div[data-testid="stMetric"] { background-color: #111; border: 1px solid #333; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor()

# --- COMMAND CENTER ---
st.sidebar.title("🎛️ COMMAND CENTER")

# *** THE FIX: MEMORY WIPE BUTTON ***
if st.sidebar.button("⚠️ RESET BRAIN MEMORY"):
    st.cache_resource.clear()
    st.rerun()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot = load_agents()

scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Lekki-Epe")
manual_blackout = st.sidebar.checkbox("🚨 REPORT BLACKOUT")
st.sidebar.markdown("---")
fuel_price = st.sidebar.number_input("Fuel Price (₦/L)", value=1250)
refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- HEADER ---
st.title(":: OMNIX PROTOCOL ::")
col_health, col_status = st.columns([1, 3])
with col_health: system_health = st.empty()
with col_status: vector_display = st.empty()

# --- TABS ---
tab_traffic, tab_finance, tab_energy, tab_sim = st.tabs(["🚦 TRAFFIC", "💰 FINANCE", "⚡ POWER", "🕹️ SIM"])

with tab_traffic:
    traffic_header = st.empty()
    col1, col2 = st.columns(2)
    with col1: traffic_load = st.empty()
    with col2: traffic_burn = st.empty()
    st.caption(":: LIVE SATELLITE FEED ::")
    map_display = st.empty()

with tab_finance:
    col1, col2 = st.columns(2)
    with col1: finance_price = st.empty()
    with col2: finance_panic = st.empty()

with tab_energy:
    energy_status = st.empty()
    energy_burn = st.empty()

with tab_sim:
    st.markdown("### 🔮 REALITY SIMULATOR")
    sim_blackout = st.checkbox("Simulate Grid Collapse", value=manual_blackout, key="sim_btn")
    sim_traffic = st.slider("Simulate Traffic Spike", 0.0, 1.0, 0.0)
    sim_chart = st.empty()

# --- LIVE LOOP ---
if st.button("🚀 RELOAD SYSTEM"):
    while True:
        # Defaults
        t_data, f_data, e_data, b_data = {'congestion': 0}, {'panic_score': 0}, {'status': 'GRID ACTIVE'}, {'aqi': 50}
        lat, lng = 6.5244, 3.3792
        
        # 1. TRAFFIC
        try:
            target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe"
            found_lat, found_lng, addr = grok.find_coordinates(target + " Lagos")
            if found_lat: 
                lat, lng = found_lat, found_lng
                t_data = grok.get_traffic_data(lat, lng)
            
            # CARS & MONEY
            loss = deepseek.compute_precise_loss(target, t_data.get('congestion',0), fuel_price)
            traffic_header.info(f"📍 {addr}")
            traffic_load.metric("CONGESTION", f"{int(t_data.get('congestion',0)*100)}%", delta=f"{loss['cars_stuck']:,} Cars Stuck")
            traffic_burn.metric("MONEY BURN", f"₦ {loss['total_burn']:,.0f}/hr", delta="Wasted Fuel", delta_color="inverse")
            
            # MAP
            map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
            map_display.map(map_data, zoom=12, size=60, color="#00ff41")
        except Exception as e:
            traffic_header.error(f"Traffic Signal Lost: {e}")

        # 2. FINANCE & BIO
        try:
            news = news_bot.scan_network()
            real_panic = news['panic_factor'] * 100
            bio = bio_bot.get_vital_signs()
            b_data = bio 
            finance_price.metric("BTC Price", "LOADING...")
            finance_panic.metric("PANIC SCORE", f"{real_panic:.0f}%", delta=news['headline'][:20])
            f_data = {'panic_score': real_panic}
        except: pass

        # 3. ENERGY
        try:
            status = "OFF" if manual_blackout else "ON"
            e_data = {'status': 'GRID ACTIVE' if status == "ON" else 'BLACKOUT'}
            if status == "OFF":
                energy_status.metric("GRID STATUS", "🔴 COLLAPSE", delta="BLACKOUT")
            else:
                energy_status.metric("GRID STATUS", "🟢 STABLE", delta="POWER ON")
        except: pass

        # 4. ORACLE (BRAIN)
        try:
            # BACK TO 'sync_senses' (Server will recognize this once cache is cleared)
            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            
            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", delta="Live Pulse")
            vector_display.code(f"S(t) = {current_vector}")

            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: impact[2] = -1.0
            if sim_traffic > 0: impact[0] = sim_traffic
            
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            future_df = pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"])
            sim_chart.line_chart(future_df, height=200)
            
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(refresh_rate)