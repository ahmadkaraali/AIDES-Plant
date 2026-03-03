import streamlit as st

# --- 1. المحرك الهندسي للهوية الذكية ---
class AIDESEngine:
    def __init__(self, profile):
        self.K_SP = 2.4e-5
        self.threshold = 0.8 if profile == 'Seawater' else 0.6
        self.factor = 1.2 if profile == 'Seawater' else 2.0
        self.flow_rate = 150 

    def calculate(self, tds, temp):
        ca = (tds / 100000) * 0.02 * self.factor
        so4 = (tds / 100000) * 0.03 * self.factor
        ion_p = ca * so4
        temp_f = 1 + (temp - 25) * 0.01
        si = ion_p / (self.K_SP * temp_f)
        risk = si > self.threshold
        voltage = 1.5 if not risk else 1.25
        gyp_tons = self.flow_rate * (tds / 1000) * 0.00008
        health_val = 100 if not risk else 100 - (si - self.threshold) * 50
        cip_val = int(120 - (tds/1000)) if risk else 450
        return si, risk, voltage, gyp_tons, health_val, cip_val

# --- 2. إعدادات الواجهة وتصميم الـ 3D النافر ---
st.set_page_config(page_title='AIDES Smart Assistant', layout='wide')

st.markdown('''
    <style>
    .stApp { background-color: #10141d; color: #e6edf3; }
    [data-testid='stMetricValue'] { color: #00ffcc !important; font-weight: bold; }
    
    .neumorphic-card {
        padding: 25px;
        border-radius: 20px;
        background: #10141d;
        box-shadow: 9px 9px 18px #080a0f, -9px -9px 18px #181e2b;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.03);
    }
    
    .floating-rocket {
        width: 100px;
        filter: drop-shadow(0 0 10px #00ffcc);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
    ''', unsafe_allow_html=True)

st.title('🛡️ مساعدك الذكي: AIDES Digital Twin')
st.write('نظام المحاكاة الذكي لإدارة عمليات التحلية والصيانة التنبؤية')

with st.sidebar:
    st.header('⚙️ Operational Settings')
    tds_in = st.slider('Feedwater TDS (ppm)', 5000, 100000, 45000)
    temp_in = st.slider('Temperature (C)', 15, 50, 25)
    prof = st.selectbox('Sector', ['Seawater', 'Produced Water', 'Industrial'])
    run = st.button('🚀 تشغيل النظام (Run System)')

if run:
    eng = AIDESEngine(prof)
    si, risk, v, gyp, h, c = eng.calculate(tds_in, temp_in)
    
    m1, m2, m3 = st.columns(3)
    m1.metric('Saturation Index', f'{si:.4f}')
    m2.metric('Voltage', f'{v:.2f} V')
    m3.metric('Gypsum Yield', f'{gyp:.3f} T/h')

    st.divider()
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='neumorphic-card'><img src='https://cdn.pixabay.com/animation/2023/06/13/15/12/15-12-47-323_512.gif' class='floating-rocket'><h3>PHASE 1</h3><p>INTAKE</p></div>", unsafe_allow_html=True)
            
    with c2:
        color_code = '#ff4b4b' if risk else '#00ffcc'
        st.markdown(f"<div class='neumorphic-card' style='border-top: 5px solid {color_code};'><h1 style='font-size: 50px;'>⚡</h1><h3>
