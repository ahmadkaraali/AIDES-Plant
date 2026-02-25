import streamlit as st
import time
import pandas as pd

# 1. إعدادات المنصة
st.set_page_config(page_title="AIDES Operator Control", layout="wide", page_icon="⚙️")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .operator-panel { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #0077b6; }
    .ai-badge { background-color: #e1f5fe; color: #01579b; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕹️ مركز التحكم التفاعلي للمشغل - نظام AIDES")
st.write("---")

# 2. لوحة تحكم المشغل (هامش الخيارات)
st.sidebar.header("🛠️ خيارات المشغل (Operator Inputs)")
with st.sidebar:
    op_mode = st.radio("اختر نمط التشغيل:", ["التحكم الذكي (AI Auto)", "التحكم اليدوي (Manual)"])
    
    st.markdown("---")
    # هامش خيارات الملوحة والتدفق
    input_tds = st.slider("تحديد ملوحة مياه التغذية (ppm):", 5000, 70000, 35000)
    input_flow = st.slider("معدل التدفق المستهدف (m³/h):", 50, 500, 150)
    
    st.markdown("---")
    start_op = st.button("🚀 تنفيذ الأوامر التشغيلية")

# 3. منطق الذكاء الاصطناعي
# إذا اختار المشغل "آلي"، النظام يصحح القيم، إذا اختار "يدوي"، يلتزم بكلام المشغل
if op_mode == "التحكم الذكي (AI Auto)":
    suggested_voltage = 1.2 + (input_tds / 50000)
    ai_status = "النظام الذكي يضبط الجهد تلقائياً لمنع الترسيب"
else:
    suggested_voltage = st.sidebar.number_input("تحديد الجهد يدوياً (Volt):", 0.5, 5.0, 1.5)
    ai_status = "تنبيه: المشغل يتحكم في الجهد يدوياً الآن"

# 4. العرض الأفقي للمراحل
if start_op:
    st.markdown(f"<div class='ai-badge'>الحالة الحالية: {ai_status}</div><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📦 **المدخلات الحالية**")
        st.metric("الملوحة المحددة", f"{input_tds} ppm")
        st.metric("التدفق المطلوب", f"{input_flow} m³/h")

    with col2:
        st.warning("⚡ **وحدة المعالجة AIDES**")
        st.metric("الجهد التشغيلي", f"{suggested_voltage:.2f} V")
        if input_tds > 50000:
            st.error("⚠️ خطر ترسيب عالي!")
        else:
            st.success("✅ العمل بظروف آمنة")

    with col3:
        st.success("🏗️ **مخرجات النظام**")
        gypsum_calc = (input_tds * input_flow) / 500000
        st.metric("إنتاج الجبس المتوقع", f"{gyp_calc:.2f} طن/س")
        st.metric("صافي الربح التقديري", f"${gyp_calc * 120:.0f}")

    st.balloons()

else:
    st.markdown("""
    ### 👨‍نيابة عن المشغل:
    يمكنك من خلال القائمة الجانبية **تغيير ملوحة المياه** أو **معدل التدفق** وتحديد ما إذا كنت تريد من **الذكاء الاصطناعي** تولي القيادة أم تريد التحكم يدوياً.
    
    *هذا الهامش يسمح للمهندس بالتدخل في الحالات الخاصة مع الحفاظ على كفاءة النظام.*
    """)

# 5. الأرشفة الذكية
st.write("---")
with st.expander("📂 سجل قرارات المشغل (Log File)"):
    st.write(f"توقيت العملية: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"النمط المختار: {op_mode}")
    st.write(f"القيم المدخلة: TDS={input_tds}, Flow={input_flow}")
