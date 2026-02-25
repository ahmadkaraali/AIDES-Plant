import streamlit as st
import time
import pandas as pd

# 1. إعدادات المنصة
st.set_page_config(page_title="AIDES Intelligent Workflow", layout="wide", page_icon="🧠")

# تنسيق CSS (إصلاح شامل لكافة الأخطاء السابقة)
st.markdown("""
    <style>
    .active-step { border: 2px solid #0077b6; background-color: #e1f5fe; border-radius: 15px; padding: 20px; box-shadow: 0px 0px 15px #0077b6; margin-bottom: 10px; }
    .ai-decision-box { background-color: #1a1a1a; color: #00ff00; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; margin: 10px 0; font-size: 14px; border-left: 5px solid #00ff00; }
    .status-badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; background-color: #ffd166; color: #000; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 نظام التدفق الذكي المتسلسل (AIDES Engine)")
st.write("---")

# 2. لوحة تحكم المشغل في القائمة الجانبية
st.sidebar.header("🕹️ لوحة تحكم القائد")
input_tds = st.sidebar.slider("تركيز الملوحة (ppm):", 5000, 70000, 35000)

# أزرار التشغيل والإطفاء
col_btn1, col_btn2 = st.sidebar.columns(2)
start_process = col_btn1.button("🚀 تشغيل")
stop_process = col_btn2.button("🛑 إطفاء")

# الروابط البصرية
ICON_INTAKE = "https://cdn.dribbble.com/users/135061/screenshots/4332560/media/765089c23577317e1451e5e0500411a7.gif"
ICON_AI = "https://cdn.dribbble.com/users/244440/screenshots/2361250/media/1d9b324391672323e98188172828b1a9.gif"
ICON_PROD = "https://cdn.dribbble.com/users/1162077/screenshots/3848914/media/4e7d95d18d8a7a938c8c50c18d890b0e.gif"

# 3. منطق التشغيل
if start_process and not stop_process:
    # حاويات فارغة للتعبئة المتسلسلة
    p1 = st.empty()
    p_ai_1 = st.empty()
    p2 = st.empty()
    p_ai_2 = st.empty()
    p3 = st.empty()
    final_report = st.empty()

    # --- المرحلة 1 ---
    with p1.container():
        st.markdown("<div class='active-step'>", unsafe_allow_html=True)
        ca, cb = st.columns([1, 4])
        ca.image(ICON_INTAKE, width=80)
        cb.subheader("المرحلة 1: سحب وتحليل مياه التغذية")
        cb.write(f"🔍 يتم الآن فحص الأيونات... الملوحة الحالية: **{input_tds:,} ppm**")
        st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- قرار الذكاء الاصطناعي 1 ---
    p_ai_1.markdown(f"""<div class='ai-decision-box'>
    [AI-SYSTEM]: تم تحليل عينة المياه.. مخاطر الترسيب متوسطة. <br>
    [AI-SYSTEM]: تم حساب القطبية المطلوبة: {(1.2 + input_tds/50000):.2f}V. <br>
    [AI-SYSTEM]: إرسال الأوامر لوحدة المعالجة... ✅
    </div>""", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- المرحلة 2 ---
    with p2.container():
        st.markdown("<div class='active-step'>", unsafe_allow_html=True)
        cc, cd = st.columns([1, 4])
        cc.image(ICON_AI, width=80)
        cd.subheader("المرحلة 2: معالجة AIDES (الانتزاع الكهربائي)")
        cd.write("⚡ يتم الآن سحب الأيونات وتعديل ملوحة المياه وتوجيه الكبريتات.")
        st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- قرار الذكاء الاصطناعي 2 ---
    p_ai_2.markdown("""<div class='ai-decision-box'>
    [AI-SYSTEM]: استقرار التيار الكهربائي بنسبة 99.8%. <br>
    [AI-SYSTEM]: تجميع بلورات كبريتات الكالسيوم جارٍ.. <br>
    [AI-SYSTEM]: فتح صمامات خط إنتاج الجبس... ✅
    </div>""", unsafe_allow_html=True)
    time.sleep(1.5)

    # --- المرحلة 3 ---
    with p3.container():
        st.markdown("<div class='active-step'>", unsafe_allow_html=True)
        ce, cf = st.columns([1, 4])
        ce.image(ICON_PROD, width=80)
        cf.subheader("المرحلة 3: استعادة الجبس النهائي")
        gyp = (input_tds * 150) / 500000
        cf.write(f"🏗️ معدل الاستعادة الحالي: **{gyp:.2f} طن/ساعة**")
        st.markdown("</div>", unsafe_allow_html=True)
    time.sleep(1)

    # --- التقرير النهائي ---
    final_report.markdown(f"""
        <div style="padding:20px; border:2px solid #1e7e34; background-color: #d4edda; border-radius: 10px; text-align: center;">
            <h3 style="margin:0; color: #155724;">✅ اكتملت الدورة بنجاح</h3>
            <p>تم أرشفة البيانات برقم مرجع: <b>AIDES-2026-{int(time.time())}</b></p>
        </div>
    """, unsafe_allow_html=True)

elif stop_process:
    st.warning("🛑 تم إيقاف النظام وإعادة كافة الحساسات لوضع الاستعداد.")
    st.info("جاهز لبدء دورة تشغيل جديدة.")

else:
    st.info("💡 النظام في وضع الاستعداد.. اضغط على 'تشغيل' لبدء التسلسل الذكي.")

# 4. الأرشفة في الأسفل (ثابتة)
st.write("---")
with st.expander("📂 سجل الأرشفة الرقمية"):
    st.table(pd.DataFrame({'المسؤول': ['AI-Controller'], 'الحالة': ['Standby'], 'التوقيت': [time.strftime("%H:%M:%S")]}))

st.caption("نظام مساعدك الذكي | تطوير د. أحمد 2026")
