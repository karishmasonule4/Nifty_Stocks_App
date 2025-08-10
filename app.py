

import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("Nifty_Stocks.csv")
df.Date = pd.to_datetime(df.Date)

# Page Config
st.set_page_config(page_title="Nifty Stock Viewer", layout="wide")

st.title("📈 Nifty Stocks Sector & Stock Viewer")

# --- Sector selection ---
sectors = df['Category'].unique()
selected_sector = st.selectbox("Select Sector", sectors)

# Filter by sector
filtered_by_sector = df[df['Category'] == selected_sector]

# --- Stock selection ---
stocks = filtered_by_sector['Symbol'].unique()
selected_stock = st.selectbox("Select Stock", stocks)

# Filter by selected stock
stock_data = filtered_by_sector[filtered_by_sector['Symbol'] == selected_stock].sort_values("Date")

# --- NEW FEATURE 1: Direct stock search ---
st.markdown("### 🔍 Search Stock by Symbol")
search_symbol = st.text_input("Enter Stock Symbol (optional)")
if search_symbol:
    search_data = df[df['Symbol'].str.contains(search_symbol.upper(), case=False)]
    if not search_data.empty:
        st.dataframe(search_data.sort_values("Date").tail(10))
    else:
        st.warning("No matching stock found!")

# --- NEW FEATURE 2: Stock statistics ---
latest_price = stock_data['Close'].iloc[-1]
highest_price = stock_data['Close'].max()
lowest_price = stock_data['Close'].min()
avg_price = stock_data['Close'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Price", f"{latest_price:.2f}")
col2.metric("Highest Price", f"{highest_price:.2f}")
col3.metric("Lowest Price", f"{lowest_price:.2f}")
col4.metric("Average Price", f"{avg_price:.2f}")

# --- Plot: Closing Price with Moving Average ---
st.subheader(f"Closing Price Trend with Moving Average: {selected_stock}")
stock_data['MA20'] = stock_data['Close'].rolling(20).mean()  # 20-day MA
stock_data['MA50'] = stock_data['Close'].rolling(50).mean()  # 50-day MA

fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(x='Date', y='Close', data=stock_data, ax=ax, label='Close Price')
sb.lineplot(x='Date', y='MA20', data=stock_data, ax=ax, label='20-Day MA')
sb.lineplot(x='Date', y='MA50', data=stock_data, ax=ax, label='50-Day MA')
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price")
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)

# --- NEW FEATURE 3: Volume trend ---
st.subheader(f"Trading Volume Trend: {selected_stock}")
fig2, ax2 = plt.subplots(figsize=(12, 4))
sb.barplot(x='Date', y='Volume', data=stock_data, ax=ax2, color='skyblue')
ax2.set_xlabel("Date")
ax2.set_ylabel("Volume")
plt.xticks(rotation=45)
st.pyplot(fig2)
