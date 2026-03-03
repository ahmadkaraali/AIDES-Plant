import streamlit as st

# --- 1. المحرك الهندسي ---
class AIDESEngine:
    def __init__(self, prof):
        self.thr = 0.8 if prof == 'Seawater' else 0.6
        self.f = 1.2 if prof == 'Seawater' else 2.0

    def calculate(self, tds, temp):
        si = (tds/100000) * 0.05 * self.f * (1 + (temp-25)*0.01) / 2.4e-5
        risk = si > self.thr
        v = 1.5 if not risk else 1.2
        gyp = (tds/1000) * 0.012
        h = 100 if not risk else 100 - (si - self.thr) * 40
        cip = int(120 - (tds/1000)) if risk else 450
        return si, risk, v, gyp, h, cip

# --- 2. الإعدادات والستايل النافر ---
st.set_page_config(page_title='AIDES Smart Assistant', layout='wide')

st.markdown('<style>', unsafe_allow_html=True)
st.markdown('body { background-color: #10141d; color: white; }', unsafe_allow_html=True)
st.markdown('.card { padding: 30px; border-radius: 20px; background: #10141d; text-align: center; }', unsafe_allow_html=True)
st.markdown('.card { box-shadow: 10px 10px 20px #080a0f, -10px -10px 20px #181e2b; margin: 15px; border: 1px solid #1d2331; }', unsafe_allow_html=True)
st.markdown('</style>', unsafe_allow_html=True)

st.title('🛡️ مساعدك الذكي: AIDES Digital Twin')

with st.sidebar:
    st.header('Settings')
    tds_in = st.slider('TDS (ppm)', 5000, 100000, 45000)
    temp_in = st.slider('Temp (C)', 15, 50, 25)
    prof = st.selectbox('Sector', ['Seawater', 'Produced Water', 'Industrial'])
    run = st.button('🚀 Run System')

if run:
    eng = AIDESEngine(prof)
    si, risk, v, gyp, h, cip = eng.calculate(tds_in, temp_in)
    
    # صف المؤشرات العلوية
    m1, m2, m3 = st.columns(3)
    m1.metric('Saturation Index', f'{si:.2f}')
    m2.metric('Voltage', f'{v:.2f} V')
    m3.metric('Gypsum T/h', f'{gyp:.3f}')

    st.markdown('---')
    
    # صف البطاقات الثلاثية الأبعاد
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#00ffcc">PHASE 1</h2>', unsafe_allow_html=True)
        st.markdown('<p>INTAKE SYSTEM</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        clr = '#ff4b4b' if risk else '#00ffcc'
        st.markdown(f'<div class="card" style="border-top: 5px solid {clr}">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:{clr}">PHASE 2</h2>', unsafe_allow_html=True)
        st.markdown(f'<p>Health: {h:.1f}%</p>', unsafe_allow_html=True)
        st.markdown(f'<p>CIP: {cip} hours</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#cc99ff">PHASE 3</h2>', unsafe_allow_html=True)
        st.markdown('<p>GYPSUM RECOVERY</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.success('✅ Analysis Complete!')
