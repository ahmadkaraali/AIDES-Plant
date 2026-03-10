import streamlit as st
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للأيقونات المجسمة والوميض المتسلسل
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    
    /* إطارات المراحل بتأثير نافر (3D) */
    .phase-card { 
        background-color: #1a1e26; 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid #2d3436; 
        text-align: center;
        box-shadow: inset 2px 2px 5px #000, 5px 5px 15px #000; 
        min-height: 220px;
        transition: all 0.3s ease;
    }

    /* أيقونات مجسمة نافرة */
    .icon-3d {
        filter: drop-shadow(4px 4px 6px #000);
        margin-bottom: 10px;
    }

    /* وميض المرحلة النشطة */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
        50% { box-shadow: 0 0 25px #00ff00; border-color: #00ff00; }
        100% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
    }
    .active-step { animation: pulse-glow 1s infinite !important; }

    .led { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
    .led-orange { background-color: #ffaa00; box-shadow: 0 0 10px #ffaa00; }
    .led-off { background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ تحكم العمليات")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    if st.button("🚀 بدء دورة التشغيل (START CYCLE)"):
        st.session_state.current_step = 1

# 4. الحسابات التشغيلية
flow = 15.0
total_min = (tds * flow) / 1000000
nacl = total_min * 0.777 if st.session_state.current_step == 3 else 0.0
gyp = (total_min * 0.077) * 1.79 if st.session_state.current_step == 3 else 0.0

# 5. العدادات العلوية
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط التشغيلي", f"{tds * 0.025:.2f} bar")
with c2: st.metric("Voltage", "1.15 V" if st.session_state.current_step > 0 else "0.00 V")
with c3: st.metric("إنتاج NaCl", f"{nacl:.3f} T/h")
with c4: st.metric("إنتاج الجبس", f"{gyp:.3f} T/h")

st.write("---")

# 6. عرض المراحل المتسلسل
p1, p2, p3 = st.columns(3)

# المرحلة الأولى: INTAKE
with p1:
    is_active = "active-step" if st.session_state.current_step == 1 else ""
    led = "led-green" if st.session_state.current_step >= 1 else "led-off"
    st.markdown(f"""
        <div class="phase-card {is_active}">
            <div class="led {led}"></div>
            <div style="font-size:18px; font-weight:bold;">PHASE 1: INTAKE</div>
            <img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="50">
            <p style="font-size:13px;">{'جاري سحب المياه...' if st.session_state.current_step == 1 else 'جاهز'}</p>
        </div>
    """, unsafe_allow_html=True)

# المرحلة الثانية: TREATMENT
with p2:
