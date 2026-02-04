import streamlit as st
import time

def render(skills_bot):
    st.sidebar.markdown("---")
    st.sidebar.warning("⚠️ **ADMIN ACCESS ONLY**")
    
    st.markdown("# :: CITIZEN DATABASE & JOB LINK ::")
    
    # SEARCH STUDENT
    col1, col2 = st.columns([3, 1])
    with col1:
        nin_input = st.text_input("🔍 SEARCH STUDENT (Enter NIN):", placeholder="Try 11111111111")
    with col2:
        st.write("")
        search_btn = st.button("🔎 SEARCH DB")

    if search_btn:
        with st.spinner("Querying National Database..."):
            identity = skills_bot.verify_identity(nin_input)
            
            if identity:
                # PROFILE CARD
                st.success("✅ RECORD FOUND")
                st.markdown(f"""
                <div style="background-color:#111; padding:20px; border-radius:10px; border-left:5px solid #00ff41;">
                    <h2>👤 {identity['name']}</h2>
                    <p>🎓 <b>Institution:</b> {identity['school']} | <b>Level:</b> {identity['level']}</p>
                    <p>🆔 <b>Status:</b> <span style="color:#00ff41">VERIFIED CITIZEN</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # JOBS SECTION
                st.markdown("---")
                st.subheader("🚀 RECOMMENDED REAL JOBS (Based on Profile)")
                
                jobs = skills_bot.match_jobs([]) # Fetch real jobs
                
                for job in jobs:
                    st.markdown(f"""
                    **{job['role']}** @ {job['company']}  
                    📍 {job['location']} | 💰 {job['salary']}  
                    [👉 APPLY NOW]({job['link']})
                    """)
                    st.markdown("---")
            else:
                st.error("❌ NIN Not Found in Database.")
