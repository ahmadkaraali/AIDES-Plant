import streamlit as st
import time
import pandas as pd

# 1. إعدادات المنصة
st.set_page_config(page_title="AIDES Operator Control", layout="wide", page_icon="⚙️")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .ai-badge { background-color: #e1f5fe; color: #01579b; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 20px; border: 1px solid #b3e5fc; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕹️ مركز التحكم التفاعلي للمشغل - نظام AIDES")
st.write("---")

# 2. لوحة تحكم المشغل في القائمة الجانبية
st.sidebar.header("🛠️ خيارات التحكم")
op_mode = st.sidebar.radio("اختر نمط التشغيل:", ["التحكم الذكي (AI Auto)", "التحكم اليدوي (Manual)"])
input_tds = st.sidebar.slider("تحديد ملوحة المياه (ppm):", 5000, 70000, 35000)
input_flow = st.sidebar.slider("معدل التدفق (m³/h):", 50, 500, 150)
start_op = st.sidebar.button("🚀 تنفيذ الأوامر التشغيلية")

# 3. منطق الحسابات (AI Logic)
# تم توحيد اسم المتغير هنا لمنع الخطأ
if op_mode == "التحكم الذكي (AI Auto)":
    current_voltage = 1.2 + (input_tds / 50000)
    ai_msg = "✅ نظام الذكاء الاصطناعي يدير الجهد الآن لضمان أعلى كفاءة."
else:
    current_voltage = st.sidebar.number_input("تحديد الجهد يدوياً (Volt):", 0.5, 5.0, 1.5)
    ai_msg = "⚠️ تنبيه: التحكم الآن في يد المشغل (نمط يدوي)."

# حساب إنتاج الجبس بناءً على المدخلات
# استخدمنا اسم واحد فقط وهو gyp_calc
gyp_calc = (input_tds * input_flow) / 500000

# 4. العرض التفاعلي عند الضغط على الزر
if start_op:
    st.markdown(f"<div class='ai-badge'>{ai_msg}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📦 **مدخلات التشغيل**")
        st.metric("الملوحة المحددة", f"{input_tds:,} ppm")
        st.metric("التدفق الحالي", f"{input_flow} m³/h")

    with col2:
        st.warning("⚡ **حالة المعالجة**")
        st.metric("الجهد المطبق", f"{current_voltage:.2f} V")
        if input_tds > 50000:
            st.error("❗ ملوحة عالية جداً")
        else:
            st.success("💎 ظروف تشغيل مثالية")

    with col3:
        st.success("🏗️ **مخرجات الإنتاج**")
        st.metric("إنتاج الجبس المتوقع", f"{gyp_calc:.2f} طن/س")
        st.metric("العائد التقديري", f"${gyp_calc * 120:.0f}")

    st.balloons()
else:
    st.info("💡 قم بضبط الإعدادات من القائمة الجانبية ثم اضغط 'تنفيذ الأوامر' لبدء المحاكاة.")

# 5. سجل الأرشفة
st.write("---")
with st.expander("📂 سجل سجلات التشغيل (Data Log)"):
    log_data = {
        'البارامتر': ['نمط التشغيل', 'الملوحة', 'التدفق', 'الجهد', 'الإنتاج'],
        'القيمة الحالية': [op_mode, f"{input_tds} ppm", f"{input_flow} m3/h", f"{current_voltage:.2f} V", f"{gyp_calc:.2f} طن/س"]
    }
    st.table(pd.DataFrame(log_data))

st.caption("نظام مساعدك الذكي - تطوير د. أحمد 2026")
