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
st.set_page_config(page_title="OMNIX PROTOCOL", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# --- CYBERPUNK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    div[data-testid="stMetric"] { background-color: #111; border: 1px solid #333; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot = load_agents()

# --- HEADER ---
st.title(":: OMNIX PROTOCOL ::")
col_health, col_status = st.columns([1, 3])
with col_health: system_health = st.empty()
with col_status: vector_display = st.empty()

# --- TABS ---
tab_main, tab_sim, tab_data = st.tabs(["👁️ DASHBOARD", "🕹️ SIMULATOR", "📊 RAW DATA"])

with tab_main:
    # A single view that combines MAP + MONEY + HEALTH (Better than separate tabs)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption(":: LIVE SURVEILLANCE ::")
        map_display = st.empty() # The Map lives here now
    with col2:
        st.caption(":: ECONOMIC IMPACT ::")
        traffic_burn = st.empty()
        bio_risk = st.empty()
        finance_panic = st.empty()

with tab_sim:
    st.markdown("### 🔮 PREDICT THE FUTURE")
    sim_blackout = st.checkbox("Simulate Grid Collapse")
    sim_traffic = st.slider("Simulate Traffic Spike", 0.0, 1.0, 0.0)
    sim_chart = st.empty()

# --- LIVE LOOP ---
if st.button("🚀 RELOAD SYSTEM"):
    while True:
        # Defaults (Fallback data so app NEVER crashes)
        t_data, f_data, e_data, b_data = {'congestion': 0}, {'panic_score': 0}, {'status': 'ON'}, {'aqi': 50}
        lat, lng = 6.5244, 3.3792 # Default Lagos
        
        # 1. TRAFFIC & MAP
        try:
            # Try to get real location
            target = "Lekki-Epe"
            found_lat, found_lng, _ = grok.find_coordinates(target + " Lagos")
            if found_lat: 
                lat, lng = found_lat, found_lng
                t_data = grok.get_traffic_data(lat, lng)
            
            # FORCE MAP DISPLAY (Even if API failed, use default lat/lng)
            map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
            map_display.map(map_data, zoom=11, size=50, color="#00ff41")
            
            # Compute Money Loss
            loss = deepseek.compute_precise_loss(target, t_data.get('congestion',0), 1250)
            traffic_burn.metric("MONEY LOST", f"₦ {loss['total_burn']:,.0f}/hr", delta="Burning Cash", delta_color="inverse")
            
        except Exception as e:
            st.error(f"Map Error: {e}")

        # 2. BIO & FINANCE
        try:
            # Biology
            bio = bio_bot.get_vital_signs()
            b_data = bio
            bio_risk.metric("AIR TOXICITY", bio['risk_level'], delta=f"AQI: {bio['aqi']}", delta_color="inverse")
            
            # Finance
            news = news_bot.scan_network()
            real_panic = news['panic_factor'] * 100
            finance_panic.metric("MARKET PANIC", f"{real_panic:.0f}%", delta=news['headline'][:15]+"...")
            f_data = {'panic_score': real_panic}
            
        except: pass

        # 3. ORACLE & SIMULATION
        try:
            # Sync Brain
            e_data = {'status': 'GRID ACTIVE'} # Default ON
            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            
            system_health.metric("CITY HEALTH", f"{health:.1f}%", delta="Live Pulse")
            vector_display.code(f"MATRIX STATE: {current_vector}")

            # Run Simulation
            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: impact[2] = -1.0
            if sim_traffic > 0: impact[0] = sim_traffic
            
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            future_df = pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"])
            sim_chart.line_chart(future_df, height=250)
            
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(10)