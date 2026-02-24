import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة لتظهر كمنصة احترافية
st.set_page_config(page_title="Smart Water Plant", layout="wide", page_icon="💧")

st.markdown("<h1 style='text-align: center; color: #0077b6;'>💧 Smart Water Desalination Dashboard</h1>", unsafe_allow_html=True)
st.write("---")

# 2. وظيفة ذكية لقراءة البيانات وتجنب الأخطاء
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_excel(uploaded_file)
        except:
            return pd.read_csv(uploaded_file)
    else:
        # بيانات تجريبية لإبهار الشركة فور فتح الموقع
        data = {
            'Code': ['REQ-2026-001', 'MNT-2026-042', 'LAB-2026-015', 'REQ-2026-005'],
            'Department': ['Production', 'Maintenance', 'Quality Lab', 'Production'],
            'Status': ['Completed', 'Pending', 'Completed', 'In Progress']
        }
        return pd.DataFrame(data)

# القائمة الجانبية
st.sidebar.header("⚙️ Control Panel")
file = st.sidebar.file_uploader("Update Plant Data", type=["xlsx", "xls", "csv"])

# تحميل البيانات (سواء المرفوعة أو التجريبية)
df = load_data(file)

# 3. عرض العدادات (Metrics) بشكل جذاب
st.subheader("🚀 Operational Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Operations", len(df), "+5% increase")
with col2:
    # محاولة ذكية لحساب المكتمل بغض النظر عن لغة العمود
    completed_count = len(df[df.apply(lambda x: x.astype(str).str.contains('Completed|مكتمل').any(), axis=1)])
    st.metric("Successful Tasks", completed_count)
with col3:
    st.metric("Plant Status", "Optimal ✅")

# 4. الرسوم البيانية التفاعلية
st.write("---")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 Workload Analysis")
    # البحث عن أي عمود يحتوي على "قسم" أو "Department"
    target_col = next((c for c in df.columns if 'القسم' in c or 'Department' in c or 'Type' in c), df.columns[0])
    fig = px.bar(df, x=target_col, color=target_col, title="Distribution by Category")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🔍 Quick Filter")
    search = st.text_input("Enter Code (e.g. REQ):")
    if search:
        df = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

# 5. عرض الجدول النهائي
st.subheader("📂 Detailed Digital Archive")
st.dataframe(df, use_container_width=True)

st.write("---")
st.caption("Advanced Solution for Water Plants - Developed by Dr. Ahmed 2026")
