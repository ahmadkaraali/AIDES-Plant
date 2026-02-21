import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. إعدادات الصفحة والواجهة (Page Config)
# ==========================================
st.set_page_config(page_title="منصة AIDES الذكية لمعالجة المياه", layout="wide", page_icon="🌊")

# تصميم CSS مخصص لواجهة احترافية (Dark Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .metric-card {
        background-color: #1e222d;
        border-left: 5px solid #00f2fe;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .ai-box {
        background: linear-gradient(135deg, #1a2a6c, #11998e, #38ef7d);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .stProgress > div > div > div > div {
        background-color: #00f2fe;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. اللوحة الجانبية (نظام التحكم والمدخلات)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2101/2101294.png", width=100) # أيقونة معبرة
st.sidebar.header("🎛️ وحدة التحكم المركزية (SCADA)")

system_status = st.sidebar.radio("حالة النظام:", ["تشغيل (Auto)", "إيقاف (Standby)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 إعدادات مصدر المياه")
water_source = st.sidebar.selectbox("نوع المياه المُدخلة:", 
                                    ["المياه المرتجعة (حفر الآبار - Oil&Gas)", 
                                     "مياه الخليج العربي (عالية الملوحة)", 
                                     "مياه بحر قياسية"])

# تحديد الملوحة بناءً على الاختيار مع إمكانية التعديل
default_tds = 65000 if water_source == "المياه المرتجعة (حفر الآبار - Oil&Gas)" else (55000 if water_source == "مياه الخليج العربي (عالية الملوحة)" else 35000)
inlet_tds = st.sidebar.slider("الملوحة الكلية (TDS) - PPM", min_value=10000, max_value=100000, value=default_tds, step=1000)

plant_capacity = 100 # متر مكعب باليوم ثابتة حسب طلبك

st.sidebar.markdown("---")
st.sidebar.info(f"**الاستطاعة التشغيلية:** {plant_capacity} م³/يوم")

# ==========================================
# 3. محاكاة البيانات والحسابات الرياضية
# ==========================================
# محاكاة قراءات الحساسات (إضافة تذبذب طفيف للواقعية)
live_tds = inlet_tds + np.random.randint(-500, 500)
live_temp = 32.5 + np.random.uniform(-1, 1)
live_ph = 6.8 + np.random.uniform(-0.2, 0.2)
# الجهد الكهربائي حسب التقرير أقل من 1.2 فولت لوحدة CDI
cdi_voltage = 1.1 + np.random.uniform(-0.05, 0.05) 

# حسابات إنتاج الجبس (افتراض: الجبس يشكل نسبة مئوية من الملوحة العالية)
# معادلة تقريبية: التدفق (100) * الملوحة (غرام/متر مكعب) * نسبة ترسب الجبس المستهدفة
gypsum_ratio = 0.08 # افتراض أن 8% من الأملاح هي كبريتات كالسيوم قابلة للاستخلاص
daily_gypsum_kg = (plant_capacity * live_tds * gypsum_ratio) / 1000 

# حسابات استهلاك الطاقة (CDI مقابل RO)
energy_cdi_kwh = plant_capacity * 1.5 # 1.5 كيلو واط للمتر المكعب
energy_ro_kwh = plant_capacity * 4.5  # 4.5 كيلو واط للـ RO التقليدي
energy_saved = energy_ro_kwh - energy_cdi_kwh

# ==========================================
# 4. بناء واجهة المستخدم الرئيسية (التبويبات)
# ==========================================
st.title("🌊 منصة AIDES: نظام الانتزاع الكهربائي الموجه بالذكاء الاصطناعي")
st.markdown("لوحة تحكم تفاعلية لمحطة معالجة المياه بإنتاجية **100 متر مكعب/اليوم** واستخلاص الجبس.")

tab1, tab2, tab3, tab4 = st.tabs(["📊 المراقبة الحية (Sensors)", "🧠 محرك الذكاء الاصطناعي (AI Core)", "⚙️ عملية الانتزاع (CDI) واستخلاص الجبس", "💰 العائد الاقتصادي والقيمة المضافة"])

# ------------------------------------------
# التبويب الأول: المراقبة الحية
# ------------------------------------------
with tab1:
    st.header("بيانات الحساسات في الوقت الفعلي (Real-Time Sensors)")
    
    if system_status == "إيقاف (Standby)":
        st.warning("النظام حالياً في وضع الاستعداد. يرجى تحويل الحالة إلى (تشغيل) من اللوحة الجانبية.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""<div class='metric-card'>
            <h4>معدل التدفق (Flow)</h4>
            <h2>{plant_capacity} m³/d</h2>
            <span style='color:#00f2fe'>حالة مستقرة ✅</span></div>""", unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""<div class='metric-card'>
            <h4>الملوحة (TDS)</h4>
            <h2>{live_tds:,} ppm</h2>
            <span style='color:{"#ff4b4b" if live_tds > 60000 else "#00f2fe"}'>{"تحذير: ملوحة شديدة" if live_tds > 60000 else "طبيعي"}</span></div>""", unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""<div class='metric-card'>
            <h4>الحرارة (Temp)</h4>
            <h2>{live_temp:.1f} °C</h2>
            <span style='color:#00f2fe'>طبيعي ✅</span></div>""", unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""<div class='metric-card'>
            <h4>الأس الهيدروجيني (pH)</h4>
            <h2>{live_ph:.2f}</h2>
            <span style='color:#00f2fe'>متوازن ✅</span></div>""", unsafe_allow_html=True)

        # رسم بياني تفاعلي للملوحة
        st.subheader("تحليل مؤشر الملوحة الكلية")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = live_tds,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "PPM (جزء في المليون)"},
            gauge = {
                'axis': {'range': [None, 100000]},
                'bar': {'color': "#00f2fe"},
                'steps' : [
                    {'range': [0, 35000], 'color': "#2b2b2b"},
                    {'range': [35000, 60000], 'color': "#555555"},
                    {'range': [60000, 100000], 'color': "#882222"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 85000}
            }))
        fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
        st.plotly_chart(fig_gauge, use_container_width=True)

