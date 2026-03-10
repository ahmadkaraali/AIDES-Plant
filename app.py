import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# تصميم CSS للأضواء والمظهر الداكن
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .status-blink-green { color: #00ff00; animation: pulse 1.5s infinite; font-weight: bold; }
    .status-blink-yellow { color: #ffff00; animation: pulse 1.5s infinite; font-weight: bold; }
    .status-blink-blue { color: #00ffff; animation: pulse 2s infinite; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")
st.subheader("نظام المحاكاة الذكي لإدارة عمليات التحلية والحصاد الصناعي")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ Operational Settings")
    tds = st.slider("Feedwater TDS (ppm)", 10000, 60000, 45000)
    temp = st.slider("Temperature (C)", 10, 50, 25)
    run = st.button("🚀 تشغيل النظام (Run System)")

# الحسابات الكيميائية (Mass Balance)
flow = 15.0 
total_salts = (tds * flow) / 1000000
nacl_val = total_salts * 0.777 
gypsum_val = (total_salts * 0.077) * 1.79

# عرض المؤشرات العلوية (المعادلة المحدثة)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Saturation Index", f"{tds * 0.025:.4f}")
with c2: st.metric("Operating Voltage", "1.15 V")
with c3: st.metric("NaCl Recovery (White)", f"{nacl_val:.3f} T/h")
with c4: st.metric("Gypsum Recovery (Blue)", f"{gypsum_val:.3f} T/h")

st.write("---")

# مراحل العمل (بدون روابط صور خارجية لتجنب الخطأ)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown('<div class="stMetric">', unsafe_allow_html=True)
    st.markdown("### PHASE 1 \n ## INTAKE")
    if run: st.markdown('<p class="status-blink-green">● FLOW ACTIVE</p>', unsafe_allow_html=True)
    st.write("سحب وتحليل مياه البحر")
    st.markdown('</div>', unsafe_allow_html=True)

with p2:
    st.markdown('<div class="stMetric">', unsafe_allow_html=True)
    st.markdown("### PHASE 2 \n ## TREATMENT")
    if run: st.markdown('<p class="status-blink-yellow">● ION SEPARATION</p>', unsafe_allow_html=True)
    st.write(f"Health: {(1-(tds/100000))*100:.1f}%")
    st.write("Next CIP: 191h")
    st.markdown('</div>', unsafe_allow_html=True)

with p3:
    st.markdown('<div class="stMetric">', unsafe_allow_html=True)
    st.markdown("### PHASE 3 \n ## HARVESTING")
    if run: st.markdown('<p class="status-blink-blue">● SALT & GYPSUM ACTIVE</p>', unsafe_allow_html=True)
    st.write("استخلاص الملح والجبس الصناعي")
    st.markdown('</div>', unsafe_allow_html=True)

if run:
    st.success("المحطة تعمل الآن بكفاءة استخلاص قصوى")
