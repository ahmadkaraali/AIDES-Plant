import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Smart Assistant", layout="wide", page_icon="🚀")

# Top Header Styling
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🚀 Smart Assistant - Digital Archiving Platform</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar for Data Management
st.sidebar.header("📂 Data Management")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Reading the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Success message
    st.success("✅ Data loaded successfully!")
    
    # KPIs / Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        # Checking for 'Status' or 'الحالة' column
        status_col = 'Status' if 'Status' in df.columns else ('الحالة' if 'الحالة' in df.columns else None)
        if status_col:
            completed = len(df[df[status_col].astype(str).str.contains('Completed|مكتمل', case=False)])
            st.metric("Completed Requests", completed)
    
    # Interactive Filtering
    st.subheader("🔍 Smart Search (REQ / MNT / LAB)")
    search_query = st.text_input("Enter code or department to search:")
    
    if search_query:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

    # Visual Analytics
    st.write("---")
    st.subheader("📊 Real-time Analytics")
    
    # Checking for 'Department' or 'القسم' column for the chart
    dept_col = 'Department' if 'Department' in df.columns else ('القسم' if 'القسم' in df.columns else None)
    
    if dept_col:
        fig = px.pie(df, names=dept_col, title='Request Distribution by Department')
        st.plotly_chart(fig)
else:
    # Welcome screen
    st.info("👋 Welcome Dr. Ahmed. Please upload an Excel file to start analyzing your data.")
    st.image("https://via.placeholder.com/800x400.png?text=Smart+Assistant+Ready+to+Work", use_column_width=True)

# Footer
st.write("---")
st.caption("Developed by Dr. Ahmed - Smart Assistant 2026")
