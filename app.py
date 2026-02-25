import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

# إعدادات الواجهة الفاخرة
st.set_page_config(page_title="AIDES Hyper-Visual Platform", layout="wide", page_icon="🏗️")

# CSS لإضافة تأثيرات جمالية (تدرج ألوان واهتزاز بسيط للتنبيهات)
st.markdown("""
    <style>
    .reportview-container { background: linear-gradient(to right, #ece9e6, #ffffff); }
    .stMetric { border-left: 5px solid #005f73; background-color: #f8f9fa; }
    @keyframes blinker { 50% { opacity: 0; } }
    .alert-flash { color: red; animation: blinker 1s linear infinite; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ المركز السيادي للتحكم الذكي | AIDES Hyper-Platform")
st.markdown("<p style='font-size: 20px; color: #555;'>نظام إدارة الموارد المتكاملة: تحلية المياه واستعادة المعادن</p>", unsafe_allow_html=True)
st.write("---")

# روابط وسائط عالية الجودة (عناصر متحركة)
GIF_MOLECULES = "https://cdn.dribbble.com/users/244440/screenshots/2361250/media/1d9b324391672323e98188172828b1a9.gif" # محاكاة حركة الجزيئات
GIF_CONTROL_ROOM = "https://cdn.dribbble.com/users/1059583/screenshots/3944634/media/f38f71261d713c706d33454224c30c82.gif" # غرفة التحكم

# القائمة الجانبية
st.sidebar.image(GIF_CONTROL_ROOM, use_container_width=True)
st.sidebar.header("🕹️ التحكم في السيناريو التشغيلي")
scenario = st.sidebar.selectbox("اختر وضع التشغيل:", ["الوضع الطبيعي", "وضع الملوحة العالية", "حالة طوارئ (ترسيب)"])
run_btn = st.sidebar.button("🚀 إطلاق المحاكاة الشاملة")

if run_btn:
    # المرحلة 1: التحليل الكيميائي الرقمي
    st.subheader("🔍 المرحلة الأولى: الاستشعار الكيميائي المتقدم")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(GIF_MOLECULES, caption="محاكاة حركة الأيونات في المحلول", use_container_width=True)
    with col2:
        st.write("### تحليل التدفق الحقيقي")
        tds_val = 35000 if scenario == "الوضع الطبيعي" else 65000
        st.progress(0.4)
        st.metric("تركيز الأملاح الحالي", f"{tds_val} ppm", delta="حالة مستقرة" if tds_val < 40000 else "حرجة", delta_color="inverse")
        time.sleep(1)

    # المرحلة 2: المعالجة الذكية (قلب النظام)
    st.write("---")
    st.subheader("⚡ المرحلة الثانية: الانتزاع الكهربائي المبرمج (AI-OS)")
    col3, col4 = st.columns([2, 1])
    with col3:
        if scenario == "حالة طوارئ (ترسيب)":
            st.markdown("<p class='alert-flash'>⚠️ تحذير: اكتشاف بوادر ترسيب على الأغشية! تفعيل القطبية العكسية فوراً.</p>", unsafe_allow_html=True)
        
        # رسم بياني متحرك للجهد الكهربائي
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 1.8 if scenario == "الوضع الطبيعي" else 2.4,
            title = {'text': "الجهد التشغيلي (Voltage)"},
            gauge = {'axis': {'range': [0, 5]}, 'bar': {'color': "darkblue"}}
        ))
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        st.info("الذكاء الاصطناعي يقوم الآن بموازنة الجهد لضمان أقصى إنتاجية بأقل استهلاك للطاقة.")
        time.sleep(1)

    # المرحلة 3: التجسيد المادي (الجبس)
    st.write("---")
    st.subheader("💎 المرحلة الثالثة: تحويل النفايات إلى ثروة (الجبس)")
    col5, col6 = st.columns([1, 1])
    with col5:
        st.success("🏗️ جاري ترسيب كبريتات الكالسيوم بنقاء 99%")
        gyp_prod = 12.5 if scenario != "حالة طوارئ (ترسيب)" else 4.2
        st.metric("إنتاج الجبس اللحظي", f"{gyp_prod} طن/ساعة")
    with col6:
        profit = gyp_prod * 150
        st.metric("العائد المادي المتوقع (ساعة)", f"${profit:,}")
        st.write("📈 تم تحقيق عائد إضافي يغطي 30% من تكاليف تشغيل المحطة.")
    
    st.balloons()
else:
    st.info("💡 جاهزون للعرض يا دكتور.. اختر سيناريو التشغيل من اليسار واضغط 'إطلاق' لإبهار اللجنة.")

# الأرشفة الرقمية في الأسفل
st.write("---")
with st.expander("📂 نظام الأرشفة الذكي - سجلات REQ/MNT/LAB"):
    st.write("يتم هنا ربط كافة البيانات الورقية السابقة بالنظام الرقمي الموحد.")
    st.table(pd.DataFrame({'التاريخ': [pd.Timestamp.now().date()], 'الحالة': ['Active'], 'المستخدم': ['Dr. Ahmed']}))
