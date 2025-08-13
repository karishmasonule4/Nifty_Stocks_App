import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("Nifty_Stocks.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Page Config
st.set_page_config(page_title="📈 Nifty Stocks Dashboard", layout="wide")
st.title("📊 Nifty Stocks - Advanced Viewer")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Date filter
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Sector filter (multi-select)
sectors = sorted(df['Category'].unique())
selected_sectors = st.sidebar.multiselect("Select Sectors", sectors, default=sectors)

# Stock search
stock_search = st.sidebar.text_input("Search Stock Name").lower()

# Filter data
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Category'].isin(selected_sectors)) &
    (df['Stock'].str.lower().str.contains(stock_search))
]

# Show filtered data
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

# Chart type selection
chart_type = st.selectbox("Choose Chart Type", ["Line Chart", "Bar Chart", "Moving Average"])

# Plot data
if not filtered_df.empty:
    plt.figure(figsize=(12, 6))

    if chart_type == "Line Chart":
        for stock in filtered_df['Stock'].unique():
            stock_data = filtered_df[filtered_df['Stock'] == stock]
            plt.plot(stock_data['Date'], stock_data['Close'], label=stock)

    elif chart_type == "Bar Chart":
        bar_data = filtered_df.groupby('Stock')['Close'].mean().sort_values()
        bar_data.plot(kind='bar')
        plt.ylabel("Average Closing Price")

    elif chart_type == "Moving Average":
        ma_window = st.slider("Moving Average Window (days)", 5, 50, 20)
        for stock in filtered_df['Stock'].unique():
            stock_data = filtered_df[filtered_df['Stock'] == stock].sort_values('Date')
            stock_data['MA'] = stock_data['Close'].rolling(ma_window).mean()
            plt.plot(stock_data['Date'], stock_data['MA'], label=f"{stock} MA({ma_window})")

    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Download filtered data
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download CSV", csv, "filtered_nifty_stocks.csv", "text/csv")

