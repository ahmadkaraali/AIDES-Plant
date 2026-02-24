import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="AIDES Smart Platform 2026", layout="wide", page_icon="🏗️")

st.markdown("<h1 style='text-align: center; color: #005f73;'>🏢 منصة AIDES للتحكم الذكي وإنتاج الجبس</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>نظام التشغيل التفاعلي - إدارة التحلية واستعادة الموارد</p>", unsafe_allow_html=True)
st.write("---")

# 2. روابط الصور المتحركة (تم اختيارها لتمثيل المصنع)
GIF_INTAKE = "https://cdn.dribbble.com/users/2051513/screenshots/4338902/media/6b867c296711818274640f898a96d27f.gif"
GIF_PROCESSING = "https://cdn.dribbble.com/users/59947/screenshots/5554614/media/9d63c1e29e92d9d107a61d1912953265.gif"
GIF_GYPSUM = "https://cdn.dribbble.com/users/1162077/screenshots/3848914/media/4e7d95d18d8a7a938c8c50c18d890b0e.gif"

# 3. القائمة الجانبية (ثابتة للمناقشة)
st.sidebar.header("🕹️ مركز التحكم")
start_op = st.sidebar.button("🚀 تشغيل محاكاة النظام الذكي")
uploaded_file = st.sidebar.file_uploader("📂 تحميل ملف الأرشفة (اختياري)", type=["xlsx"])

# 4. منطق التشغيل المتسلسل (المحاكاة المتحركة)
if start_op:
    # المرحلة 1
    st.subheader("1️⃣ مرحلة سحب وتحليل المياه (Intake & Analysis)")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(GIF_INTAKE, use_container_width=True)
    with c2:
        with st.status("جاري سحب عينات المياه وتحليل الملوحة...", expanded=True):
            time.sleep(1.5)
            st.write("✅ الحساسات: TDS = 38,000 ppm")
            st.write("✅ التدفق: 150 m³/h")
    st.write("---")

    # المرحلة 2
    st.subheader("2️⃣ مرحلة المعالجة والانتزاع الكهربائي (AI-Control)")
    c3, c4 = st.columns([1, 2])
    with c3:
        st.image(GIF_PROCESSING, use_container_width=True)
    with c4:
        with st.status("الذكاء الاصطناعي يضبط الجهد الكهربائي...", expanded=True):
            time.sleep(2)
            st.write("⚡ الجهد المطبق: 1.45 Volt")
            st.write("🛡️ حالة الترسيب: منخفضة (تم تفعيل منع الترسيب الذكي)")
    st.write("---")

    # المرحلة 3
    st.subheader("3️⃣ مرحلة إنتاج الجبس (Resource Recovery)")
    c5, c6 = st.columns([1, 2])
    with c5:
        st.image(GIF_GYPSUM, use_container_width=True)
    with c6:
        with st.status("جاري تجميع وبلورة الجبس المنتج...", expanded=True):
            time.sleep(2)
            st.success("💎 كمية الإنتاج: 12.5 طن / ساعة")
            st.metric("العائد المادي المتوقع", "$1,500 / hr")
    st.balloons()

# 5. قسم الأرشفة الدائم (سواء رفعت ملف أو لا)
st.write("---")
st.subheader("📂 نظام الأرشفة والتدقيق الرقمي")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df, use_container_width=True)
else:
    # عرض البيانات التي أرسلتها في ملفك كنموذج ثابت
    demo_data = {
        'كود السجل': ['REQ-2026-001', 'MNT-2026-042', 'LAB-2026-015'],
        'البيان': ['تحليل TDS', 'صيانة مضخات', 'فحص مختبر'],
        'الحالة': ['مكتمل', 'قيد المراجعة', 'جاري التدقيق']
    }
    st.table(demo_data)

st.caption("نظام مساعدي الذكي | تطوير د. أحمد 2026")
