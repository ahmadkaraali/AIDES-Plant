import streamlit as st
import time
import pandas as pd

# --- النواة الهندسية (AIDES Control Engine) ---
class AIDESProfile:
    def __init__(self, name, scaling_factor, cleaning_threshold, base_voltage, max_voltage):
        self.name = name
        self.scaling_factor = scaling_factor
        self.cleaning_threshold = cleaning_threshold
        self.base_voltage = base_voltage
        self.max_voltage = max_voltage

class AIDESControlEngine:
    def __init__(self, profile):
        self.profile = profile
        self.K_SP_GYPSUM = 2.4e-5

    def calculate_scaling_risk(self, tds, temp):
        # تقدير كيميائي بناءً على معادلاتك
        ca_conc = (tds / 100000) * 0.02 * self.profile.scaling_factor
        so4_conc = (tds / 100000) * 0.03 * self.profile.scaling_factor
        ion_product = ca_conc * so4_conc
        temp_factor = 1 + (temp - 25) * 0.01
        
        saturation_index = ion_product / (self.K_SP_GYPSUM * temp_factor)
        
        if saturation_index > self.profile.cleaning_threshold:
            return "CRITICAL_SCALING_RISK", saturation_index
        return "SAFE", saturation_index

    def optimize_voltage(self, tds, risk_status):
        target_voltage = self.profile.base_voltage
        if tds > 40000:
            target_voltage += (tds - 40000) * 0.00005
        
        if risk_status == "CRITICAL_SCALING_RISK":
            target_voltage *= 0.85  # خفض الجهد لمنع الترسيب
        
        return min(target_voltage, self.profile.max_voltage)

# --- واجهة المستخدم (The Convincing UI) ---
st.set_page_config(page_title="AIDES Advanced Control", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>AIDES Industrial Digital Twin</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>نظام التحكم الذكي المبني على كود (PLC/SCADA) الخاص ببراءة الاختراع</p>", unsafe_allow_html=True)

# القائمة الجانبية لإدخال البيانات الحقيقية
with st.sidebar:
    st.header("⚙️ مدخلات الحساسات اللحظية")
    tds = st.slider("ملوحة المياه (TDS) ppm", 5000, 100000, 45000)
    temp = st.slider("درجة الحرارة (°C)", 10, 60, 25)
    
    st.write("---")
    st.header("🔬 بروفايل المحطة")
    profile_type = st.selectbox("نوع مياه التغذية:", ["Seawater", "Produced Water"])
    
    # تعريف البروفايلات بناءً على كودك
    if profile_type == "Seawater":
        profile = AIDESProfile("Seawater", 1.2, 0.8, 1.5, 4.0)
    else:
        profile = AIDESProfile("Produced Water", 2.0, 0.6, 2.0, 5.0)

# تشغيل المحرك الذكي
engine = AIDESControlEngine(profile)
risk_status, s_index = engine.calculate_scaling_risk(tds, temp)
opt_voltage = engine.optimize_voltage(tds, risk_status)

# عرض النتائج بطريقة إقناعية (Dashboard)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("مؤشر التشبع (Saturation Index)", f"{s_index:.4f}")
    if risk_status == "CRITICAL_SCALING_RISK":
        st.error("⚠️ خطر ترسيب جبس عالي")
    else:
        st.success("✅ وضع آمن للترسيب")

with col2:
    st.metric("الجهد الأمثل الموجه (Optimized V)", f"{opt_voltage:.2f} V")
    st.info(f"النمط الحالي: {profile.name}")

with col3:
    gyp_yield = (tds * 0.05) / 1000  # فرضية إنتاجية
    st.metric("الإنتاج المتوقع للجبس", f"{gyp_yield:.2f} Ton/h")

st.write("---")
st.subheader("🛰️ مسار اتخاذ القرار الذكي (AI Logic Reasoning)")

# محاكاة لعملية اتخاذ القرار خطوة بخطوة
with st.status("جاري تحليل البيانات الكيميائية...", expanded=True):
    time.sleep(1)
    st.write(f"1. تم سحب البيانات: الملوحة {tds} ودرجة الحرارة {temp}")
    time.sleep(1)
    st.write(f"2. حساب حاصل الإذابة الأيوني ومقارنته بـ $K_{{sp}} = 2.4 \times 10^{{-5}}$")
    time.sleep(1)
    if risk_status == "CRITICAL_SCALING_RISK":
        st.write("3. ❌ اكتشاف تخطي عتبة الترسيب! تفعيل بروتوكول الحماية (Power Reduction).")
    else:
        st.write("3. ✅ المؤشرات ضمن النطاق. الحفاظ على كفاءة الانتزاع القصوى.")
    time.sleep(1)
    st.write(f"4. الأمر النهائي الموجه للوحدة: ضبط الجهد على {opt_voltage:.2f} V")

# رسم بياني تقني
st.write("---")
st.subheader("📊 مراقبة استقرار النظام")
chart_data = pd.DataFrame({
    'Time': range(10),
    'Saturation': [s_index * (1 + (i*0.01)) for i in range(10)],
    'Voltage': [opt_voltage] * 10
})
st.line_chart(chart_data.set_index('Time'))
