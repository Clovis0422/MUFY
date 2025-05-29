import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Sample data
df = pd.DataFrame({
    "Month": ["January", "February", "March", "April"],
    "Sales": [200, 450, 300, 600],
    "Price": [1200, 1500, 1800, 2100]
})

# Add sidebar filters
st.sidebar.header("Filters")

# Dropdown
selected_month = st.sidebar.selectbox(
    "Select Month",
    options=df['Month'].unique()
)

# Slider
price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=0,
    max_value=3000,
    value=(0, 3000)
)

# Filtered DataFrame
filtered_df = df[(df['Month'] == selected_month) & (df['Price'].between(*price_range))]

# Show filtered results
st.write("Filtered Data", filtered_df)

# Optional: Chart
fig = px.bar(filtered_df, x="Month", y="Sales", title="Sales by Month")
st.plotly_chart(fig)

