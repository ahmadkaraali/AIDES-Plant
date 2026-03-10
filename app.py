import streamlit as st
import time

# 1. إعدادات الصفحة والمظهر العام (Dark Mode)
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS لإطارات احترافية وأضواء LED نابضة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    /* إطارات المراحل كما في الصورة السابقة */
    .phase-card { 
        background-color: #161a23; 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid #2d3436; 
        text-align: center;
        min-height: 350px;
        transition: all 0.5s ease;
    }
    /* إضاءة النيون عند التشغيل */
    .glow-green { border: 2px solid #00ff00 !important; box-shadow: 0 0 20px rgba(0,255,0,0.3); }
    .glow-orange { border: 2px solid #ffaa00 !important; box-shadow: 0 0 20px rgba(255,170,0,0.3); }
    
    /* أزرار الإضاءة (LED Indicators) */
    .led { height: 20px; width: 20px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 15px #00ff00; }
    .led-orange { background-color: #ffaa00; box-shadow: 0 0 15px #ffaa00; }
    .led-off { background-color: #333; }
    
    .phase-label { color: #888; font-size: 14px; font-weight: bold; }
    .phase-name { font-size: 28px; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان الرئيسي
st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")
st.write("نظام المحاكاة التفاعلي لبيان خطوات الفصل الأيوني وحصاد المعادن")

# 4. لوحة التحكم الجانبية
with st.sidebar:
    st.header("🎮 تحكم المحطة")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    start_btn = st.button("🚀 إطلاق المحطة (START PLANT)")

# 5. منطق المحاكاة المتسلسلة (لإقناع الخبير)
status = "standby"
if start_btn:
    status = "running"

# 6. الحسابات التشغيلية
flow = 15.0
total_min = (tds * flow) / 1000000
nacl = total_min * 0.777 if status == "running" else 0.0
gyp = (total_min * 0.077) * 1.79 if status == "running" else 0.0

# 7. العدادات العلوية
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط التشغيلي", f"{tds * 0.025:.2f} bar")
with c2: st.metric("Operating Voltage", "1.15 V" if status == "running" else "0.00 V")
with c3: st.metric("إنتاج NaCl (الملح)", f"{nacl:.3f} T/h")
with c4: st.metric("إنتاج الجبس", f"{gyp:.3f} T/h")

st.write("---")

# 8. عرض المراحل الثلاث داخل إطارات (كما في صورتك المفضلة)
p1, p2, p3 = st.columns(3)

# المرحلة الأولى: INTAKE
with p1:
    card_class = "phase-card glow-green" if status == "running" else "phase-card"
    led_class = "led led-green" if status == "running" else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-label">PHASE 1</div>
            <div class="phase-name">INTAKE</div>
            <img src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="80">
            <p style="margin-top:20px;">{'سحب المياه نشط' if status == "running" else 'وضع الاستعداد'}</p>
        </div>
    """, unsafe_allow_html=True)

# المرحلة الثانية: TREATMENT (تأثير برتقالي ثم أخضر)
with p2:
    card_class = "phase-card glow-orange" if status == "running" else "phase-card"
    led_class = "led led-orange" if status == "running" else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-label">PHASE 2</div>
            <div class="phase-name">TREATMENT</div>
            <img src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="80">
            <p style="margin-top:20px;">{'فصل الأيونات الجاري' if status == "running" else 'في انتظار التدفق'}</p>
        </div>
    """, unsafe_allow_html=True)

# المرحلة الثالثة: HARVESTING
with p3:
    card_class = "phase-card glow-green" if status == "running" else "phase-card"
    led_class = "led led-green" if status == "running" else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-label">PHASE 3</div>
            <div class="phase-name">HARVESTING</div>
            <img src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="80">
            <p style="margin-top:20px;">{'استخلاص الملح والجبس' if status == "running" else 'بانتظار الإنتاج'}</p>
        </div>
    """, unsafe_allow_html=True)

if status == "running":
    st.success("تم تأكيد خطوات العمل: السحب -> المعالجة -> الحصاد")
