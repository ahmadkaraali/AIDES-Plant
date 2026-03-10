import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS محسن (أيقونات أصغر وأضواء تفاعلية)
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .phase-card { 
        background-color: #161a23; 
        padding: 15px; 
        border-radius: 15px; 
        border: 1px solid #2d3436; 
        text-align: center;
        min-height: 250px; /* تقليل الارتفاع لتناسب الشاشة */
        transition: all 0.4s ease;
    }
    .glow-green { border: 2px solid #00ff00 !important; box-shadow: 0 0 15px rgba(0,255,0,0.2); }
    .glow-orange { border: 2px solid #ffaa00 !important; box-shadow: 0 0 15px rgba(255,170,0,0.2); }
    
    .led { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-bottom: 5px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
    .led-orange { background-color: #ffaa00; box-shadow: 0 0 10px #ffaa00; }
    .led-off { background-color: #333; }
    
    .phase-name { font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    img { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ تحكم العمليات")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    # استخدام Toggle بدلاً من Button للحفاظ على الحالة
    is_running = st.toggle("تفعيل المحطة (START PLANT)", value=False)

# 4. الحسابات التشغيلية
flow = 15.0
total_min = (tds * flow) / 1000000
nacl = total_min * 0.777 if is_running else 0.0
gyp = (total_min * 0.077) * 1.79 if is_running else 0.0

# 5. العدادات العلوية (بسيطة وواضحة)
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("الضغط التشغيلي", f"{tds * 0.025:.2f} bar")
with c2: st.metric("Voltage", "1.15 V" if is_running else "0.00 V")
with c3: st.metric("إنتاج الملح NaCl", f"{nacl:.3f} T/h")
with c4: st.metric("إنتاج الجبس", f"{gyp:.3f} T/h")

st.write("---")

# 6. عرض المراحل (أيقونات مصغرة للنصف)
p1, p2, p3 = st.columns(3)

# المرحلة الأولى: السحب (أخضر عند العمل)
with p1:
    card_class = "phase-card glow-green" if is_running else "phase-card"
    led_class = "led led-green" if is_running else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-name">INTAKE</div>
            <img src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="45"> <p style="font-size:13px;">{'سحب وتدفق مياه البحر' if is_running else 'وضع الاستعداد'}</p>
        </div>
    """, unsafe_allow_html=True)

# المرحلة الثانية: المعالجة (برتقالي = تحضير أيوني)
with p2:
    # اللون البرتقالي هنا يعني "تحضير موازنة الأيونات" قبل الفصل
    card_class = "phase-card glow-orange" if is_running else "phase-card"
    led_class = "led led-orange" if is_running else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-name">TREATMENT</div>
            <img src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="45"> <p style="font-size:13px; color:#ffaa00;">{'تحضير وفصل الأيونات' if is_running else 'في انتظار التشغيل'}</p>
        </div>
    """, unsafe_allow_html=True)

# المرحلة الثالثة: الحصاد (أخضر عند العمل)
with p3:
    card_class = "phase-card glow-green" if is_running else "phase-card"
    led_class = "led led-green" if is_running else "led led-off"
    st.markdown(f"""
        <div class="{card_class}">
            <div class="{led_class}"></div>
            <div class="phase-name">HARVESTING</div>
            <img src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="45"> <p style="font-size:13px;">{'تجميع الملح والجبس' if is_running else 'بانتظار الإنتاج'}</p>
        </div>
    """, unsafe_allow_html=True)

if is_running:
    st.success("المحطة تعمل الآن: سحب مستمر -> تحضير أيوني -> حصاد المعادن")
