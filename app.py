import streamlit as st
import time
import pandas as pd

# 1. النواة الهندسية (كود الدكتور أحمد)
class AIDESEngine:
    def __init__(self, profile):
        self.K_SP = 2.4e-5
        self.threshold = 0.8 if profile == "Seawater" else 0.6
        self.factor = 1.2 if profile == "Seawater" else 2.0

    def calculate(self, tds, temp):
        ca = (tds / 100000) * 0.02 * self.factor
        so4 = (tds / 100000) * 0.03 * self.factor
        ion_p = ca * so4
        temp_f = 1 + (temp - 25) * 0.01
        si = ion_p / (self.K_SP * temp_f)
        risk = si > self.threshold
        voltage = 1.5 if not risk else 1.5 * 0.85
        return si, risk, voltage

# 2. إعدادات الواجهة (الواقعية الصناعية)
st.set_page_config(page_title="AIDES Real-time Simulator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    /* وضوح الأرقام الفسفوري */
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; font-size: 35px !important; }
    
    .process-node { 
        padding: 15px; border-radius: 10px; border: 2px solid #30363d; text-align: center; background: #161b22;
    }
    .flow-line { height: 4px; background: #58a6ff; margin-top: 50px; }
    .status-box { padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 AIDES: Interactive Process Simulator")
st.write("محاكاة حية لمسار المياه وعملية استعادة الجبس بناءً على التوأم الرقمي")

# المدخلات
with st.sidebar:
    st.header("🎮 لوحة تحكم المحاكاة")
    tds = st.slider("ملوحة التغذية (ppm)", 5000, 100000, 45000)
    temp = st.slider("الحرارة (°C)", 15, 50, 25)
    profile = st.selectbox("نوع المياه", ["Seawater", "Produced Water"])
    run = st.button("🚀 تشغيل المحاكاة الحية")

if run:
    engine = AIDESEngine(profile)
    si, risk, v = engine.calculate(tds, temp)

    # صف الأرقام الواضحة جداً
    c1, c2, c3 = st.columns(3)
    c1.metric("Saturation Index (SI)", f"{si:.4f}")
    c2.metric("Control Voltage", f"{v:.2f} V")
    c3.metric("Est. Gypsum Yield", f"{(tds*0.04)/1000:.2f} T/h")

    st.write("---")
    st.subheader("🛠️ تمثيل مسار التدفق (Process Flow)")

    # محاكاة مرئية للمحطة
    m1, f1, m2, f2, m3 = st.columns([2, 1, 2, 1, 2])

    with m1:
        st.markdown("<div class='process-node'><b>📥 مدخل مياه التغذية</b><br>تحليل كيميائي مستمر</div>", unsafe_allow_html=True)
        st.write(f"💧 الملوحة: {tds:,} ppm")
        st.write("✅ الحساسات تعمل")

    f1.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)

    with m2:
        # خلية المعالجة الذكية يتغير لونها حسب الخطر
        color = "#ff3333" if risk else "#00ffcc"
        st.markdown(f"<div class='process-node' style='border-color:{color}'><b>⚡ خلية AIDES الذكية</b><br>المعالجة والانتزاع</div>", unsafe_allow_html=True)
        if risk:
            st.markdown(f"<div class='status-box' style='background:#721c24; color:#f8d7da;'>⚠️ تنبيه: خطر ترسيب جبس! (SI={si:.2f})<br>تفعيل خفض الجهد..</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-box' style='background:#155724; color:#d4edda;'>✅ الحالة: مستقرة<br>كفاءة انتزاع قصوى</div>", unsafe_allow_html=True)

    f2.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)

    with m3:
        st.markdown("<div class='process-node'><b>🏗️ إنتاج الجبس</b><br>تجميع وتجفيف</div>", unsafe_allow_html=True)
        st.write(f"💎 النقاء: 99.1%")
        st.write(f"📦 الإنتاج: {(tds*0.04)/1000:.2f} طن/س")

    st.write("---")
    # منطق الذكاء الاصطناعي (Terminal Style)
    with st.expander("👁️ عرض منطق اتخاذ القرار (AI Reasoning Hub)"):
        st.code(f"""
        [Step 1]: Chemical Analysis Initialized for {profile}
        [Step 2]: Calculated Ion Product for Ca & SO4
        [Step 3]: SI ({si:.4f}) vs Threshold ({engine.threshold})
        [Step 4]: Decision: {'REDUCE POWER' if risk else 'STABILIZE'}
        [Step 5]: Execution: Voltage set to {v}V
        """)
else:
    st.info("💡 حرك المؤشرات واضغط 'تشغيل المحاكاة' لرؤية كيف يتفاعل النظام مع الواقع.")
