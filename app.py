import streamlit as st
import time

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="AIDES Digital Twin", layout="wide")

# 2. تصميم CSS للأيقونات المجسمة (3D) والوميض المتسلسل الاحترافي
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    
    /* إطارات المراحل بتأثير نافر (3D) قوي */
    .phase-card { 
        background-color: #1a1e26; 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid #2d3436; 
        text-align: center;
        box-shadow: inset 2px 2px 5px #000, 8px 8px 20px #000; 
        min-height: 240px;
        transition: all 0.3s ease;
    }

    /* أيقونات مجسمة نافرة */
    .icon-3d {
        filter: drop-shadow(5px 5px 8px #000);
        margin-bottom: 15px;
    }

    /* وميض المرحلة النشطة - أخضر (عمل) */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
        50% { box-shadow: 0 0 30px #00ff00; border-color: #00ff00; }
        100% { box-shadow: 0 0 5px #00ff00; border-color: #2d3436; }
    }
    
    /* وميض المرحلة النشطة - برتقالي (تحضير) */
    @keyframes pulse-orange {
        0% { box-shadow: 0 0 5px #ffaa00; border-color: #2d3436; }
        50% { box-shadow: 0 0 30px #ffaa00; border-color: #ffaa00; }
        100% { box-shadow: 0 0 5px #ffaa00; border-color: #2d3436; }
    }

    .active-green { animation: pulse-green 1.2s infinite !important; }
    .active-orange { animation: pulse-orange 1.2s infinite !important; }

    .led { height: 14px; width: 14px; border-radius: 50%; display: inline-block; margin-bottom: 10px; }
    .led-green { background-color: #00ff00; box-shadow: 0 0 12px #00ff00; }
    .led-orange { background-color: #ff
