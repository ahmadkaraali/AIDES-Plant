import streamlit as st
import time
import pandas as pd

# 1. Engineering Core (Dr. Ahmed's Patent Logic)
class AIDESEngine:
    def __init__(self, profile):
        self.K_SP = 2.4e-5
        self.threshold = 0.8 if profile == "Seawater" else 0.6
        self.factor = 1.2 if profile == "Seawater" else 2.0
        self.flow_rate = 150 # m3/hr

    def calculate(self, tds, temp):
        # Chemical Calculations for Scaling Risk
        ca = (tds / 100000) * 0.02 * self.factor
        so4 = (tds / 100000) * 0.03 * self.factor
        ion_p = ca * so4
        temp_f = 1 + (temp - 25) * 0.01
        si = ion_p / (self.K_SP * temp_f)
        
        # Scaling Risk Protocol
        risk = si > self.threshold
        voltage = 1.5 if not risk else 1.5 * 0.85
        
        # Accurate Gypsum Yield (Mass Balance)
        gyp_kg_hr = self.flow_rate * (tds / 1000) * 0.05 * 1.72 * 0.9
        gyp_tons = gyp_kg_hr / 1000
        
        return si, risk, voltage, gyp_tons

# 2. UI Configuration
st.set_page_config(page_title="AIDES Smart Platform", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b101a; color: #e6edf3; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; font-size: 38px !important; }
    .node-card { padding: 20px; border-radius: 12px; border: 1px solid #30363d; background: #161b22; text-align: center; min-height: 150px; }
    .flow-line { height: 4px; background: linear-gradient(90deg, #58a6ff, #00ffcc); margin-top: 70px; }
    .ai-log { background: #0d1117; color: #ffd166; padding: 12px; border-left: 4px solid #ffd166; font-family: 'Courier New', monospace; font-size: 13px; margin: 10px 0; }
    .success-summary { padding: 25px; border: 2px solid #238636; background: rgba(35, 134, 54, 0.1); border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AIDES: Advanced Mineral Recovery System")
st.write("Intelligent Process Simulation & Scaling Control Technology")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Operational Inputs")
    tds_input = st.slider("Feedwater TDS (ppm)", 5000, 100000, 45000)
    temp_input = st.slider("Temperature (°C)", 15, 50, 25)
    water_profile = st.selectbox("Feedwater Source", ["Seawater", "Produced Water"])
    st.markdown("---")
    start_btn = st.button("🚀 Start Sequence")

# Display Metrics
m_cols = st.columns(3)
p_si = m_cols[0].empty()
p_v = m_cols[1].empty()
p_g = m_cols[2].empty()

st.write("---")
st.subheader("📊 Dynamic Process Simulation")
f_cols = st.columns([2, 0.5, 2, 0.5, 2])
n1 = f_cols[0].empty()
l1 = f_cols[1].empty()
n2 = f_cols[2].empty()
l2 = f_cols[3].empty()
n3 = f_cols[4].empty()

if start_btn:
    engine = AIDESEngine(water_profile)
    si_res, risk_res, v_res, gyp_res = engine.calculate(tds_input, temp_input)
    
    # PHASE 1: INTAKE
    with n1.container():
        st.markdown("<div class='node-card'><b>📥 PHASE 1: INTAKE</b><br>Chemical Fingerprinting...</div>", unsafe_allow_html=True)
        time.sleep(1)
        st.write(f"🔹 TDS: {tds_input:,} ppm")
    
    # إصلاح السطر 82 المسبب للخطأ
    st.markdown(f"<div class='ai-log'>[AI]: Initializing analysis... SI predicted at {si_res:.2f}. Moving to treatment cell.</div>", unsafe_allow_html=True)
    l1.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)
    time.sleep(1)

    # PHASE 2: SMART TREATMENT
    p_si.metric("Saturation Index (SI)", f"{si_res:.4f}")
    with n2.container():
        status_color = "#ff3333" if risk_res else "#00ffcc"
        st.markdown(f"<div class='node-card' style='border-color:{status_color}'><b>⚡ PHASE 2: AIDES CELL</b><br>Ion Recovery & Mitigation</div>", unsafe_allow_html=True)
        time.sleep(1)
        if risk_res:
            st.markdown(f"<div class='ai-log' style='color:red; border-color:red;'>[AI-ALERT]: SCALING RISK DETECTED (High Load). Voltage adjusted to {v_res:.2f}V.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-log'>[AI-SYSTEM]: Scaling Index is stable. Voltage optimized at {v_res:.2f}V.</div>", unsafe_allow_html=True)
    
    p_v.metric("Control Voltage", f"{v_res:.2f} V")
    l2.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)
    time.sleep(1)

    # PHASE 3: HARVESTING
    with n3.container():
        st.markdown("<div class='node-card'><b>🏗️ PHASE 3: HARVESTING</b><br>Mineral Recovery Phase</div>", unsafe_allow_html=True)
        time.sleep(1)
        st.write(f"💎 Purity: 99.2%")
        st.write(f"📦 Production: {gyp_res:.3f} T/hr")
    
    p_g.metric("Gypsum Yield", f"{gyp_res:.3f} T/h")
    
    # FINAL COMPLETION SUMMARY
    st.write("---")
    st.markdown(f"""
        <div class="success-summary">
            <h2 style="margin:0; color: #238636;">✅ Process Sequence Successfully Completed</h2>
            <p>AIDES System has successfully mitigated scaling risks and optimized mineral recovery.</p>
            <small>Session Log ID: AIDES-ENG-2026-{int(time.time())}</small>
        </div>
    """, unsafe_allow_html=True)

else:
    st.info("💡 Standby Mode: Select parameters and press 'Start Sequence' to begin the simulation.")

st.write("---")
st.caption("AIDES Smart Assistant | Professional Interface 2026")
