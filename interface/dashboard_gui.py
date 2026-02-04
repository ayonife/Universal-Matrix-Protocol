import sys
import os
import streamlit as st
import requests
from streamlit_lottie import st_lottie

sys.path.append(os.path.dirname(__file__))
import city_ops
import citizen_portal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor
from core.skills_agent import SkillsAgent

st.set_page_config(page_title="OMNIX v6.0 (Realism)", page_icon="🧿", layout="wide")

@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor(), SkillsAgent()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot, skills_bot = load_agents()

# *** THE CHROMA-SHIFT ANIMATION ***
st.markdown("""
    <style>
    /* ANIMATED BACKGROUND */
    @keyframes colorChange {
        0% { background-color: #000000; }
        25% { background-color: #0a0a20; }
        50% { background-color: #001000; }
        75% { background-color: #100000; }
        100% { background-color: #000000; }
    }
    
    .stApp {
        animation: colorChange 20s infinite alternate;
        color: #e0e0e0;
        font-family: 'Courier New';
    }

    /* NEON BORDERS */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 65, 0.5);
        border-radius: 8px;
        backdrop-filter: blur(5px);
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🧿 OMNIX")
    app_mode = st.radio("SYSTEM ACCESS:", ["🏙️ OPS CENTER", "👤 CITIZEN DB"])
    
    def load_lottieurl(url):
        try: return requests.get(url).json()
        except: return None
    lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
    if lottie: st_lottie(lottie, height=80)

if app_mode == "🏙️ OPS CENTER":
    city_ops.render(grok, deepseek, midas, nepa, oracle, news_bot, bio_bot)
else:
    citizen_portal.render(skills_bot)
