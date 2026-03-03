import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

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
        health = 100 if not risk else 100 - (si - self.threshold) * 50
        next_cip = int(250 - (tds/1000)*1.2) if risk else 450
        return si, risk, voltage, gyp_tons, health, cip

# --- 2. إعدادات الواجهة الرسومية ---
st.set_page_config(page_title="AIDES Smart Assistant", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b101a; color: #e6edf3; }
    [data-testid='stMetricValue'] { color: #00ffcc !important; font-weight: bold; }
    .node-card { padding: 20px; border-radius: 12px; border: 1px solid #30363d; background: #161b22; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ مساعدك الذكي: AIDES Digital Twin")
st.write("نظام المحاكاة الذكي لإدارة عمليات التحلية والصيانة التنبؤية")

# القائمة الجانبية للمدخلات
with st.sidebar:
    st.header("⚙️ Operational Settings")
    tds_in = st.slider("Feedwater TDS (ppm)", 5000, 100000, 45000)
    temp_in = st.slider("Temperature (°C)", 15, 50, 25)
    prof = st.selectbox("Application Sector", ["Seawater", "Produced Water", "Industrial", "Agriculture"])
    run = st.button("🚀 تشغيل النظام (Run System)")

# روابط الأيقونات (GIFs)
ICON_IN = "https://cdn.pixabay.com/animation/2023/06/13/15/12/15-12-47-323_512.gif"
ICON_CL = "https://cdn.pixabay.com/animation/2022/10/25/11/49/11-49-14-118_512.gif"
ICON_GY = "https://cdn.pixabay.com/animation/2022/07/31/05/23/05-23-44-323_512.gif"

if run:
    engine = AIDESEngine(prof)
    si, risk, v, gyp, health, cip = engine.calculate(tds_in, temp_in)
    
    # صف المؤشرات الرئيسية
    col1, col2, col3 = st.columns(3)
    col1.metric("Saturation Index", f"{si:.4f}")
    col2.metric("Operating Voltage", f"{v:.2f} V")
    col3.metric("Gypsum Recovery", f"{gyp:.3f} T/h")

    st.divider()
    
    # صف الرسم البياني والتدفق
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"<div class='node-card'><img src='{ICON_IN}' width='100'><br><b>PHASE 1: INTAKE</b></div>", unsafe_allow_html=True)
        st.info("سحب المياه وتحليل الملوحة")
        
    with c2:
        clr = "#ff4b4b" if risk else "#00ffcc"
        st.markdown(f"<div class='node-card' style='border-color:{clr}'><img src='{ICON_CL}' width='100'><br><b>PHASE 2: TREATMENT</b></div>", unsafe_allow_html=True)
        st.write(f"🛠️ Electrode Health: **{health:.1f}%**")
        st.write(f"📅 Next CIP: **{cip} hours**")
        
    with c3:
        st.markdown(f"<div class='node-card'><img src='{ICON_GY}' width='100'><br><b>PHASE 3: HARVESTING</b></div>", unsafe_allow_html=True)
        st.success(f"تم استرداد {gyp:.2f} طن/ساعة")

    st.success("تم الانتهاء من محاكاة العملية بنجاح - النظام مستقر")
