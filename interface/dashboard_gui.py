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
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent

# --- CONFIGURATION ---
st.set_page_config(
    page_title="OMNIX PROTOCOL",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CYBERPUNK HUD STYLING ---
st.markdown("""
    <style>
    /* 1. MAIN TERMINAL BACKGROUND */
    .stApp {
        background-color: #050505; /* Void Black */
        color: #00ff41; /* Matrix Green Text */
        font-family: 'Courier New', monospace;
    }

    /* 2. GLOWING METRIC BOXES */
    div[data-testid="stMetric"] {
        background-color: #111;
        border: 1px solid #333;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); /* Green Glow */
    }

    /* 3. TEXT COLORS FOR METRICS */
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        color: #ffffff;
        text-shadow: 0 0 5px #ffffff;
    }

    div[data-testid="stMetricLabel"] {
        color: #00ff41; /* Green Labels */
        font-weight: bold;
    }

    /* 4. RED ALERT STYLE (For Panic/Blackouts) */
    .css-1wivap2 {
        /* This targets negative deltas, turning them Neon Red */
        color: #ff0055 !important;
        text-shadow: 0 0 10px #ff0055;
    }

    /* 5. TABS AS PHYSICAL BUTTONS */
    button[data-baseweb="tab"] {
        background-color: #1a1a1a;
        color: #00ff41;
        border: 1px solid #00ff41;
        margin: 0 5px;
        border-radius: 3px;
    }
    button[data-baseweb="tab"]:hover {
        background-color: #00ff41;
        color: #000;
        box-shadow: 0 0 15px #00ff41;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent()

grok, deepseek, midas, nepa, oracle, news_bot = load_agents()

# --- SIDEBAR CONTROL ---
st.sidebar.title("🎛️ COMMAND CENTER")
scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Ikorodu")
st.sidebar.markdown("---")
manual_blackout = st.sidebar.checkbox("🚨 REPORT BLACKOUT", value=False)
st.sidebar.markdown("---")
fuel_price = st.sidebar.number_input("Fuel Price (₦/L)", value=1250)
refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- MAIN DASHBOARD (MOBILE TABS) ---
st.title(":: OMNIX PROTOCOL ::")

# --- ENTITY STATUS HEADER ---
col_health, col_status = st.columns([1, 4])
with col_health:
    system_health = st.empty()
with col_status:
    st.caption(":: UNIVERSAL STATE VECTOR S(t) ::")
    vector_display = st.empty()

# 📱 TABS
tab_traffic, tab_finance, tab_energy, tab_map = st.tabs(["🚦 TRAFFIC", "💰 FINANCE", "⚡ POWER", "🗺️ MAP"])

with tab_traffic:
    st.markdown("### TRAFFIC SECTOR")
    traffic_header = st.empty()
    traffic_load = st.empty()
    traffic_burn = st.empty()

with tab_finance:
    st.markdown("### FINANCIAL SECTOR")
    finance_price = st.empty()
    finance_panic = st.empty()

with tab_energy:
    st.markdown("### POWER GRID")
    energy_status = st.empty()
    energy_burn = st.empty()

with tab_map:
    st.markdown("### LIVE SATELLITE")
    map_display = st.empty()
    st.markdown("---")
    st.caption(":: ORACLE PREDICTION (T+12 HOURS) ::")
    prediction_chart = st.empty() # Placeholder for the future graph

# --- LIVE ENGINE ---
if st.button("🚀 ACTIVATE SYSTEM"):
    status_msg = st.empty()
    status_msg.markdown("`SYSTEM INITIALIZED. SCANNING...`")

    while True:
        # Initialize defaults
        t_data = {'congestion': 0}
        f_data = {'panic_score': 0}
        e_data = {'status': 'GRID ACTIVE'}
        
        # 1. TRAFFIC LOGIC
        target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe Expressway"
        search_term = target if "lagos" in target.lower() else target + " Lagos"

        try:
            lat, lng, addr = grok.find_coordinates(search_term)
            if lat:
                t_data = grok.get_traffic_data(lat, lng)
                metrics = deepseek.compute_precise_loss(target, t_data['congestion'], fuel_price)

                traffic_header.info(f"📍 {addr}")
                traffic_load.metric("Congestion", f"{int(t_data['congestion']*100)}%", delta=f"{metrics['cars_stuck']:,} Cars")
                traffic_burn.metric("Traffc Burn", f"₦ {metrics['total_burn']:,.0f}/hr", delta_color="inverse")

                map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
                map_display.map(map_data, zoom=12)
        except Exception as e:
            traffic_header.error(f"Signal Lost: {e}")

        # 2. REAL INTELLIGENCE (NEWS + FINANCE)
        try:
            # A. Get Bitcoin Price
            market = midas.get_asset_health("BTC-USD")
            
            # B. Get Real News & Panic
            news_data = news_bot.scan_network()
            real_panic = news_data['panic_factor'] * 100 
            
            # C. Update Finance Tab
            finance_price.metric("BTC Price", f"${market['price']:,.0f}")
            finance_panic.metric(
                "Panic Score", 
                f"{real_panic:.0f}%", 
                delta=f"NEWS: {news_data['headline'][:20]}..." 
            )
            
            if real_panic > 50:
                st.toast(f"📰 BREAKING: {news_data['headline']}")
            
            f_data = {'panic_score': real_panic}
            
        except Exception as e:
            finance_price.warning(f"Intel Error: {e}")

        # 3. ENERGY LOGIC
        try:
            status = "OFF" if manual_blackout else "ON"
            power_data = nepa.calculate_burn_rate(status)
            e_data = {'status': 'GRID ACTIVE' if status == "ON" else 'BLACKOUT'}

            if status == "OFF":
                energy_status.metric("Grid Status", "🔴 SYSTEM COLLAPSE", delta="BLACKOUT DETECTED", delta_color="inverse")
                energy_burn.metric("Diesel Burn Rate", f"₦ {power_data['burn_rate']:,.0f}/hr", delta=f"{power_data['generators_on']:,} Gens", delta_color="inverse")
            else:
                energy_status.metric("Grid Status", "🟢 GRID STABLE", delta="POWER RESTORED")
                energy_burn.metric("Diesel Burn Rate", "₦ 0 / hr", delta="Generators Offline")
        except:
            pass

        # 4. ORACLE SYNC (THE BRAIN)
        try:
            current_vector = oracle.sync_senses(t_data, f_data, e_data)
            health = oracle.get_system_health()

            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", 
                               delta="STABLE" if health > 70 else "CRITICAL")
            
            vector_display.code(f"S(t) = [TRAFFIC: {current_vector[0]:.2f} | PANIC: {current_vector[1]:.2f} | ENERGY: {current_vector[2]:.2f}]")

            # Run Simulation
            future_states = oracle.simulate_future(steps=12)
            future_df = pd.DataFrame(future_states, columns=["Traffic", "Panic", "Grid Stability"])
            future_df.index.name = "Hours from Now"
            
            # Update Chart in Map Tab
            prediction_chart.line_chart(future_df, height=200)

        except Exception as e:
            st.error(f"Oracle Failure: {e}")

        time.sleep(refresh_rate)