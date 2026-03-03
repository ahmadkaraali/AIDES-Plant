import streamlit as st
import time

# --- 1. الموصفات الهندسية (Smart Assistant Engine) ---
class AIDESEngine:
    def __init__(self, profile):
        self.K_SP = 2.4e-5
        self.threshold = 0.8 if profile == "Seawater" else 0.6
        self.factor = 1.2 if profile == "Seawater" else 2.0
        self.flow_rate = 150 

    def calculate(self, tds, temp):
        ca = (tds / 100000) * 0.02 * self.factor
        so4 = (tds / 100000) * 0.03 * self.factor
        ion_p = ca * so4
        temp_f = 1 + (temp - 25) * 0.01
        si = ion_p / (self.K_SP * temp_f)
        risk = si > self.threshold
        voltage = 1.5 if not risk else 1.5 * 0.85
        gyp_kg_hr = self.flow_rate * (tds / 1000) * 0.05 * 1.72 * 0.9
        gyp_tons = gyp_kg_hr / 1000
        # Predictive Maintenance Logic
        health_val = 100 if not risk else 100 - (si - self.threshold) * 50
        cip_val = int(150 - (tds/1000)*1.5) if risk else 450
        return si, risk, voltage, gyp_tons, health_val, cip_val

# --- 2. إعدادات الواجهة الرسومية وتأثير الـ 3D ---
st.set_page_config(page_title="AIDES Smart Assistant", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #10141d; color: #e6edf3; }
    [data-testid='stMetricValue'] { color: #00ffcc !important; font-weight: bold; font-size: 3rem !important; }
    
    /* تصميم البطاقات النافرة (3D Neumorphism) */
    .neumorphic-card {
        padding: 30px;
        border-radius: 20px;
        background: #10141d;
        box-shadow: 10px 10px 20px #080a0f, -10px -10px 20px #181e2b;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .floating-rocket {
        width: 120px;
        filter: drop-shadow(0 0 15px #00ffcc);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-15px) scale(1.05); }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ مساعدك الذكي: AIDES Digital Twin")
st.write("نظام المحاكاة الذكي لإدارة عمليات التحلية والصيانة التنبؤية")

with st.sidebar:
    st.header("⚙️ Operational Settings")
    tds_in = st.slider("Feedwater TDS (ppm)", 5000, 100000, 45000)
    temp_in = st.slider("Temperature (C)", 15, 50, 25)
    prof = st.selectbox("Application Sector", ["Seawater", "Produced Water", "Industrial", "Agriculture"])
    run = st.button("🚀 تشغيل النظام (Run System)")

# روابط الأيقونات
ICON_ROCKET = "https://cdn.pixabay.com/animation/2023/06/13/15/12/15-12-47-323_512.gif"

if run:
    engine = AIDESEngine(prof)
    si, risk, v, gyp, h, c = engine.calculate(tds_in, temp_in)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Saturation Index", f"{si:.4f}")
    col2.metric("Operating Voltage", f"{v:.2f} V")
    col3.metric("Gypsum Recovery", f"{gyp:.3f} T/h")

    st.divider()
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"<div class='neumorphic-card'><img src='{ICON_ROCKET}' class='floating-rocket'><br><br><h3>PHASE 1: INTAKE</h3></div>", unsafe_allow_html=True)
            
    with c2:
        clr = "#ff4b4b" if risk else "#00ffcc"
        st.markdown(f"""<div class='neumorphic-card' style='border-top: 4px solid {clr};'>
                <h1 style='font-size: 60px;'>⚡
