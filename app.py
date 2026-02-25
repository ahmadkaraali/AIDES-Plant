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

# 2. إعدادات الواجهة (المحافظة على تصميم الصورة المرفقة)
st.set_page_config(page_title="AIDES Real-time Simulator", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; font-size: 35px !important; }
    .process-node { padding: 15px; border-radius: 10px; border: 2px solid #30363d; text-align: center; background: #161b22; min-height: 120px; }
    .flow-line { height: 4px; background: #58a6ff; margin-top: 60px; transition: 2s; }
    .ai-msg { background: #1a1a1a; color: #ffd166; padding: 10px; border-left: 4px solid #ffd166; font-family: monospace; font-size: 14px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 AIDES: Interactive Process Simulator")
st.write("محاكاة حية متسلسلة لمسار المياه وعملية استعادة الجبس")

with st.sidebar:
    st.header("🎮 لوحة تحكم المحاكاة")
    tds = st.slider("ملوحة التغذية (ppm)", 5000, 100000, 45000)
    temp = st.slider("الحرارة (°C)", 15, 50, 25)
    profile = st.selectbox("نوع المياه", ["Seawater", "Produced Water"])
    run = st.button("🚀 بدء دورة التشغيل النمذجية")

# حاويات العرض (تبدأ فارغة)
header_cols = st.columns(3)
m_si = header_cols[0].empty()
m_v = header_cols[1].empty()
m_g = header_cols[2].empty()

st.write("---")
st.subheader("🛠️ تمثيل مسار التدفق (Process Flow)")
flow_cols = st.columns([2, 0.5, 2, 0.5, 2])
node1 = flow_cols[0].empty()
line1 = flow_cols[1].empty()
node2 = flow_cols[2].empty()
line2 = flow_cols[3].empty()
node3 = flow_cols[4].empty()

if run:
    engine = AIDESEngine(profile)
    si, risk, v = engine.calculate(tds, temp)
    
    # --- المرحلة 1: المدخلات ---
    with node1.container():
        st.markdown("<div class='process-node'><b>📥 مدخل مياه التغذية</b><br>جاري سحب العينة...</div>", unsafe_allow_html=True)
        time.sleep(1)
        st.write(f"💧 الملوحة: {tds:,} ppm")
        st.markdown("<p style='color:#00ffcc;'>✅ تم التحليل</p>", unsafe_allow_html=True)
    
    # رسالة ذكاء اصطناعي للتحويل
    st.markdown(f"<div class='ai-msg'>[AI]: تحليل المرحلة 1 مكتمل. قيمة الإشباع المتوقعة SI={si:.2f}. توجيه التدفق للمرحلة 2...</div>", unsafe_allow_html=True)
    line1.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- المرحلة 2: المعالجة الذكية ---
    m_si.metric("Saturation Index (SI)", f"{si:.4f}")
    with node2.container():
        color = "#ff3333" if risk else "#00ffcc"
        st.markdown(f"<div class='process-node' style='border-color:{color}'><b>⚡ خلية AIDES الذكية</b><br>المعالجة والانتزاع</div>", unsafe_allow_html=True)
        time.sleep(1)
        if risk:
            st.error(f"⚠️ تنبيه: خطر ترسيب! (SI={si:.2f})")
            st.markdown(f"<div class='ai-msg'>[AI]: تم تفعيل بروتوكول براءة الاختراع. خفض الجهد لـ {v}V لمنع الترسيب.</div>", unsafe_allow_html=True)
        else:
            st.success("✅ الحالة: مستقرة")
            st.markdown(f"<div class='ai-msg'>[AI]: استقرار كيميائي مثالي. الحفاظ على جهد {v}V.</div>", unsafe_allow_html=True)
    
    m_v.metric("Control Voltage", f"{v:.2f} V")
    line2.markdown("<div class='flow-line'></div>", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- المرحلة 3: الإنتاج النهائي ---
    with node3.container():
        st.markdown("<div class='process-node'><b>🏗️ إنتاج الجبس</b><br>تجميع وتجفيف</div>", unsafe_allow_html=True)
        time.sleep(1)
        gyp = (tds * 0.04) / 1000
        st.write(f"💎 النقاء: 99.1%")
        st.write(f"📦 الإنتاج: {gyp:.2f} طن/س")
    
    m_g.metric("Est. Gypsum Yield", f"{gyp:.2f} T/h")
    st.markdown("<div class='ai-msg'>[AI]: اكتملت الدورة التشغيلية بنجاح. تم تسجيل البيانات في الأرشيف السيادي.</div>", unsafe_allow_html=True)
    st.balloons() # لمسة احتفالية خفيفة بالنهاية

else:
    st.info("💡 النظام في وضع الاستعداد. اضغط على 'بدء دورة التشغيل' لمشاهدة المحاكاة النمذجية.")
