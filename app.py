import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

# 1. النواة الهندسية (كود الدكتور أحمد)
class AIDESControlEngine:
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.K_SP_GYPSUM = 2.4e-5
        self.settings = {
            "Seawater": {"factor": 1.2, "threshold": 0.8, "base_v": 1.5},
            "Produced Water": {"factor": 2.0, "threshold": 0.6, "base_v": 2.0}
        }
        self.curr = self.settings[profile_name]

    def analyze(self, tds, temp):
        ca_conc = (tds / 100000) * 0.02 * self.curr["factor"]
        so4_conc = (tds / 100000) * 0.03 * self.curr["factor"]
        ion_product = ca_conc * so4_conc
        temp_factor = 1 + (temp - 25) * 0.01
        s_index = ion_product / (self.K_SP_GYPSUM * temp_factor)
        risk = "CRITICAL" if s_index > self.curr["threshold"] else "SAFE"
        v = self.curr["base_v"]
        if tds > 40000: v += (tds - 40000) * 0.00005
        if risk == "CRITICAL": v *= 0.85 
        return s_index, risk, v

# 2. تحسينات الواجهة (ألوان زاهية وخطوط واضحة)
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

st.markdown("""
    <style>
    /* جعل الخلفية داكنة احترافية */
    .stApp { background-color: #050505; color: white; }
    
    /* تحسين وضوح الأرقام في المربعات (Metrics) */
    [data-testid="stMetricValue"] {
        color: #00ffcc !important; /* لون فسفوري واضح جداً */
        font-size: 40px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 18px !important;
    }
    .decision-panel { 
        background-color: #101010; 
        border-left: 5px solid #00ffcc; 
        padding: 20px; 
        font-family: 'Consolas', monospace; 
        color: #00ffcc;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AIDES: Digital Twin Command Center")
st.write("الجيل القادم من أنظمة التحكم الكيميائي الذكي")

with st.sidebar:
    st.header("📡 Live Sensor Data")
    tds = st.slider("TDS (ppm)", 5000, 100000, 45000)
    temp = st.slider("Temperature (°C)", 15, 50, 25)
    p_type = st.selectbox("Feedwater Profile", ["Seawater", "Produced Water"])
    st.markdown("---")
    run_engine = st.button("🚀 تفعيل النظام الذكي")

if run_engine:
    engine = AIDESControlEngine(p_type)
    s_index, risk, v = engine.analyze(tds, temp)

    # صف المؤشرات بوضوح عالي
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Saturation Index", f"{s_index:.4f}")
    c2.metric("Target Voltage", f"{v:.2f} V")
    c3.metric("System Status", risk)
    c4.metric("Est. Production", f"{(tds*0.04)/1000:.2f} T/h")

    st.write("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📈 التحليل الديناميكي للترسيب")
        # رسم بياني احترافي يوضح العلاقة
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Saturation Index', x=['Current State'], y=[s_index], marker_color='#00ffcc'))
        fig.add_trace(go.Scatter(name='Critical Threshold', x=['Current State'], y=[engine.curr["threshold"]], mode='lines+markers', marker_color='red'))
        fig.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🧠 منطق الذكاء الاصطناعي")
        st.markdown(f"""
        <div class='decision-panel'>
        > ANALYZING CHEMICAL DATA...<br>
        > ION PRODUCT CALCULATED.<br>
        > Ksp LIMIT: 2.4e-5<br>
        > STATUS: <span style='color:{"red" if risk=="CRITICAL" else "#00ffcc"}'>{risk}</span><br>
        > ACTION: {'ADJUSTING VOLTAGE' if risk=="CRITICAL" else 'MAXIMIZING YIELD'}<br>
        > OUTPUT V: {v:.2f}V
        </div>
        """, unsafe_allow_html=True)

    if risk == "CRITICAL":
        st.warning(f"⚠️ تم اكتشاف خطر ترسيب! النظام قام بتفعيل بروتوكول براءة الاختراع وخفض الجهد إلى {v:.2f}V")
    else:
        st.success("✅ النظام يعمل بكفاءة إنتاجية قصوى.")

else:
    st.info("💡 بانتظار إشارة البدء لعرض بيانات التوأم الرقمي...")

st.write("---")
st.caption("AIDES Smart Platform | تصميم وتطوير د. أحمد 2026")
