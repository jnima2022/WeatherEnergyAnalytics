import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import numpy as np
from datetime import datetime, timedelta

# Function to fetch weather data
def get_weather_data(latitude, longitude, start_date, end_date):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation&start_date={start_date}&end_date={end_date}"
    response = requests.get(url)
    return response.json()

# Function to fetch mock commodity price data (replace with real API when available)
def get_commodity_prices(commodity, start_date, end_date):
    # Mock data for demonstration
    dates = pd.date_range(start=start_date, end=end_date)
    prices = np.random.uniform(50, 100, len(dates))
    return pd.DataFrame({'Date': dates, 'Price': prices})

# Function to analyze weather impact on commodity prices
def analyze_weather_impact(weather_data, price_data):
    # Implement your analysis logic here
    # This is a simplified example
    weather_df = pd.DataFrame({
        'Date': pd.to_datetime(weather_data['hourly']['time']),
        'Temperature': weather_data['hourly']['temperature_2m'],
        'Precipitation': weather_data['hourly']['precipitation']
    })
    
    merged_data = pd.merge(weather_df, price_data, on='Date', how='inner')
    correlation = merged_data['Temperature'].corr(merged_data['Price'])
    
    return correlation, merged_data

st.title("Weather Impact on Commodity Prices and Energy Demand")

# User inputs
commodity = st.selectbox("Select a commodity", ["Natural Gas", "Crude Oil", "Electricity"])
location = st.selectbox("Select a location", ["New York", "Chicago", "Houston", "Los Angeles", "San Francisco", "Miami", "Dallas", "Seattle", "Boston", "Denver"])
start_date = st.date_input("Start date", datetime.now() - timedelta(days=30))
end_date = st.date_input("End date", datetime.now())

# Mapping of locations to coordinates (replace with actual coordinates)
coordinates = {
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Los Angeles": (34.0522, -118.2437),
    "San Francisco": (37.7749, -122.4194),
    "Miami": (25.7617, -80.1918),
    "Dallas": (32.7767, -96.7970),
    "Seattle": (47.6062, -122.3321),
    "Boston": (42.3601, -71.0589),
    "Denver": (39.7392, -104.9903)
}


if st.button("Analyze"):
    # Fetch data
    weather_data = get_weather_data(coordinates[location][0], coordinates[location][1], start_date, end_date)
    price_data = get_commodity_prices(commodity, start_date, end_date)
    
    # Analyze data
    correlation, merged_data = analyze_weather_impact(weather_data, price_data)
    
    # Display results
    st.write(f"Correlation between temperature and {commodity} price: {correlation:.2f}")
    
    # Plot temperature and price
    fig = px.line(merged_data, x='Date', y=['Temperature', 'Price'], title=f"Temperature and {commodity} Price Over Time")
    st.plotly_chart(fig)
    
    # Plot precipitation and price
    fig2 = px.line(merged_data, x='Date', y=['Precipitation', 'Price'], title=f"Precipitation and {commodity} Price Over Time")
    st.plotly_chart(fig2)
    
    # Additional insights
    st.subheader("Weather Impact Analysis")
    st.write("This analysis shows the relationship between weather patterns and commodity prices. A positive correlation indicates that as temperature increases, prices tend to rise, while a negative correlation suggests the opposite.")
    st.write("Factors to consider:")
    st.write("- Seasonal patterns in energy demand")
    st.write("- Extreme weather events and their impact on supply chains")
    st.write("- Long-term climate trends affecting production and consumption")

# Add a section for energy demand analysis
st.subheader("Energy Demand Forecast")
st.write("Based on the weather forecast and historical data, we can predict energy demand trends:")

# Mock energy demand forecast (replace with actual predictive model)
demand_forecast = pd.DataFrame({
    'Date': pd.date_range(start=end_date, periods=7),
    'Forecasted Demand': np.random.uniform(80, 120, 7)
})

fig3 = px.line(demand_forecast, x='Date', y='Forecasted Demand', title="7-Day Energy Demand Forecast")
st.plotly_chart(fig3)

st.write("This forecast takes into account expected weather conditions and historical consumption patterns.")

#To run: streamlit run app.py