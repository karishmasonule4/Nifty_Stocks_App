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

# Show available sectors
sectors = df['Category'].unique()
selected_sector = st.selectbox("Select Sector", sectors)

# Filter based on selected sector
filtered_by_sector = df[df['Category'] == selected_sector]

# Show available stocks in selected sector
stocks = filtered_by_sector['Symbol'].unique()
selected_stock = st.selectbox("Select Stock", stocks)

# Filter based on selected stock
stock_data = filtered_by_sector[filtered_by_sector['Symbol'] == selected_stock]

# Plotting
st.subheader(f"Closing Price Trend: {selected_stock}")
fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(x=stock_data['Date'], y=stock_data['Close'], ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Closing Price")
plt.xticks(rotation=45)
st.pyplot(fig)
