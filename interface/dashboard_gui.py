import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
from streamlit_lottie import st_lottie
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor

# --- CONFIGURATION ---
st.set_page_config(page_title="OMNIX v3.0", page_icon="🧿", layout="wide", initial_sidebar_state="expanded")

# --- ANIMATION LOADER ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# --- LOAD AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot = load_agents()

# --- COMMAND CENTER & THEME SWITCH ---
with st.sidebar:
    st.markdown("## 🧿 COMMAND CENTER")
    
    # 1. THEME TOGGLE
    theme_mode = st.toggle("☀️ LIGHT MODE", value=False)
    
    if lottie_ai:
        st_lottie(lottie_ai, height=120, key="brain")
    
    st.markdown("---")
    scan_mode = st.radio("📡 MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
    target_input = st.text_input("🎯 TARGET", "Lekki-Epe")
    st.markdown("---")
    fuel_price = st.number_input("Fuel Price (₦/L)", value=1250, step=50)
    st.markdown("---")
    if st.button("⚠️ WIPE MEMORY"):
        st.cache_resource.clear()
        st.rerun()
    refresh_rate = st.slider("Refesh Rate (s)", 5, 60, 10)

# --- DYNAMIC CSS ENGINE ---
# We define colors based on the toggle
if theme_mode:
    # LIGHT MODE COLORS
    bg_color = "#f0f2f6"
    text_color = "#000000"
    card_bg = "#ffffff"
    sidebar_bg = "#e0e0e0"
    accent = "#000000"
else:
    # DARK MODE COLORS (Default)
    bg_color = "#0e1117"
    text_color = "#00ff41"
    card_bg = "#1a1a1a"
    sidebar_bg = "#161616"
    accent = "#00ff41"

# INJECT CSS
st.markdown(f"""
    <style>
    /* 1. DYNAMIC BACKGROUND */
    .stApp {{ 
        background-color: {bg_color}; 
        color: {text_color};
        font-family: 'Courier New', monospace;
        transition: background-color 0.5s ease;
    }}

    /* 2. RAINBOW HOVER ANIMATION (The "Lovely" Part) */
    @keyframes chroma {{
        0% {{ border-color: #ff0000; box-shadow: 0 0 10px #ff0000; }}
        20% {{ border-color: #ff00ff; box-shadow: 0 0 10px #ff00ff; }}
        40% {{ border-color: #0000ff; box-shadow: 0 0 10px #0000ff; }}
        60% {{ border-color: #00ffff; box-shadow: 0 0 10px #00ffff; }}
        80% {{ border-color: #00ff00; box-shadow: 0 0 10px #00ff00; }}
        100% {{ border-color: #ffff00; box-shadow: 0 0 10px #ffff00; }}
    }}

    /* 3. METRIC CARDS */
    div[data-testid="stMetric"] {{ 
        background-color: {card_bg}; 
        border: 2px solid {accent}; 
        padding: 15px; 
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, border-color 0.5s ease;
    }}
    
    /* HOVER TRIGGER */
    div[data-testid="stMetric"]:hover {{
        transform: scale(1.05);
        animation: chroma 2s infinite linear; /* THIS MAKES IT CHANGE COLORS RANDOMLY */
        cursor: crosshair;
    }}

    /* 4. SIDEBAR */
    section[data-testid="stSidebar"] {{ 
        background-color: {sidebar_bg};
        border-right: 2px solid {accent};
    }}
    
    /* 5. TEXT COLORS */
    h1, h2, h3, p, label, .stMarkdown {{ color: {text_color} !important; }}
    div[data-testid="stMetricValue"] {{ color: {text_color} !important; font-size: 28px; }}
    div[data-testid="stMetricLabel"] {{ color: {accent} !important; }}

    /* 6. BUTTONS */
    .stButton button {{
        background-color: {card_bg};
        color: {text_color};
        border: 1px solid {accent};
        transition: all 0.3s ease;
    }}
    .stButton button:hover {{
        animation: chroma 0.5s infinite linear; /* FAST COLOR FLASH */
        color: {bg_color};
        background-color: {text_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
col_title, col_anim = st.columns([4, 1])
with col_title:
    st.markdown("# :: OMNIX PROTOCOL v3 ::")
with col_anim:
    status_color = "#000000" if theme_mode else "#00ff41"
    st.markdown(f'<b style="color:{status_color}; font-size:20px;">● SYSTEM ONLINE</b>', unsafe_allow_html=True)

# System Health
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
    sim_blackout = st.checkbox("Simulate Grid Collapse", key="sim_btn")
    sim_traffic = st.slider("Simulate Traffic Spike", 0.0, 1.0, 0.0)
    sim_chart = st.empty()

# --- LIVE LOOP ---
if st.button("🚀 ACTIVATE PROTOCOL"):
    # Toast Logic
    msgs = ["Connecting to Satellite...", "Handshake Secured...", "Decrypting Bio-Data..."]
    for msg in msgs:
        st.toast(msg, icon="🧿")
        time.sleep(0.5)

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
            traffic_header.info(f"📍 {addr}")
            traffic_load.metric("CONGESTION", f"{int(t_data.get('congestion',0)*100)}%", delta=f"{loss['cars_stuck']:,} Cars")
            traffic_burn.metric("MONEY BURN", f"₦ {loss['total_burn']:,.0f}/hr", delta="Lost Wealth", delta_color="inverse")
            
            map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
            map_display.map(map_data, zoom=12, size=60, color="#00ff41")
        except: pass

        # 2. FINANCE & BIO
        try:
            news = news_bot.scan_network()
            real_panic = news['panic_factor'] * 100
            bio = bio_bot.get_vital_signs()
            b_data = bio 
            finance_price.metric("BTC PRICE", "$98,420")
            finance_panic.metric("PANIC SCORE", f"{real_panic:.0f}%", delta=news['headline'][:20])
            f_data = {'panic_score': real_panic}
        except: pass

        # 3. ENERGY
        try:
            status = "OFF" if sim_blackout else "ON"
            e_data = {'status': 'GRID ACTIVE' if status == "ON" else 'BLACKOUT'}
            if status == "OFF":
                energy_status.metric("GRID STATUS", "🔴 COLLAPSE", delta="CRITICAL")
            else:
                energy_status.metric("GRID STATUS", "🟢 ONLINE", delta="STABLE")
        except: pass

        # 4. ORACLE
        try:
            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            
            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", delta="Live Pulse")
            vector_display.code(f"S(t) = {current_vector}")

            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: impact[2] = -1.0
            if sim_traffic > 0: impact[0] = sim_traffic
            
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            future_df = pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"])
            sim_chart.area_chart(future_df, height=250)
            
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(refresh_rate)