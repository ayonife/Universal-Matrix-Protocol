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
st.set_page_config(page_title="OMNIX v3.2", page_icon="🧿", layout="wide", initial_sidebar_state="expanded")

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

# --- COMMAND CENTER ---
with st.sidebar:
    st.markdown("## 🧿 COMMAND CENTER")
    theme_mode = st.toggle("☀️ LIGHT MODE", value=False)
    if lottie_ai: st_lottie(lottie_ai, height=120, key="brain")
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

# --- DYNAMIC CSS ---
if theme_mode:
    bg_color, text_color, card_bg, accent = "#f0f2f6", "#000000", "#ffffff", "#000000"
    link_color = "#0000EE"
else:
    bg_color, text_color, card_bg, accent = "#0e1117", "#00ff41", "#1a1a1a", "#00ff41"
    link_color = "#00ff41"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Courier New', monospace; transition: background-color 0.5s ease; }}
    
    @keyframes chroma {{
        0% {{ border-color: #ff0000; box-shadow: 0 0 10px #ff0000; }}
        50% {{ border-color: #00ff00; box-shadow: 0 0 10px #00ff00; }}
        100% {{ border-color: #0000ff; box-shadow: 0 0 10px #0000ff; }}
    }}
    
    div[data-testid="stMetric"] {{ 
        background-color: {card_bg}; border: 2px solid {accent}; padding: 10px; border-radius: 8px;
        transition: transform 0.2s ease;
    }}
    div[data-testid="stMetric"]:hover {{ transform: scale(1.05); animation: chroma 2s infinite linear; }}
    
    h1, h2, h3, p, label, .stMarkdown, div[data-testid="stMetricValue"] {{ color: {text_color} !important; }}
    div[data-testid="stMetricLabel"] {{ color: {accent} !important; opacity: 0.8; }}
    a {{ text-decoration: none; color: {link_color} !important; font-weight: bold; border-bottom: 1px dotted {accent}; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_title, col_anim = st.columns([4, 1])
with col_title: st.markdown("# :: OMNIX PROTOCOL v3.2 ::")
with col_anim:
    status_color = "#000000" if theme_mode else "#00ff41"
    st.markdown(f'<b style="color:{status_color};">● ONLINE</b>', unsafe_allow_html=True)

col_health, col_status = st.columns([1, 3])
with col_health: system_health = st.empty()
with col_status: vector_display = st.empty()

# --- TABS ---
tab_traffic, tab_finance, tab_energy, tab_sim = st.tabs(["🚦 TRAFFIC", "💰 FINANCE", "⚡ POWER", "🕹️ SIM"])

with tab_traffic:
    traffic_header = st.empty()
    # NEW LAYOUT: 4 Columns for MAXIMUM PRECISION
    c1, c2, c3, c4 = st.columns(4)
    with c1: traffic_speed = st.empty()  # NEW
    with c2: traffic_delay = st.empty()  # NEW
    with c3: traffic_load = st.empty()   # Congestion
    with c4: traffic_burn = st.empty()   # Money
    map_display = st.empty()

with tab_finance:
    col1, col2 = st.columns(2)
    with col1: finance_price = st.empty()
    with col2: finance_panic = st.empty()
    st.markdown("---")
    news_feed_display = st.empty()

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
    st.toast("Acquiring Satellite Precision...", icon="📡")
    
    while True:
        # Defaults
        t_data, f_data, e_data, b_data = {'congestion': 0}, {'panic_score': 0}, {'status': 'GRID ACTIVE'}, {'aqi': 50}
        lat, lng = 6.5244, 3.3792
        
        # 1. TRAFFIC (PRECISION MODE)
        try:
            target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe"
            found_lat, found_lng, addr = grok.find_coordinates(target + " Lagos")
            if found_lat: 
                lat, lng = found_lat, found_lng
                t_data = grok.get_traffic_data(lat, lng)
            
            # Extract Precision Data (Simulated for Demo if API misses, but ready for real data)
            cong = t_data.get('congestion', 0)
            
            # TomTom Logic: If congestion is high, speed is low
            est_speed = max(5, 80 * (1 - cong)) # Est 80km/h free flow
            est_delay = int(cong * 60) # Minutes of delay
            
            loss = deepseek.compute_precise_loss(target, cong, fuel_price)
            
            traffic_header.info(f"📍 {addr}")
            
            # THE NEW PRECISE METRICS
            traffic_speed.metric("AVG SPEED", f"{int(est_speed)} km/h", delta="-Slow" if cong > 0.3 else "Fast", delta_color="inverse")
            traffic_delay.metric("DELAY", f"+{est_delay} min", delta="Time Lost", delta_color="inverse")
            traffic_load.metric("CONGESTION", f"{int(cong*100)}%", delta=f"~{loss['cars_stuck']} Est. Cars")
            traffic_burn.metric("MONEY BURN", f"₦ {loss['total_burn']:,.0f}/hr", delta="Wasted Fuel", delta_color="inverse")
            
            map_display.map(pd.DataFrame({'lat': [lat], 'lon': [lng]}), zoom=12, size=60, color="#00ff41")
        except: pass

        # 2. FINANCE & NEWS
        try:
            news_data = news_bot.scan_network()
            real_panic = news_data['panic_factor'] * 100
            stories = news_data['stories']
            bio = bio_bot.get_vital_signs()
            b_data = bio 
            finance_price.metric("BTC PRICE", "$98,420")
            finance_panic.metric("SOCIAL PANIC", f"{real_panic:.0f}%", delta="Live Sentiment")
            
            news_html = ""
            for story in stories:
                news_html += f"👉 **[{story['source']}]** [{story['title']}]({story['link']})\n\n"
            news_feed_display.markdown(news_html)
            f_data = {'panic_score': real_panic}
        except: pass

        # 3. ENERGY & ORACLE
        try:
            status = "OFF" if sim_blackout else "ON"
            e_data = {'status': 'GRID ACTIVE' if status == "ON" else 'BLACKOUT'}
            if status == "OFF": energy_status.metric("GRID STATUS", "🔴 COLLAPSE", delta="CRITICAL")
            else: energy_status.metric("GRID STATUS", "🟢 ONLINE", delta="STABLE")

            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", delta="Live Pulse")
            vector_display.code(f"S(t) = {current_vector}")

            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: impact[2] = -1.0
            if sim_traffic > 0: impact[0] = sim_traffic
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            sim_chart.area_chart(pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"]), height=250)
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(refresh_rate)