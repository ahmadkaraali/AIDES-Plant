import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# تصميم CSS متطور لإضاءة النيون والوميض التشغيلي
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stMetric { background-color: #161a23; padding: 20px; border-radius: 15px; border: 1px solid #2d3436; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    
    /* أنيميشن النبض الضوئي */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px rgba(0,255,0,0.2); border-color: #2d3436; }
        50% { box-shadow: 0 0 25px rgba(0,255,0,0.6); border-color: #00ff00; }
        100% { box-shadow: 0 0 5px rgba(0,255,0,0.2); border-color: #2d3436; }
    }
    .active-card { animation: pulse-glow 2s infinite; border: 2px solid #00ff00 !important; }
    
    /* أضواء LED صغيرة */
    .led-green { height: 12px; width: 12px; background-color: #00ff00; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #00ff00; margin-right: 10px; }
    .led-off { height: 12px; width: 12px; background-color: #444; border-radius: 50%; display: inline-block; margin-right: 10px; }
    
    .phase-title { font-size: 24px; font-weight: bold; margin-bottom: 10px; color: #dfe6e9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")
st.write("نظام المحاكاة التفاعلي لإثبات كفاءة الفصل الأيوني وحصاد الملح والجبس")

# القائمة الجانبية للتحكم
with st.sidebar:
    st.header("🎮 لوحة التحكم التشغيلية")
    tds = st.slider("ملوحة المياه (TDS ppm)", 10000, 60000, 45000)
    run = st.checkbox("⚡ تشغيل المحطة الآن (START PLANT)", value=False)
    st.info("قم بتفعيل الزر أعلاه لإظهار بيان العمل للشركة")

# الحسابات الهندسية لملح الطعام والجبس
flow = 15.0 
total_salts = (tds * flow) / 1000000
nacl_val = total_salts * 0.777 
gypsum_val
