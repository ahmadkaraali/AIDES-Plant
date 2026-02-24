import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# إعدادات واجهة المنصة الاحترافية
st.set_page_config(page_title="Water Desalination Smart Platform", layout="wide", page_icon="💧")

# تحسين المظهر الخارجي بلمسة صناعية
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("💧 Water Desalination Plant - Smart Control Center")
st.markdown("---")

# القائمة الجانبية للتحكم
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3105/3105807.png", width=100)
st.sidebar.title("Operational Control")
uploaded_file = st.sidebar.file_uploader("Upload Plant Operational Data (Excel)", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Plant Data Synchronized Successfully!")

    # --- القسم الأول: مؤشرات الأداء الرئيسية (KPIs) ---
    st.subheader("📊 Key Performance Indicators (KPIs)")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric(label="Total Requests", value=len(df))
    with m2:
        # البحث عن طلبات الصيانة المكتملة
        done_mnt = len(df[df.apply(lambda x: 'MNT' in str(x).upper() and 'مكتمل' in str(x), axis=1)])
        st.metric(label="Maintenance Efficiency", value=f"{done_mnt} Jobs")
    with m3:
        # البحث عن فحوصات المختبر
        lab_tests = len(df[df.apply(lambda x: 'LAB' in str(x).upper(), axis=1)])
        st.metric(label="Quality Lab Tests", value=lab_tests)
    with m4:
        st.metric(label="System Status", value="Active", delta="Operational")

    # --- القسم الثاني: التحليل البياني والخرائط الذهنية ---
    st.write("---")
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📈 Operational Trend Analysis")
        # رسم بياني يوضح توزيع العمل حسب النوع (REQ, MNT, LAB)
        df['Type'] = df.iloc[:, 0].apply(lambda x: 'Maintenance' if 'MNT' in str(x) else ('Lab' if 'LAB' in str(x) else 'Request'))
        fig_line = px.bar(df, x='Type', color='Type', title="Workload Distribution", template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("📋 Quick Action Center")
        search = st.text_input("Quick Search (Code/Status):")
        if search:
            df_search = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
            st.dataframe(df_search[['الرمز', 'البيان', 'الحالة']] if 'الرمز' in df.columns else df.head(10))
        else:
            st.info("Search by code (e.g., REQ-2026)")

    # --- القسم الثالث: جدول البيانات الكامل بنظام احترافي ---
    st.write("---")
    with st.expander("📂 View Full Archiving Logs"):
        st.dataframe(df, use_container_width=True)

else:
    # واجهة ترحيبية قوية لإقناع الشركة
    st.info("📢 Waiting for Plant Data Stream...")
    st.warning("Please upload the Excel file to activate the real-time Dashboard.")
    
    # محاكاة لما سيبدو عليه الأمر (Demo)
    st.markdown("""
    ### Why 'Your Smart Assistant'?
    * **Efficiency:** Automated tracking of maintenance (MNT) and lab (LAB) tasks [cite: 2026-02-07].
    * **Precision:** No more lost paper logs; every request (REQ) is archived digitally [cite: 2026-02-17].
    * **Decision Making:** Real-time charts to help management optimize water production [cite: 2026-02-07].
    """)

st.write("---")
st.caption("Developed by Dr. Ahmed - Smart Water Management Solution 2026")
