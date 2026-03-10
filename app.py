import streamlit as stimport streamlit as st
import time

# 1. إعدادات الصفحة والمظهر
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للأيقونات المجسمة (3D) والوميض المتسلسل
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    
    /* إطارات المراحل مجسمة */
    .phase-card { 
        background-color: #1a1e26; 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid #2d3436; 
        text-align: center;
        box-shadow: inset 2px 2px 5px #000, 5px 5px 15px #000; /* تأثير النفر والبروز */
        min-height: 220px;
    }

    /* أيقونات نافرة ثلاثية الأبعاد */
    .icon-3d {
        filter: drop-shadow(3px 3px 5px #000);
        transition: transform 0.3s;
    }

    /* أنيميشن الوميض القوي للمرحلة النشطة */
    @keyframes fast-blink {
        0% { opacity: 1; box-shadow: 0 0 20px #00ff00; border-color: #00ff00; }
        50% { opacity: 0.5; box-shadow: 0 0 5px #333; border-color: #2d3436; }
        100% { opacity: 1; box-shadow: 0 0 20px #00ff00; border-color: #00ff00; }
    }
    .active-step { animation: fast-blink 1s infinite !important; }

    .led { height: 15px; width: 15px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
    .led-off { background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ تحكم العمليات")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    start_sim = st.button("🚀 بدء دورة التشغيل (START CYCLE)")

# 4. منطق التسلسل الزمني (Sequence Logic)
step = 0
if start_sim:
    # محاكاة مرور الوقت بين المراحل لإقناع الخبير
    placeholder = st.empty()
    for s in range(1, 4):
        # تحديث الحالة لكل مرحلة
        c1, c2, c3 = st.columns(3)
        
        with c1: # المرحلة الأولى
            is_active = "active-step" if s == 1 else ""
            led = "led-green" if s >= 1 else "led-off"
            st.markdown(f'<div class="phase-card {is_active}"><div class="led {led}"></div><div style="font-size:18px; font-weight:bold;">PHASE 1</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="50"><p>{"جاري السحب..." if s==1 else "تم السحب" if s>1 else "استعداد"}</p></div>', unsafe_allow_html=True)
        
        with c2: # المرحلة الثانية
            is_active = "active-step" if s == 2 else ""
            led = "led-green" if s >= 2 else "led-off"
            st.markdown(f'<div class="phase-card {is_active}"><div class="led {led}"></div><div style="font-size:18px; font-weight:bold;">PHASE 2</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width="50"><p>{"جاري المعالجة..." if s==2 else "تم الفصل" if s>2 else "انتظار التدفق"}</p></div>', unsafe_allow_html=True)
            
        with c3: # المرحلة الثالثة
            is_active = "active-step" if s == 3 else ""
            led = "led-green" if s >= 3 else "led-off"
            st.markdown(f'<div class="phase-card {is_active}"><div class="led {led}"></div><div style="font-size:18px; font-weight:bold;">PHASE 3</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2312/2312701.png" width="50"><p>{"جاري الحصاد..." if s==3 else "بانتظار المنتج"}</p></div>', unsafe_allow_html=True)
        
        time.sleep(2) # انتظار ثانيتين بين كل مرحلة لبيان العمل
        if s < 3: st.rerun() # إعادة التشغيل للانتقال للمرحلة التالية

# 5. عرض العدادات (تظهر عند الانتهاء أو الاستعداد)
if not start_sim:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("الضغط التشغيلي", f"{tds * 0.025:.2f} bar")
    with c2: st.metric("Voltage", "0.00 V")
    with c3: st.metric("إنتاج NaCl", "0.000 T/h")
    with c4: st.metric("إنتاج الجبس", "0.000 T/h")
    
    st.write("---")
    # عرض الحالة الافتراضية
    col1, col2, col3 = st.columns(3)
    for col, name, img in zip([col1, col2, col3], ["INTAKE", "TREATMENT", "HARVESTING"], ["1034410", "2807530", "2312701"]):
        with col: st.markdown(f'<div class="phase-card"><div class="led led-off"></div><div style="font-size:18px; font-weight:bold;">{name}</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/{img}/{img}.png" width="50"><p>وضع الاستعداد</p></div>', unsafe_allow_html=True)
import time

# 1. إعدادات الصفحة والمظهر
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للأيقونات المجسمة (3D) والوميض المتسلسل
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    
    /* إطارات المراحل مجسمة */
    .phase-card { 
        background-color: #1a1e26; 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid #2d3436; 
        text-align: center;
        box-shadow: inset 2px 2px 5px #000, 5px 5px 15px #000; /* تأثير النفر والبروز */
        min-height: 220px;
    }

    /* أيقونات نافرة ثلاثية الأبعاد */
    .icon-3d {
        filter: drop-shadow(3px 3px 5px #000);
        transition: transform 0.3s;
    }

    /* أنيميشن الوميض القوي للمرحلة النشطة */
    @keyframes fast-blink {
        0% { opacity: 1; box-shadow: 0 0 20px #00ff00; border-color: #00ff00; }
        50% { opacity: 0.5; box-shadow: 0 0 5px #333; border-color: #2d3436; }
        100% { opacity: 1; box-shadow: 0 0 20px #00ff00; border-color: #00ff00; }
    }
    .active-step { animation: fast-blink 1s infinite !important; }

    .led { height: 15px; width: 15px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 10px #00ff00; }
    .led-off { background-color: #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇧🇭 AIDES Digital Twin :مساعدك الذكي")

# 3. لوحة التحكم الجانبية
with st.sidebar:
    st.header("⚙️ تحكم العمليات")
    tds = st.slider("ملوحة مياه التغذية (ppm)", 10000, 60000, 45000)
    start_sim = st.button("🚀 بدء دورة التشغيل (START CYCLE)")

# 4. منطق التسلسل الزمني (Sequence Logic)
step = 0
if start_sim:
    # محاكاة مرور الوقت بين المراحل لإقناع الخبير
    placeholder = st.empty()
    for s in range(1, 4):
        # تحديث الحالة لكل مرحلة
        c1, c2, c3 = st.columns(3)
        
        with c1: # المرحلة الأولى
            is_active = "active-step" if s == 1 else ""
            led = "led-green" if s >= 1 else "led-off"
            st.markdown(f'<div class="phase-card {is_active}"><div class="led {led}"></div><div style="font-size:18px; font-weight:bold;">PHASE 1</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/1034/1034410.png" width="50"><p>{"جاري السحب..." if s==1 else "تم السحب" if s>1 else "استعداد"}</p></div>', unsafe_allow_html=True)
        
        with c2: # المرحلة الثانية
            is_active = "active-step" if s == 2 else ""
            led = "led-green" if s >= 2 else "led-off"
            st.markdown(f'<div class="phase-card {is_active}"><div class="led {led}"></div><div style="font-size:18px; font-weight:bold;">PHASE 2</div><img class="icon-3d" src="https://cdn-icons-png.flaticon.com/512/2807/2807530.png" width
