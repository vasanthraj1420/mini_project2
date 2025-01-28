import pandas as pd
import streamlit as st
import pymysql 
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu##Data Analysis and Visualization
st.set_page_config(layout="wide")
web = option_menu(menu_title="🔴Stock Analysis🟢",
                 options=["💲Home", "📉Data Analysis & Visualization"],
                 icons=[":house:", "info-circle"],
                 orientation="horizontal"
                 )
if web == "💲Home":
    st.image(r"C:\Users\vasan\Pictures\Screenshots\stock logo.png", width=200)
    st.title("Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends")
    st.subheader(":red[Domain:] Finance/Data Analytics")
    st.subheader(":red[Objective:]")
    st.markdown("The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year.")
    st.subheader(":red[Overview:]")
    st.markdown("""
    - **Pandas**: Data manipulation and analysis library.
    - **MySQL**: Relational database for managing stock data.
    - **Streamlit**: Interactive, data-driven web applications.
    """)
    st.subheader(":red[Skill-taken:]")
    st.markdown("Pandas, Python, Power BI, Streamlit, SQL, Statistics, Data Organizing, Cleaning, and Visualizing.")
    st.subheader(":red[Developed-by:] G.Vasanth Raj")
    
if web=="📉Data Analysis & Visualization":
    s=st.selectbox('stocks Analysis & Visualization',["Volatility Analysis","Cumulative Return Over Time","Sector-wise Performance",
                                                      "Stock Price Correlation","Top 5 Gainers and Losers (Month-wise)"])
    conn = pymysql.connect(host="localhost", user="root", password="14201420vj", database="Stock_Analysis")
    db_config = {"host": "localhost","user": "root","password": "14201420vj","database": "Stock_Analysis"}
    if s=="Volatility Analysis":
        st.title('Stock Volatility Analysis')
        v=st.selectbox('Top 10 Volatile',["Top 10 high Volatile Stocks","Top 10 Low Volatile Stocks"])
        if v== "Top 10 high Volatile Stocks":
            #conn = pymysql.connect(host="localhost", user="root", password="14201420vj", database="Stock_Analysis")
            query = '''SELECT Ticker, Volatility FROM top_10_Hige_volatility'''
            top_10_volatility = pd.read_sql(query, conn)
            conn.close()
            st.write("Top 10 Most Volatile Stocks:", top_10_volatility)
            plt.figure(figsize=(12, 6))
            plt.bar(top_10_volatility['Ticker'], top_10_volatility['Volatility'], color='green')
            plt.title('Top 10 High volatile Stocks (Past Year)', fontsize=14)
            plt.xlabel('Stock Ticker', fontsize=12)
            plt.ylabel('Volatility (Standard Deviation)', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)
        if v=="Top 10 Low Volatile Stocks":
            #conn = pymysql.connect(host="localhost", user="root", password="14201420vj", database="Stock_Analysis")
            query = '''SELECT Ticker, Volatility FROM top_10_Low_volatility'''
            top_10_volatility = pd.read_sql(query, conn)
            conn.close()
            st.write("Top 10 Most Volatile Stocks:", top_10_volatility)
            plt.figure(figsize=(12, 6))
            plt.bar(top_10_volatility['Ticker'], top_10_volatility['Volatility'], color='red')
            plt.title('Top 10 Low Volatile Stocks (Past Year)', fontsize=14)
            plt.xlabel('Stock Ticker', fontsize=12)
            plt.ylabel('Volatility (Standard Deviation)', fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)
    if s=="Cumulative Return Over Time":
        st.title('Cumulative Return Over Time')
        conn = pymysql.connect(**db_config)
        query = "SELECT * FROM stockdatas"
        data = pd.read_sql(query, conn)
        conn.close()
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values(by=['Ticker', 'date'])
        data['Daily Return'] = data.groupby('Ticker')['close'].pct_change()
        data['Cumulative Return'] = (1 + data['Daily Return']).groupby(data['Ticker']).cumprod() - 1
        data['Cumulative Return (%)'] = data['Cumulative Return'] * 100
        conn = pymysql.connect(**db_config)
        query = "SELECT * FROM Cumulative_Return"
        top_ticker= pd.read_sql(query, conn)
        conn.close()
        top_tickers = top_ticker['Ticker'].unique()
        filtered_data = data[data['Ticker'].isin(top_tickers)]
        top_ticker['Cumulative_Return (%)']=top_ticker['Cumulative_Return']*100
        st.write('Cumulative Return (%) Data', top_ticker)
        plt.figure(figsize=(12, 6))
        for ticker in top_tickers:
           stock_data = filtered_data[filtered_data['Ticker'] == ticker]
           plt.plot(stock_data['date'], stock_data['Cumulative Return (%)'], label=ticker)
        plt.title('Cumulative Return for Top 5 Performing Stocks (Year)', fontsize=14)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Return (%)', fontsize=12)
        plt.legend(title='Stock Ticker')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)
    if s=="Sector-wise Performance":
        st.title('Average Yearly Return by Sector')
        conn = pymysql.connect(**db_config)
        query = '''SELECT * FROM stock_analysis.sector_wise_performance'''
        sector_performance = pd.read_sql(query, conn)
        conn.close()
        st.write("Sector Performance Data", sector_performance)
        plt.figure(figsize=(10, 6))
        plt.bar(sector_performance['sector'], sector_performance['Yearly_Return'], color=(0.6, 0.8, 1))
        plt.xlabel('Sector', fontsize=12)
        plt.ylabel('Average Yearly Return (%)', fontsize=12)
        plt.title('Average Yearly Return by Sector', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt)
    if s=="Stock Price Correlation":
        query='''SELECT * FROM StockDatas '''
        data=pd.read_sql(query,conn)
        conn.close()
        sector_returns = data.groupby(['date', 'sector'])['Daily_Return'].mean().unstack()
        sector_correlation = sector_returns.corr()
        sector_correlation_filtered = sector_correlation.copy()
        plt.figure(figsize=(12, 8))
        sns.heatmap(sector_correlation_filtered, annot=True, cmap='coolwarm', fmt=".2f", cbar=True, center=0)
        plt.title("Sector-Level Correlation Heatmap ")
        plt.xlabel("Sectors")
        plt.ylabel("Sectors")
        plt.show()
        st.pyplot(plt)
    if s=="Top 5 Gainers and Losers (Month-wise)":
        query='''SELECT * FROM Gainers_Losers '''
        monthly_data=pd.read_sql(query,conn)
        conn.close()
        top_gainers = monthly_data.groupby('month').apply(lambda x: x.nlargest(5, 'monthly_return')).reset_index(drop=True)
        top_losers = monthly_data.groupby('month').apply(lambda x: x.nsmallest(5, 'monthly_return')).reset_index(drop=True)
        months = monthly_data['month'].unique()
        st.write("Top 5 Gainers and Losers (Month-wise)")
        plt.figure(figsize=(20, 25))
        for i, month in enumerate(months):
            plt.subplot(len(months), 2, i * 2 + 1)
            month_gainers = top_gainers[top_gainers['month'] == month]
            sns.barplot(data=month_gainers, x='monthly_return', y='Ticker', palette='Greens_r')
            plt.title(f"Top 5 Gainers - {month}")
            plt.xlabel("Monthly Return (%)")
            plt.ylabel("Ticker")
            plt.subplot(len(months), 2, i * 2 + 2)
            month_losers = top_losers[top_losers['month'] == month]
            sns.barplot(data=month_losers, x='monthly_return', y='Ticker', palette='Reds_r')
            plt.title(f"Top 5 Losers - {month}")
            plt.xlabel("Monthly Return (%)")
            plt.ylabel("Ticker")
        plt.tight_layout()
        plt.show()
        st.pyplot(plt)



    