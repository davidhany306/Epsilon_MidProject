import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="🛒 Retail Dashboard", layout="wide")

# --- Title ---
st.title("🛍️ Retail Store Sales Dashboard")
st.markdown("Explore sales trends, customer behavior, and product insights.")

# --- File Upload ---
uploaded_file = st.file_uploader("retail_store_sales.csv", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Preprocessing ---
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
    df['year'] = df['Transaction Date'].dt.year
    df['month'] = df['Transaction Date'].dt.month_name()
    df['day'] = df['Transaction Date'].dt.day
    df['YearMonth'] = df['Transaction Date'].dt.to_period('M').astype(str)

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filters")
    selected_years = st.sidebar.multiselect("Select Year(s)", options=df['year'].unique(), default=df['year'].unique())
    selected_categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
    selected_payment = st.sidebar.multiselect("Select Payment Method", options=df['Payment Method'].unique(), default=df['Payment Method'].unique())

    df_filtered = df[
        df['year'].isin(selected_years) &
        df['Category'].isin(selected_categories) &
        df['Payment Method'].isin(selected_payment)
    ]

    # --- KPIs ---
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${df_filtered['Total Spent'].sum():,.0f}")
    col2.metric("Transactions", df_filtered.shape[0])
    col3.metric("Unique Customers", df_filtered['Customer ID'].nunique())

    # --- Charts Row 1 ---
    st.subheader("📈 Sales Trends")

    col1, col2 = st.columns(2)

    with col1:
        sales_by_month = df_filtered.groupby('YearMonth')['Total Spent'].sum().reset_index()
        fig1 = px.line(sales_by_month, x='YearMonth', y='Total Spent', title="Monthly Revenue Trend")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        sales_by_category = df_filtered.groupby('Category')['Total Spent'].sum().sort_values().reset_index()
        fig2 = px.bar(sales_by_category, x='Total Spent', y='Category', orientation='h', title="Revenue by Category")
        st.plotly_chart(fig2, use_container_width=True)

    # --- Charts Row 2 ---
    st.subheader("🛒 Product & Payment Insights")

    col3, col4 = st.columns(2)

    with col3:
        top_items = df_filtered.groupby('Item')['Total Spent'].sum().sort_values(ascending=False).head(10).reset_index()
        fig3 = px.bar(top_items, x='Total Spent', y='Item', orientation='h', title="Top 10 Items by Revenue")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        payment_mix = df_filtered['Payment Method'].value_counts().reset_index()
        payment_mix.columns = ['Payment Method', 'Count']  # ✅ Renaming for clarity
        fig4 = px.pie(payment_mix, names='Payment Method', values='Count', title="Payment Method Distribution")
        st.plotly_chart(fig4, use_container_width=True)

    # --- Optional: Download ---
    st.subheader("⬇️ Download Filtered Data")
    st.download_button("Download CSV", df_filtered.to_csv(index=False), file_name="filtered_sales.csv")
