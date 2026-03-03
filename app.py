import streamlit as st

# --- 1. المحرك الهندسي (مع تحسين دقة الحسابات) ---
class AIDESEngine:
    def __init__(self, prof):
        self.thr = 0.8 if prof == 'Seawater' else 0.6
        self.f = 1.2 if prof == 'Seawater' else 2.0

    def calculate(self, tds, temp):
        # حساب SI بدقة هندسية
        si = (tds/100000) * 0.05 * self.f * (1 + (temp-25)*0.01) / 2.4e-5
        risk = si > self.thr
        v = 1.27 if not risk else 1.15
        gyp = (tds/1000) * 0.0116
        # منع ظهور أرقام سالبة في الصحة
        h = max(0, min(100, 100 - (si - self.thr) * 10)) if risk else 100
        cip = int(196 - (tds/10000)) if risk else 450
        return si, risk, v, gyp, h, cip

# --- 2. تصميم "غرفة التحكم" (Control Room UI) ---
st.set_page_config(page_title='AIDES Digital Twin', layout='wide')

st.markdown('''
    <style>
    /* إعادة الخلفية الداكنة الفخمة */
    .stApp { background-color: #0b101a; color: #e6edf3; }
    
    /* تنسيق أرقام المؤشرات لتكون متوهجة مثل الصورة الأولى */
    [data-testid='stMetricValue'] { 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0,255,204,0.3);
    }

    /* تصميم البطاقات النافرة 3D بالخلفية الداكنة */
    .control-card {
        padding: 30px;
        border-radius: 20px;
        background: #161b22;
        box-shadow: 10px 10px 20px #05070b, -5px -5px 15px #1c222d;
        text-align: center;
        margin: 10px;
        border: 1px solid #30363d;
        transition: 0.3s;
    }
    
    .control-card:hover { transform: translateY(-5px); border-color: #00ffcc; }
    
    h3 { color: #8b949e; font-size: 1rem !important; }
    h2 { color: #ffffff; margin-top: 10px; }
    </style>
    ''', unsafe_allow_html=True)

# العنوان بشعار الدرع كما في الصورة
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title('🛡️ مساعدك الذكي: AIDES Digital Twin')
    st.write('نظام المحاكاة الذكي لإدارة عمليات التحلية والصيانة التنبؤية')

# القائمة الجانبية (Operational Settings)
with st.sidebar:
    st.header('⚙️ Operational Settings')
    tds_in = st.slider('Feedwater TDS (ppm)', 5000, 100000, 45000)
    temp_in = st.slider('Temperature (C)', 15, 50, 25)
    prof = st.selectbox('Application Sector', ['Seawater', 'Produced Water', 'Industrial'])
    run = st.button('🚀 تشغيل النظام (Run System)')

if run:
    eng = AIDESEngine(prof)
    si, risk, v, gyp, h, cip = eng.calculate(tds_in, temp_in)
    
    # المؤشرات الرقمية (التي أحببتها في الصورة الأولى)
    m1, m2, m3 = st.columns(3)
    m1.metric('Saturation Index', f'{si:.4f}')
    m2.metric('Operating Voltage', f'{v:.2f} V')
    m3.metric('Gypsum Recovery', f'{gyp:.3f} T/h')

    st.markdown('<br>', unsafe_allow_html=True)
    
    # صف البطاقات النافرة (3D Neumorphic)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f'''<div class="control-card">
            <img src="https://cdn.pixabay.com/animation/2023/06/13/15/12/15-12-47-323_512.gif" width="80">
            <h3>PHASE 1</h3><h2>INTAKE</h2>
            <p style="color:#58a6ff">سحب المياه المالح</p>
        </div>''', unsafe_allow_html=True)
            
    with c2:
        clr = '#ff4b4b' if risk else '#00ffcc'
        st.markdown(f'''<div class="control-card" style="border-bottom: 4px solid {clr}">
            <h1 style="color:{clr}; font-size:60px;">⚡</h1>
            <h3>PHASE 2</h3><h2>TREATMENT</h2>
            <p>Health: <b style="color:{clr}">{h:.1f}%</b></p>
            <p>Next CIP: <b>{cip} hours</b></p>
        </div>''', unsafe_allow_html=True)
            
    with c3:
        st.markdown(f'''<div class="control-card">
            <h1 style="color:#cc99ff; font-size:60px;">🏗️</h1>
            <h3>PHASE 3</h3><h2>HARVESTING</h2>
            <p style="color:#d2a8ff">استرداد الجبس النقي</p>
        </div>''', unsafe_allow_html=True)
    
    st.success('✅ Analysis Complete! System is Stabilized.')
