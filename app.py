import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. Enhanced CSS for High Visibility & 3D Effects
st.markdown("""
<style>
.main { background-color: #0b0e14; color: #ffffff; }
.phase-card { 
    background-color: #1a1e26; 
    padding: 30px; 
    border-radius: 20px; 
    border: 1px solid #3d4446; 
    text-align: center;
    box-shadow: inset 2px 2px 5px #000, 8px 8px 20px #000; 
    min-height: 280px; 
    transition: all 0.3s ease;
}
/* Making Text Bold and Ultra-Visible */
.phase-title { 
    color: #ffffff; 
    font-size: 22px; 
    font-weight: 900; 
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px #000;
}
.status-text { 
    color: #00ff00; 
    font-size: 16px; 
    font-weight: 700; 
    margin-top: 15px;
    text-shadow: 1px 1px 2px #000;
}
.status-text-orange { 
    color: #ffaa00; 
    font-size: 16px; 
    font-weight: 700; 
    margin-top: 15px;
    text-shadow: 1px 1px 2px #000;
}

.icon-3d { filter: drop-shadow(5px 5px 8px #000); margin-bottom: 15px; }

/* Animations */
@keyframes pulse-green { 0% { box-shadow: 0 0 35px #00ff00; border-color: #00ff00; } 50% { border-color: #3d4446; } }
@keyframes pulse-orange { 0% { box-shadow: 0 0 35px #ffaa00; border-color: #ffaa00; } 50% { border-color: #3d4446; } }
.active-green { animation: pulse-green 1s infinite !important; border: 2px solid #00ff00 !important; }
.active-orange { animation: pulse-orange 1s infinite !important; border: 2px solid #ffaa00 !important; }

.led { height: 14px; width: 14px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
.led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
.led-orange { background-color: #ffaa00; box-shadow: 0 0 10px #ffaa00; }
.led-off { background-color: #333; }
</style>
""", unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin : Your Smart Assistant")

# 3. Session State Management
if 'step' not in st.session_state: st.session_state.step = 0

with st.sidebar:
    st.header("⚙️ AI Control Panel")
    tds = st.slider("Feed Water Salinity (ppm)", 10000, 60000, 45000)
    if st.button("🚀 Launch Ion Separation Cycle"): st.session_state.step = 1
    if st.button("🔄 Reset System"): 
        st.session_state.step = 0
        st.rerun()

# 4. Logic & Technical Parameters
voltage, freq, status_msg = "0.00 V", "0 Hz", "STANDBY"
if st.session_state.step == 1: 
    voltage, freq, status_msg = "0.45 V", "10 Hz", "WATER INTAKE ACTIVE"
elif st.session_state.step == 2: 
    voltage, freq, status_msg = "0.90 V", "20 Hz", "GYPSUM (Ca/SO4) TREATMENT"
elif st.session_state.step == 3: 
    voltage, freq, status_msg = "1.35 V", "65 Hz", "SALT (Na/Cl) TREATMENT"
elif st.session_state.step == 4: 
    voltage, freq, status_msg = "1.15 V", "45 Hz", "FINAL HARVESTING"

# 5. Metrics Bar
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Operating Pressure", f"{tds * 0.025:.2f} bar")
with c2: st.metric("AI Voltage (V)", voltage)
with c3: st.metric("Pulse Frequency", freq)
with c4: st.metric("System Status", status_msg)

st.write("---")

# 6. Sequential Display
p1, p2, p3 = st.columns(3)

# PHASE 1
with p1:
    act = "active-green" if st.session_state.step == 1 else ""
    led = "led-green" if st.session_state.step >= 1 else "led-off"
    st.markdown(f"""
        <div class="phase-card {act}">
            <div class="led {led}"></div>
            <div class="phase-title">PHASE 1: INTAKE</div>
            <img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="50">
            <div class="status-text">{"FEEDING WATER..." if st.session_state.step==1 else "INTAKE READY" if st.session_state.step > 1 else "IDLE"}</div>
        </div>
    """, unsafe_allow_html=True)

# PHASE 2 (Two-Stage Treatment: Gypsum then Salt)
with p2:
    act = "active-orange" if (st.session_state.step == 2 or st.session_state.step == 3) else ""
    led = "led-orange" if (st.session_state.step >= 2) else "led-off"
    
    # Sub-logic for text color and message in Phase 2
    if st.session_state.step == 2:
        msg = "GYPSUM EXTRACTION"
    elif st.session_state.step == 3:
        msg = "NaCl CRYSTALLIZATION"
    elif st.session_state.step > 3:
        msg = "TREATMENT COMPLETE"
    else:
        msg = "AWAITING FLOW"

    st.markdown(f"""
        <div class="phase-card {act}">
            <div class="led {led}"></div>
            <div class="phase-title">PHASE 2: AI TREATMENT</div>
            <img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="50">
            <div class="status-text-orange">{msg}</div>
        </div>
    """, unsafe_allow_html=True)

# PHASE 3
with p3:
    act = "active-green" if st.session_state.step == 4 else ""
    led = "led-green" if st.session_state.step >= 4 else "led-off"
    st.markdown(f"""
        <div class="phase-card {act}">
            <div class="led {led}"></div>
            <div class="phase-title">PHASE 3: HARVESTING</div>
            <img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="50">
            <div class="status-text">{"COLLECTING MINERALS" if st.session_state.step==4 else "PRODUCTION READY" if st.session_state.step >= 4 else "AWAITING OUTPUT"}</div>
        </div>
    """, unsafe_allow_html=True)

# 7. Auto-Step Controller
if 1 <= st.session_state.step < 4:
    time.sleep(4.5) # Increased time for visual impact and explanation
    st.session_state.step += 1
    st.rerun()