# ------------------------------------------
# التبويب الثاني: محرك الذكاء الاصطناعي
# ------------------------------------------
with tab2:
    st.header("التنبؤ والتحكم الذكي (AI-Driven Control)")
    
    scaling_risk = "مرتفع جداً (حرج)" if live_tds > 70000 else ("متوسط إلى مرتفع" if live_tds > 45000 else "منخفض")
    
    st.markdown(f"""
    <div class='ai-box'>
        <h2>🤖 قرار الذكاء الاصطناعي (AI Decision Engine)</h2>
        <p style="font-size: 1.2rem;">التنبؤ بخطر ترسب الجبس (Scaling Risk): <b>{scaling_risk}</b></p>
        <hr/>
        <h3>الإجراء المتخذ آلياً:</h3>
        <p style="font-size: 1.1rem;">توجيه تيار النفايات المركز (Brine) مباشرة إلى <b>مفاعل التبلور الموجه</b> لمنع انسداد خطوط الحقن وتآكل المعدات.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.info("**محرك التحسين (Optimization Engine):**\n\n تم ضبط جهد أقطاب النانو عند **{:.2f} فولت** لضمان الإزالة الانتقائية للأيونات ثنائية التكافؤ (الكالسيوم والكبريتات) بأقل استهلاك للطاقة.".format(cdi_voltage))
    with c2:
        st.warning("**محاكي العمليات (Plant Process Simulator):**\n\n تم تنشيط النمط الخاص بـ **{}** لضبط حساسية الأقطاب.".format(water_source.split('(')[0]))

# ------------------------------------------
# التبويب الثالث: الانتزاع الكهربائي والجبس
# ------------------------------------------
with tab3:
    st.header("إنتاج الجبس ذو القيمة المضافة (Directed Crystallization)")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.metric(label="كمية الجبس المتوقعة (يومياً)", value=f"{daily_gypsum_kg:,.1f} كغ", delta="بلورات نقية عالية الجودة")
        st.metric(label="جهد وحدة (CDI)", value=f"{cdi_voltage:.2f} V", delta="جهد منخفض جداً", delta_color="inverse")
        
    with col_b:
        st.subheader("محاكاة دورة استخلاص الجبس")
        st.write("نسبة تشبع الحوض وبدء التبلور الميكانيكي:")
        progress_val = min(100, int((live_tds / 80000) * 100))
        st.progress(progress_val)
        st.write(f"نسبة التركيز في تيار النفايات (Brine) وصلت إلى **{progress_val}%** من حد التبلور المثالي.")
        
        st.success("""
        **آلية العمل المطبقة (حسب المرفقات):**
        1. الإزالة الكهروكيميائية الانتقائية عبر جسيمات النانو المعدّلة.
        2. التوجيه الذكي للـ Brine إلى مفاعل التبلور.
        3. تنشيط ظروف مثالية لنمو بلورات الجبس لتسهيل فصلها ميكانيكياً (بدون إنزيمات معقدة).
        """)

# ------------------------------------------
# التبويب الرابع: العائد الاقتصادي والتوفير
# ------------------------------------------
with tab4:
    st.header("مقارنة الكفاءة والتكاليف (ROI & Value Addition)")
    
    # حسابات الأرباح
    price_per_ton_gypsum = 45 # دولار للطن كمثال
    daily_revenue = (daily_gypsum_kg / 1000) * price_per_ton_gypsum
    annual_revenue = daily_revenue * 330 # افتراض 330 يوم عمل
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.subheader("🔋 توفير الطاقة (طريقة AIDES مقابل RO)")
        df_energy = pd.DataFrame({
            "التقنية": ["التناضح العكسي (RO)", "نظام AIDES (CDI)"],
            "استهلاك الطاقة (kWh/day)": [energy_ro_kwh, energy_cdi_kwh]
        })
        fig_bar = px.bar(df_energy, x="التقنية", y="استهلاك الطاقة (kWh/day)", color="التقنية",
                         color_discrete_map={"التناضح العكسي (RO)": "#ff4b4b", "نظام AIDES (CDI)": "#00f2fe"})
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.write(f"💡 توفير يومي للطاقة مقداره: **{energy_saved:,.0f} كيلو واط ساعي**")

    with col_y:
        st.subheader("💵 القيمة المضافة (إيرادات الجبس)")
        st.markdown(f"""
        <div style='background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #38ef7d;'>
            <h3 style='color: #38ef7d;'>الإيرادات السنوية المتوقعة من بيع الجبس الثانوي</h3>
            <h1 style='color: white;'>$ {annual_revenue:,.2f}</h1>
            <p>يمكن توجيه هذا المنتج لمصانع الأسمنت أو الأسمدة، مما يحول <b>تكلفة التخلص من النفايات</b> إلى <b>مصدر إيرادات جزئي</b> يتوافق مع أهداف الاستدامة.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        st.info("📉 **انخفاض تكاليف التشغيل (OPEX):** لا حاجة لاستخدام مواد كيميائية باهظة (فقط حقن نانوي دقيق)، وتقليل فترات التوقف (Downtime) الناتجة عن تآكل المعدات.")

st.markdown("---")
st.caption("تم تصميم هذه المنصة بناءً على متطلبات مشروع تقرير نظام AIDES - تنفيذ الهيكل العظمي الذكي ووحدة الربط الصناعي (PLC Interface).")