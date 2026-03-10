import streamlit as st
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للأيقونات المجسمة والوميض (تم تبسيطه لتجنب أخطاء النسخ)
st.markdown("""
<style>
.main { background-color: #0b0e14; color: white; }
.phase-card { 
    background-color: #1a1e26; padding: 25px; border-radius: 20px; 
    border: 1px solid #2d3436; text-align: center;
    box-shadow: inset 2px 2px 5px #000, 8px 8px 20px #000; 
    min-height: 240px; transition: all 0.3s ease;
}
.icon-3d { filter: drop-shadow(5px 5px 8px #000); margin-bottom: 15px; }
@keyframes pulse-green {
    0% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
    50% { box-shadow: 0 0 30px #00ff00; border-color: #00ff00; }
    100% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
}
@keyframes pulse-orange {
    0% { box-shadow: 0 0 5px #ffaa00; border-color: #2d3436; }
    50% { box-shadow: 0 0 30px #ffaa00; border-color: #ffaa00; }
    100% { box-shadow: 0 0 5px #ffaa00; border-color: #2d3436; }
}
.active-green { animation: pulse-green 1.2s infinite !important; }
.active-orange { animation: pulse-orange 1.2s infinite !important; }
.led { height: 14px; width: 14px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
.led-green { background-color: #00ff00; box-shadow: 0 0 12px #00ff00; }
.led-orange { background-color: #ffaa00; box-shadow: 0 0 12px #ffaa00; }
.led-off { background-color: #333; }
</style>
""", unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

# 3. إدارة الحالة (Session State)
if 'step' not in st.session_state:
    st.session_state.step = 0

# 4. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ تحكم العمليات")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    if st.button("🚀 بدء دورة التشغيل (START CYCLE)"):
        st.session_state.step = 1

# 5. الحسابات والعدادات
total_min = (tds * 15.0) / 1000000
nacl_val = total_min * 0.777 if st.session_state.step == 3 else 0.0
gyp_val = (total_min * 0.077) * 1.79 if st.session_state.step == 3 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط", f"{tds * 0.025:.2f} bar")
with c2: st.metric("Voltage", "1.15 V" if st.session_state.step > 0 else "0.00 V")
with c3: st.metric("الملح NaCl", f"{nacl_val:.3f} T/h")
with c4: st.metric("الجبس", f"{gyp_val:.3f} T/h")

st.write("---")

# 6. عرض المراحل المتسلسل (أيقونات نافرة)
p1, p2, p3 = st.columns(3)

with p1: # المرحلة 1
    act = "active-green" if st.session_state.step == 1 else ""
    led = "led-green" if st.session_state.step >= 1 else "led-off"
    st.markdown(f'<div class="phase-card {act}"><div class="led {led}"></div><div style="font-size:20px; font-weight:bold;">PHASE 1: INTAKE</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="45"><p>{"جاري السحب..." if st.session_state.step==1 else "جاهز"}</p></div>', unsafe_allow_html=True)

with p2: # المرحلة 2
    act = "active-orange" if st.session_state.step == 2 else ""
    led = "led-orange" if st.session_state.step >= 2 else "led-off"
    st.markdown(f'<div class="phase-card {act}"><div class="led {led}"></div><div style="font-size:20px; font-weight:bold;">PHASE 2: TREATMENT</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="45"><p style="color:#ffaa00;">{"تحضير أيوني..." if st.session_state.step==2 else "جاهز"}</p></div>', unsafe_allow_html=True)

with p3: # المرحلة 3
    act = "active-green" if st.session_state.step == 3 else ""
    led = "led-green" if st.session_state.step >= 3 else "led-off"
    st.markdown(f'<div class="phase-card {act}"><div class="led {led}"></div><div style="font-size:20px; font-weight:bold;">PHASE 3: HARVESTING</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="45"><p>{"جاري الحصاد..." if st.session_state.step==3 else "جاهز"}</p></div>', unsafe_allow_html=True)

# 7. التتابع التلقائي
if 0 < st.session_state.step < 3:
    time.sleep(2.5)
