import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie # NEW ANIMATION TOOL
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor

# --- CONFIGURATION ---
st.set_page_config(page_title="OMNIX v2.0", page_icon="🧿", layout="wide", initial_sidebar_state="expanded")

# --- ULTRA-UI CSS (THE MAGIC) ---
st.markdown("""
    <style>
    /* 1. THE VOID BACKGROUND */
    .stApp { 
        background-color: #0e1117; 
        background-image: radial-gradient(#1c2331 1px, transparent 1px);
        background-size: 20px 20px;
        font-family: 'Courier New', monospace; 
    }

    /* 2. NEON TEXT GLOW */
    h1 {
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
        color: #fff !important;
        text-align: center;
        letter-spacing: 5px;
    }

    /* 3. HOVERING METRIC CARDS */
    div[data-testid="stMetric"] { 
        background: linear-gradient(145deg, #1a1a1a, #222222);
        border: 1px solid #333; 
        padding: 15px; 
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 255, 65, 0.3);
        border-color: #00ff41;
    }

    /* 4. SIDEBAR COMMAND CENTER */
    section[data-testid="stSidebar"] { 
        background-color: #161616;
        border-right: 2px solid #00ff41;
        box-shadow: 5px 0 15px rgba(0,0,0,0.5);
    }
    
    /* 5. PULSING LIVE DOT */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0, 255, 65, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 255, 65, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 255, 65, 0); }
    }
    .live-dot {
        height: 15px;
        width: 15px;
        background-color: #00ff41;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANIMATION LOADER ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Load Animations
lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json") # Cyber Brain
lottie_grid = load_lottieurl("https://lottie.host/90642935-773a-4934-8027-e4359d72491b/mC8j4iLq8u.json") # Power Grid (Generic)

# --- LOAD AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot = load_agents()

# --- COMMAND CENTER (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🧿 COMMAND CENTER")
    
    # ANIMATED BRAIN IN SIDEBAR
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="brain")
    
    st.markdown("---")
    
    scan_mode = st.radio("📡 MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
    target_input = st.text_input("🎯 TARGET", "Lekki-Epe")
    
    st.markdown("---")
    st.markdown("**💸 ECONOMIC PARAMS**")
    fuel_price = st.number_input("Fuel Price (₦/L)", value=1250, step=50)
    
    st.markdown("---")
    if st.button("⚠️ WIPE MEMORY"):
        st.cache_resource.clear()
        st.rerun()
        
    refresh_rate = st.slider("Refesh Rate (s)", 5, 60, 10)

# --- MAIN DASHBOARD ---
# Title with Animation
col_title, col_anim = st.columns([4, 1])
with col_title:
    st.markdown("# :: OMNIX PROTOCOL v2 ::")
with col_anim:
    st.markdown('<div class="live-dot"></div> <span style="color:#00ff41">SYSTEM ONLINE</span>', unsafe_allow_html=True)

# System Health Bar
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
    st.caption(":: SATELLITE UPLINK ESTABLISHED ::")
    map_display = st.empty()

with tab_finance:
    col1, col2 = st.columns(2)
    with col1: finance_price = st.empty()
    with col2: finance_panic = st.empty()

with tab_energy:
    col1, col2 = st.columns([3, 1])
    with col1: 
        energy_status = st.empty()
        energy_burn = st.empty()
    with col2:
        # Mini animation for power
        st.markdown("⚡ **GRID MONITOR**")

with tab_sim:
    st.markdown("### 🔮 REALITY SIMULATOR")
    sim_blackout = st.checkbox("Simulate Grid Collapse", key="sim_btn")
    sim_traffic = st.slider("Simulate Traffic Spike", 0.0, 1.0, 0.0)
    sim_chart = st.empty()

# --- LIVE ENGINE LOOP ---
if st.button("🚀 ACTIVATE PROTOCOL"):
    # Initial Toast Animation
    st.toast("Protocol Initialized...", icon="🧿")
    time.sleep(1)
    st.toast("Connecting to Lagos Grid...", icon="⚡")
    
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
            
            loss = deepseek.compute_precise_loss(target, t_data.get('congestion',0), fuel_price)
            traffic_header.markdown(f"### 📍 SECURED LINK: {addr}")
            traffic_load.metric("CONGESTION LEVEL", f"{int(t_data.get('congestion',0)*100)}%", delta=f"{loss['cars_stuck']:,} Cars Detected")
            traffic_burn.metric("ECONOMIC LOSS", f"₦ {loss['total_burn']:,.0f}/hr", delta="Wasted Fuel", delta_color="inverse")
            
            map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
            map_display.map(map_data, zoom=12, size=60, color="#00ff41")
        except Exception as e:
            traffic_header.error(f"Signal Lost: {e}")

        # 2. FINANCE & BIO
        try:
            news = news_bot.scan_network()
            real_panic = news['panic_factor'] * 100
            bio = bio_bot.get_vital_signs()
            b_data = bio 
            finance_price.metric("BTC PRICE", "$98,420") # Placeholder
            finance_panic.metric("SOCIAL PANIC", f"{real_panic:.0f}%", delta=news['headline'][:25]+"...")
            f_data = {'panic_score': real_panic}
        except: pass

        # 3. ENERGY
        try:
            status = "OFF" if sim_blackout else "ON" # Linked to Sim button for now
            e_data = {'status': 'GRID ACTIVE' if status == "ON" else 'BLACKOUT'}
            if status == "OFF":
                energy_status.metric("GRID STATUS", "🔴 COLLAPSE", delta="CRITICAL FAILURE")
            else:
                energy_status.metric("GRID STATUS", "🟢 ONLINE", delta="STABLE (100MW)")
        except: pass

        # 4. ORACLE
        try:
            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            
            # Dynamic Color for Health
            h_color = "normal" if health > 50 else "off"
            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", delta="Stable" if health > 50 else "Degrading", delta_color=h_color)
            
            # Animated Vector Display
            vector_display.info(f"⚡ MATRIX STATE: {current_vector}")

            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: impact[2] = -1.0
            if sim_traffic > 0: impact[0] = sim_traffic
            
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            future_df = pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"])
            sim_chart.area_chart(future_df, height=250, color=["#ff0000", "#00ff41", "#0000ff", "#ffff00"]) 
            
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(refresh_rate)