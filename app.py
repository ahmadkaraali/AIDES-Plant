import streamlit as st
import time

st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# تصميم CSS للأيقونات المجسمة والوميض
st.markdown("""
<style>
.main { background-color: #0b0e14; color: white; }
.phase-card { 
    background-color: #1a1e26; padding: 25px; border-radius: 20px; 
    border: 1px solid #2d3436; text-align: center;
    box-shadow: inset 2px 2px 5px #000, 8px 8px 20px #000; 
    min-height: 260px; transition: all 0.3s ease;
}
.icon-3d { filter: drop-shadow(5px 5px 8px #000); margin-bottom: 15px; }
@keyframes pulse-green { 0% { box-shadow: 0 0 35px #00ff00; border-color: #00ff00; } 50% { border-color: #2d3436; } }
@keyframes pulse-orange { 0% { box-shadow: 0 0 35px #ffaa00; border-color: #ffaa00; } 50% { border-color: #2d3436; } }
.active-green { animation: pulse-green 1s infinite !important; }
.active-orange { animation: pulse-orange 1s infinite !important; }
.led { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
.led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
.led-orange { background-color: #ffaa00; box-shadow: 0 0 10px #ffaa00; }
</style>
""", unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

if 'step' not in st.session_state: st.session_state.step = 0

with st.sidebar:
    st.header("⚙️ تحكم الذكاء الاصطناعي")
    tds = st.slider("ملوحة التغذية (ppm)", 10000, 60000, 45000)
    if st.button("🚀 بدء دورة الفصل الأيوني الذكي"): st.session_state.step = 1

# منطق تغير الكمون (Voltage) حسب نوع الملح
voltage = "0.00 V"
freq = "0 Hz"
if st.session_state.step == 1: voltage, freq = "0.85 V", "10 Hz"
elif st.session_state.step == 2: voltage, freq = "1.25 V", "60 Hz" # جهد أعلى لفصل الصوديوم
elif st.session_state.step == 3: voltage, freq = "1.10 V", "45 Hz"

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط", f"{tds * 0.025:.2f} bar")
with c2: st.metric("AI Potential (V)", voltage)
with c3: st.metric("Pulse Frequency", freq)
with c4: st.metric("System Load", "Active" if st.session_state.step > 0 else "Idle")

st.write("---")

p1, p2, p3 = st.columns(3)

with p1: # INTAKE
    act = "active-green" if st.session_state.step == 1 else ""
    st.markdown(f'<div class="phase-card {act}"><div class="led-green"></div><br><b>PHASE 1: INTAKE</b><br><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="45"><p>سحب المياه وتعديل pH</p></div>', unsafe_allow_html=True)

with p2: # TREATMENT
    act = "active-orange" if st.session_state.step == 2 else ""
    st.markdown(f'<div class="phase-card {act}"><div class="led-orange"></div><br><b>PHASE 2: AI TREATMENT</b><br><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="45"><p style="color:#ffaa00;">جاري موازنة الكمون الأيوني</p></div>', unsafe_allow_html=True)

with p3: # HARVESTING
    act = "active-green" if st.session_state.step == 3 else ""
    st.markdown(f'<div class="phase-card {act}"><div class="led-green"></div><br><b>PHASE 3: HARVESTING</b><br><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="45"><p>حصاد NaCl و Gypsum</p></div>', unsafe_allow_html=True)

if 1 <= st.session_state.step < 3:
    time.sleep(3)
    st.session_state.step += 1
    st.rerun()
