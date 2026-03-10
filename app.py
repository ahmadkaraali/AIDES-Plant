import streamlit as st

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للإضاءة القوية (Neon) والنبض التشغيلي
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stMetric { background-color: #161a23; padding: 25px; border-radius: 15px; border: 1px solid #2d3436; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    
    /* أنيميشن التوهج عند التشغيل */
    @keyframes glow {
        0% { box-shadow: 0 0 5px #00ff00; }
        50% { box-shadow: 0 0 25px #00ff00; }
        100% { box-shadow: 0 0 5px #00ff00; }
    }
    .active-plant { animation: glow 2s infinite; border: 2px solid #00ff00 !important; }
    
    /* نقاط LED الحالة */
    .led-on { height: 15px; width: 15px; background-color: #00ff00; border-radius: 50%; display: inline-block; box-shadow: 0 0 12px #00ff00; margin-right: 10px; }
    .led-off { height: 15px; width: 15px; background-color: #ff4b4b; border-radius: 50%; display: inline-block; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان
st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")
st.write("بيان تشغيل محطة التحلية وحصاد المعادن الصناعية - عرض حي لأصحاب القرار")

# 4. لوحة التحكم
with st.sidebar:
    st.header("🎮 تحكم المحطة")
    tds_input = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    is_running = st.toggle("تفعيل المحطة (RUN PLANT)", value=False)
    if is_running:
        st.success("المحطة متصلة وتعمل الآن")
    else:
        st.warning("المحطة في وضع الاستعداد")

# 5. الحسابات التشغيلية (Mass Balance)
flow = 15.0 # m3/h
total_minerals = (tds_input * flow) / 1000000
nacl_val = total_minerals * 0.777
gyp_val = (total_minerals * 0.077) * 1.79

# 6. العدادات الرقمية الكبرى (إظهار ملح الطعام والجبس بوضوح)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط التشغيلي", f"{tds_input * 0.025:.2f} bar")
with c2: st.metric("Operating Voltage", "1.15 V" if is_running else "0.00 V")
with c3: st.metric("إنتاج ملح الطعام (NaCl)", f"{nacl_val:.3f} T/h" if is_running else "0.000")
with c4: st.metric("إنتاج الجبس (Gypsum)", f"{gyp_val:.3f} T/h" if is_running else "0.000")
