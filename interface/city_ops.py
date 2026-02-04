import streamlit as st
import pandas as pd
import time

def render(grok, deepseek, midas, nepa, oracle, news_bot, bio_bot):
    st.sidebar.markdown("---")
    st.sidebar.markdown("📡 **LIVE SURVEILLANCE**")
    
    # REAL SEARCH BAR (Type anything!)
    target_input = st.sidebar.text_input("SEARCH ZONE (e.g. Oshodi):", "Lekki-Epe")
    
    if st.sidebar.button("🛰️ RELOCATE SATELLITE"):
        with st.spinner(f"Re-aligning Satellite to {target_input}..."):
            time.sleep(1) # Dramatic pause

    st.sidebar.markdown("🚨 **THRESHOLDS**")
    alert_speed = st.sidebar.slider("Traffic Speed Alert (km/h)", 0, 60, 10)

    # HEADER
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown(f"# :: OPS CENTER: {target_input.upper()} ::")
    with c2: st.markdown("🟢 **ONLINE**")

    tab_traffic, tab_finance = st.tabs(["🚦 TRAFFIC & MAPS", "💰 MARKET INTEL"])

    with tab_traffic:
        try:
            # REAL GEOCODING
            found_lat, found_lng, addr = grok.find_coordinates(target_input + " Lagos")
            
            if found_lat:
                # Get Traffic Data
                t_data = grok.get_traffic_data(found_lat, found_lng)
                cong = t_data.get('congestion', 0)
                
                # Real Math
                est_speed = max(5, 80 * (1 - cong))
                est_delay = int(cong * 60)
                loss = deepseek.compute_precise_loss(target_input, cong, 1250)

                # 4-Column Metric
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("SPEED", f"{int(est_speed)} km/h", "Slow" if est_speed < 20 else "Fast")
                c2.metric("DELAY", f"+{est_delay} min", "Traffic" if est_delay > 10 else "Clear")
                c3.metric("CONGESTION", f"{int(cong*100)}%", "Density")
                c4.metric("MONEY LOST", f"₦ {loss['total_burn']:,.0f}", "/hr")

                # THE REAL MAP
                st.map(pd.DataFrame({'lat': [found_lat], 'lon': [found_lng]}), zoom=13)
            else:
                st.error("⚠️ Location Not Found. Try a major area name.")
        except Exception as e:
            st.error(f"Satellite Uplink Error: {e}")

    with tab_finance:
        st.markdown("### 📰 REAL-TIME NEWS WIRE")
        news = news_bot.scan_network()
        for story in news['stories']:
             st.markdown(f"> 👉 **[{story['source']}]** [{story['title']}]({story['link']})")
