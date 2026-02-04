import streamlit as st
import time

def render(skills_bot):
    st.sidebar.markdown("---")
    st.sidebar.info("ℹ️ **DEMO KEYS:**\n\n🆔 **11111111111** (Pro)\n🆔 **22222222222** (Fresher)")
    
    st.markdown("# :: LASUSTECH CAREER ORACLE ::")
    st.caption("Linking Academic Input to Market Output")
    
    # 1. ADMIN UPLOAD SECTION (The Hook for the School)
    with st.expander("🔐 SCHOOL ADMIN: Upload Student Data (CSV)"):
        st.file_uploader("Upload GDP/Transcript Data", type=["csv"])
        st.info("Simulated: Connecting to LASUSTECH Registry API...")

    # 2. STUDENT SEARCH
    st.markdown("---")
    c1, c2 = st.columns([3, 1])
    nin_input = c1.text_input("🔍 ENTER STUDENT ID / NIN:", placeholder="Try 22222222222")
    search_btn = c2.button("🚀 ANALYZE PATH")

    if search_btn and nin_input:
        with st.spinner("Calculating Career Trajectory..."):
            identity = skills_bot.verify_identity(nin_input)
            
            if identity:
                # PROFILE
                st.success("✅ STUDENT RECORD FOUND")
                c1, c2, c3 = st.columns(3)
                c1.metric("NAME", identity['name'])
                c2.metric("SCHOOL", identity['school'])
                c3.metric("LEVEL", identity['level'])
                
                st.markdown(f"**🛠️ DETECTED SKILLS:** `{', '.join(identity['skills'])}`")
                
                # GAP ANALYSIS
                st.markdown("---")
                st.subheader("🎯 JOB MARKET FIT")
                
                matches = skills_bot.match_jobs(identity['skills'])
                
                for item in matches:
                    job = item['job']
                    score = item['score']
                    missing = item['missing']
                    
                    # CARD DESIGN
                    with st.container():
                        c1, c2 = st.columns([1, 3])
                        
                        # SCORE VISUAL
                        color = "green" if score > 70 else "red"
                        c1.markdown(f"<h1 style='color:{color}; text-align:center;'>{score}%</h1>", unsafe_allow_html=True)
                        c1.caption("HIRE PROBABILITY")
                        
                        # DETAILS
                        with c2:
                            st.markdown(f"### {job['role']} @ {job['company']}")
                            st.markdown(f"💰 **{job['salary']}** | 📍 Lagos")
                            
                            if score == 100:
                                st.balloons()
                                st.success("🌟 YOU ARE READY! APPLY NOW!")
                                st.markdown(f"[👉 CLICK TO APPLY]({job['link']})")
                            else:
                                # THE ADVICE ENGINE
                                st.warning(f"⚠️ **GAP DETECTED:** You are missing: `{', '.join(missing)}`")
                                st.info(f"🎓 **RECOMMENDED ACTION:** Take `{job['course_rec']}` next semester.")
                        
                        st.markdown("---")

            else:
                st.error("❌ Student ID Not Found")
