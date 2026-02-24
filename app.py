import streamlit as st
import time

# إعدادات المنصة
st.set_page_config(page_title="AIDES Visual Factory", layout="wide", page_icon="🏭")

st.markdown("<h1 style='text-align: center; color: #005f73;'>🏭 محاكاة التشغيل الذكي: من المياه إلى الجبس</h1>", unsafe_allow_html=True)
st.write("---")

# روابط صور متحركة تعبيرية (يمكن استبدالها بروابط مباشرة لصور محطتكم)
img_intake = "https://cdn.dribbble.com/users/2051513/screenshots/4338902/media/6b867c296711818274640f898a96d27f.gif" # صوره سحب مياه
img_processing = "https://cdn.dribbble.com/users/59947/screenshots/5554614/media/9d63c1e29e92d9d107a61d1912953265.gif" # صورة معالجة وكهرباء
img_gypsum = "https://cdn.dribbble.com/users/1162077/screenshots/3848914/media/4e7d95d18d8a7a938c8c50c18d890b0e.gif" # صورة إنتاج وتعبئة

# زر التشغيل
if st.sidebar.button("▶️ تشغيل الدورة الإنتاجية الآن"):
    
    # --- المرحلة الأولى ---
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(img_intake, caption="1. وحدة سحب وتحليل المياه", use_column_width=True)
    with c2:
        st.info("🔍 جاري فحص الحساسات الذكية...")
        bar1 = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            bar1.progress(i + 1)
        st.write("✅ تم تحليل الملوحة: **38,000 ppm**")
    
    st.write("---")
    
    # --- المرحلة الثانية ---
    c3, c4 = st.columns([1, 2])
    with c3:
        st.image(img_processing, caption="2. وحدة الانتزاع الكهربائي (AIDES)", use_column_width=True)
    with c4:
        st.warning("⚡ جاري ضبط الجهد الكهربائي ومنع الترسيب...")
        bar2 = st.progress(0)
        for i in range(100):
            time.sleep(0.03)
            bar2.progress(i + 1)
        st.write("✅ الجهد التشغيلي الحالي: **1.45 Volt**")

    st.write("---")

    # --- المرحلة الثالثة ---
    c5, c6 = st.columns([1, 2])
    with c5:
        st.image(img_gypsum, caption="3. وحدة بلورة واستخراج الجبس", use_column_width=True)
    with c6:
        st.success("🏗️ جاري ترسيب الجبس ونقله للمخازن...")
        bar3 = st.progress(0)
        for i in range(100):
            time.sleep(0.04)
            bar3.progress(i + 1)
        st.write("✅ كمية الإنتاج: **12.5 طن/ساعة**")
        st.balloons()

else:
    st.info("👈 اضغط على زر التشغيل في القائمة الجانبية لبدء المحاكاة الحركية للمحطة.")

# أرشيف البيانات المعتاد في الأسفل لتوثيق العمل
with st.expander("📂 أرشيف سجلات التشغيل الرقمي"):
    st.write("هنا تظهر بيانات ملف الإكسل الخاص بك (REQ/MNT/LAB)")
