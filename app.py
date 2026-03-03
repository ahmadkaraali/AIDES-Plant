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

# --- 2. الإعدادات والتصميم ---
st.set_page_config(page_title='Smart Assistant', layout='wide')

# ستايل ثلاثي الأبعاد (نافر) بأسطر قصيرة
st.markdown('<style>', unsafe_allow_html=True)
st.markdown('.stApp { background-color: #10141d; color: white; }', unsafe_allow_html=True)
st.markdown('.card { padding: 20px; border-radius: 15px; background: #10141d; text-align: center; border: 1px solid #30363d; }', unsafe_allow_html=True)
st.markdown('.card { box-shadow: 8px 8px 16px #080a0f, -8px -8px 16px #181e2b; margin: 10px; }', unsafe_allow_html=True)
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
    
    # المؤشرات
    c1, c2, c3 = st.columns(3)
    c1.metric('Saturation Index', f'{si:.2f}')
    c2.metric('Voltage', f'{v:.2f} V')
    c3.metric('Gypsum T/h', f'{gyp:.3f}')

    st.write('---')
    
    # المراحل الثلاث بتصميم نافذ
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image("https://cdn.pixabay.com/animation/2023/06/13/15/12/15-12-47-323_512.gif", width=100)
        st.markdown('<h3>PHASE 1</h3><p>INTAKE</p></div>', unsafe_allow_html=True)
            
    with col2:
        clr = '#ff4b4b' if risk else '#00ffcc'
        st.markdown(f'<div class="card" style="border-top: 5px solid {clr}">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:{clr}">⚡</h1>', unsafe_allow_html=True)
        st.markdown(f'<h3>PHASE 2</h3><p>Health: {h:.1f}%</p><p>CIP: {cip}h</p></div>', unsafe_allow_html=True)
            
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#cc99ff">🏗️</h1>
