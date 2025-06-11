import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import numpy as np
import streamlit as st
html_title = """<h1 style="color:red;text-align:center;">retail_store_sales</h1>"""
st.markdown(html_title,unsafe_allow_html=True)
st.image('WhatsApp Image 2025-06-11 at 21.30.23_94879f49.jpg' )
tab1, tab2, tab3, tab4 = st.tabs(["Dataset uncleaned","Dataset cleaned", "Visualizations", "About"])
columns = [
    "Transaction ID: A unique identifier for each transaction.",
    "Customer ID: A unique identifier for each customer.",
    "Category: The category of the purchased item.",
    "Item: The name of the purchased item.",
    "Price Per Unit: The static price of a single unit of the item.",
    "Quantity: The quantity of the item purchased.",
    "Total Spent: The total amount spent on the transaction.",
    "Payment Method: The method of payment used.",
    "Location: The location where the transaction occurred.",
    "Transaction Date: The date of the transaction.",
    "Discount Applied: Indicates whether a discount was applied to the transaction."
]
with tab1:
    st.subheader("Dataset uncleaned")
    df_uncleaned = pd.read_csv('uncleaned.csv')
    st.dataframe(df_uncleaned.head(3))
    st.write(df_uncleaned.describe())
    st.write("Missing values before cleaning:")
    st.write(df_uncleaned.isnull().sum())
    st.write("Columns:", columns)
with tab2:
    st.subheader("Dataset cleaned")
    df_cleaned = pd.read_csv('cleaned.csv')
    st.dataframe(df_cleaned.head(3))
    st.write(df_cleaned.describe())
    st.write("Missing values after cleaning:")
    st.write(df_cleaned.isnull().sum())
with tab3:
   
   
   
    st.subheader("Visualizations")
    st.write("Total Spent by Category")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_cleaned, x='Category', y='Total Spent', estimator='sum', ci=None, ax=ax1)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig1)

    st.write("Monthly Transaction Counts")
    monthly_counts = df_cleaned['month'].value_counts().reindex([
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ])
    plt.figure(figsize=(8, 4))
    monthly_counts.plot(kind='line', marker='o')
    plt.ylabel("Transaction Count")
    plt.xlabel("Month")
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt.gcf())

    st.write("Payment Method Distribution")
    plt.figure(figsize=(6, 6))
    df_cleaned['Payment Method'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.ylabel("")
    plt.title("Payment Method Distribution")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    st.write("Total Spent With/Without Discount")
    plt.figure(figsize=(8, 4))
    sns.boxplot(data=df_cleaned, x='Discount Applied', y='Total Spent')
    plt.title("Total Spent With/Without Discount")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    st.write("Spending by Location and Category")







    fig2 = px.treemap(df_cleaned, path=['Location', 'Category'], values='Total Spent', title='Spending by Location and Category')
    st.plotly_chart(fig2)
    st.write("Average Spend by Category and Month")
    heat_data = df_cleaned.pivot_table(index='Category', columns='month', values='Total Spent', aggfunc='mean')
    plt.figure(figsize=(12,6))
    sns.heatmap(heat_data, cmap="YlGnBu", annot=True, fmt=".1f")
    plt.title("Average Spend by Category and Month")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    st.write("Pairplot of Price Per Unit, Quantity, and Total Spent")
    sns.pairplot(df_cleaned, vars=['Price Per Unit', 'Quantity', 'Total Spent'], hue='Discount Applied')
    st.pyplot(plt.gcf())
    st.write("Top 5 Customers by Total Spent and Transaction Count")
    data = df_cleaned.groupby('Customer ID').agg({'Total Spent': 'sum', 'Transaction ID': 'count'})
    top_frequent = data.sort_values(by=['Transaction ID', 'Total Spent'], ascending=[False, False]).head(5)
    st.dataframe(top_frequent)
    st.write("Monthly Total Sales")
    df_cleaned['Transaction Date'] = pd.to_datetime(df_cleaned['Transaction Date'])
    df_cleaned['YearMonth'] = df_cleaned['Transaction Date'].dt.to_period('M')
    monthly = df_cleaned.groupby('YearMonth')['Total Spent'].sum()
    plt.figure(figsize=(10, 5))
    monthly.plot(marker='o', title='Monthly Total Sales')
    plt.ylabel('Money Spent')
    plt.grid(True)
    plt.show()
    st.pyplot(plt.gcf())
    st.write("Online vs In-Store Spending")
    location_totals = df_cleaned.groupby('Location')['Total Spent'].sum().reset_index()
    st.write("Total Spent by Location")
    st.dataframe(location_totals) 
    st.write("Pie Chart of Online vs In-Store Spending")
    st.write("Total Spent by Location")
    st.dataframe(location_totals)
    




    
    fig3 = px.pie(location_totals, names='Location', values='Total Spent', title='Online vs In-Store Spending', hole=0.3)
    st.plotly_chart(fig3)
    st.write("Total Spent by Year")
    st.dataframe(df_cleaned.groupby('year')['Total Spent'].sum())
    st.write("Total Quantity Sold by Category")
    st.dataframe(df_cleaned.groupby('Category')['Quantity'].sum().sort_values(ascending=False))
    st.write("Total Spent by Month")
    st.dataframe(df_cleaned.groupby('month')['Total Spent'].sum().sort_values(ascending=False))
    st.write("Total Quantity Sold by Month and Category")
    st.dataframe(df_cleaned.groupby(['month', 'Category'])['Quantity'].sum().unstack(fill_value=0)) 




with tab4:
    st.subheader("About")
    st.write("This project analyzes retail store sales data to uncover insights about customer behavior, spending patterns, and product performance. The dataset includes transaction details such as date, location, category, payment method, and discounts applied.")
    st.write("The analysis includes data cleaning, exploratory data analysis (EDA), and various visualizations to present findings.")
    st.write("The project uses libraries such as Pandas, Matplotlib, Seaborn, and Plotly for data manipulation and visualization.")
