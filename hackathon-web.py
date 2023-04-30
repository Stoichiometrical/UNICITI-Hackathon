import json
import numpy as np
from scipy.signal import find_peaks
import pandas as pd
import streamlit as st
import altair as alt
import joblib
import requests
from streamlit_lottie import st_lottie
import matplotlib.pyplot as plt
import xgboost as xgb
import datetime as dt





# Load the starting lottie file
def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        lottie_data = json.load(f)
    return lottie_data

def render_lottie_animation(filepath, speed=1, width=700, height=400, loop=True):
    lottie_data = load_lottie_file(filepath)
    st_lottie(lottie_data, speed=speed, width=width, height=height, loop=loop)


st.title("Energy Usage Monitoring")
st.markdown("### Welcome to the Energy Usage Monitoring Board.Check and regulate your energy usage today")

st.markdown("## Save Energy, Save The Grid ,Save Your Money ")

render_lottie_animation("business.json")

st.markdown("### Here is what the weather looks like today")
st.write("   ")

import requests

url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"53.1,-0.13"}

headers = {
    "content-type": "application/octet-stream",
    "X-RapidAPI-Key": "1526a07e77msh8e85f3abfa458bcp1cf15djsn8400d4456de9",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# Check if the request was successful
if response.status_code == 200:
    # Extract the data from the response
    data = response.json()

    # Extract temperature and humidity from the data
    temp = data['current']['temp_c']
    hum = data['current']['humidity']

    # Print the values
    print('Temperature:', temp)
    print('Humidity:', hum)
else:
    print('Error:', response.status_code)



press = 2000






# Create the columns for the buttons
col1, col2, col3= st.columns([1, 1, 1])


# Temperature sectionns
with col1:
    st.write(
        f"""
            <div style='
                background-color: orange;
                border-radius: 20px;
                padding: 10px;
                text-align: center;
            '>
                <p style='color: white; font-size: 24px;'>Temperature</p>
                <p style='color: white; font-size: 36px;'>{temp}&deg;C</p>
            </div>
            """,
        unsafe_allow_html=True
    )
with col2:
    st.write(
        f"""
              <div style='
                  background-color: #00BFFF;
                  border-radius: 20px;
                  padding: 10px;
                  text-align: center;
              '>
                  <p style='color: white; font-size: 24px;'>Humidity</p>
                  <p style='color: white; font-size: 36px;'>{hum}%</p>
              </div>
              """,
        unsafe_allow_html=True
    )
with col3:
    st.write(
        f"""
              <div style='
                  background-color: #DAA520;
                  border-radius: 20px;
                  padding: 10px;
                  text-align: center;
              '>
                  <p style='color: white; font-size: 24px;'>Pressure</p>
                  <p style='color: white; font-size: 36px;'>{press}mb</p>
              </div>
              """,
        unsafe_allow_html=True
    )
st.write(" ")

# Load the trained model
xgb_model = joblib.load('xgb_model.pkl')

# Function to get weather data from API
def get_weather_data():
    # Make API request to get weather data
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": "53.1,-0.13"}
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "1526a07e77msh8e85f3abfa458bcp1cf15djsn8400d4456de9",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    # Extract relevant weather data
    weather_data = response.json()['current']
    temp_c = weather_data['temp_c']
    humidity = weather_data['humidity']

    return temp_c, humidity

# Get today's date and extract day of month and day of week as integers
today = dt.datetime.today()
day_of_month = today.day
day_of_week = today.weekday()

# Create a dataframe with user input and weather data
input_data = pd.DataFrame({
    'dayofmonth': [day_of_month] * 24,
    'day': [day_of_week] * 24,
    'hour': range(24),
    'temp': [0] * 24,
    'humidity': [0] * 24
})

# Use the model to predict energy usage
y_predict = xgb_model.predict(input_data)

# Create a chart with predicted energy usage
data = pd.DataFrame({'x': range(24), 'y': y_predict})
chart = alt.Chart(data).mark_line().encode(x='x', y='y').properties(width=600, height=400)

st.write("   ")
# Display the chart in Streamlit when a button is clicked
if st.button('Click here to See Your Predicted Usage Today'):
    # Get weather data from API
    temp_c, humidity = get_weather_data()

    # Create a dataframe with user input and weather data
    input_data = pd.DataFrame({
        'dayofmonth': [day_of_month] * 24,
        'day': [day_of_week] * 24,
        'hour': range(24),
        'temp': [temp_c] * 24,
        'humidity': [humidity] * 24
    })

    # Use the model to predict energy usage
    y_predict = xgb_model.predict(input_data)
    st.markdown("## This is predicted energy usage for the day")

    # Create a chart with predicted energy usage
    data = pd.DataFrame({'x': range(24), 'y': y_predict})
    chart = alt.Chart(data).mark_line().encode(x='x', y='y').properties(width=600, height=400)

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    # Find peaks in the data
    peaks, _ = find_peaks(data['y'], distance=2, height=0)

    # Get the top 3 peaks
    top_peaks = sorted(zip(peaks, data['y'][peaks]), key=lambda x: x[1], reverse=True)[:3]

    # Display peak recommendations
    st.title("Recommendations")
    st.markdown("### Here are some recommendations for energy optimization:")
    st.write("##### A peak is when your energy usage will be very high. It is advised to reduce energy at these times.")
    st.write("If you click on approve the changes will be automated at the specified peak times.")

    approve_all = st.checkbox("Approve All")

    for i, (index, value) in enumerate(top_peaks):
        recommendation = f"Peak {i + 1} at {index} o'clock, the energy used will be {round(value, 2)} kWh"
        checkbox_key = f"recommendation_{i}"
        approve = st.checkbox(recommendation, key=checkbox_key)

        st.subheader(f"Peak {i + 1} at {index} o'clock, the energy used will be {round(value, 2)} kWh")
        if value > 0:
            st.markdown("- Consider reducing the usage of HVAC system during this peak to conserve energy.")
        else:
            st.markdown(
                    "- During this peak, ensure that the HVAC system is turned off to avoid unnecessary energy consumption.")
            st.markdown("- Reduce overhead lighting during this peak to further save energy.")
            st.markdown("- Get more input from solar battery reserve")

    if approve_all:
        st.write("All recommendations approved.")


# Define function to predict energy consumption for 24 hour period
def predict_energy_consumption(dayofmonth, day, temp, humidity):
    # Create a dataframe with the user input
    input_data = pd.DataFrame({'dayofmonth': [dayofmonth] * 24, 'day': [day] * 24, 'hour': range(24),
                               'temp': [temp] * 24, 'humidity': [humidity] * 24})

    # Make the prediction
    y_predict = xgb_model.predict(input_data)

    # Plot the predicted energy consumption graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(24), y_predict, label='Predicted')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Energy Consumption')
    ax.set_title('Predicted Energy Consumption for 24 Hours')
    ax.legend()
    st.pyplot(fig)

st.write("      ")
st.write("      ")
# Create the user interface using Streamlit
st.markdown('## Want to see how temperature and humidity affect your energy consumption ? Change the features below to see what to expect based different  weather forecasts')

# Define the input fields for the user
dayofmonth = st.number_input('Day of Month', value=1, step=1)
day = st.selectbox('Day', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
temp = st.number_input('Temperature', value=20.0, step=0.1)
humidity = st.number_input('Humidity', value=50, step=1)

# Convert day of week to integer representation
day_dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
day_num = day_dict[day]

# Create a button to trigger the energy consumption prediction and graph display
if st.button('Predict'):
    predict_energy_consumption(dayofmonth, day_num, temp, humidity)



st.write("    ")
st.write("    ")
st.write("    ")


st.markdown("## How does Energy Board hep you become more environmentally sustainable?")

# First row
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background-color: #F7D08A; padding: 20px; border-radius: 10px;">
            <h3>Energy Optimization</h3>
            <p>Our energy optimization feature is designed to help you optimize your energy consumption based on weather conditions. By leveraging weather information, our model can predict energy usage patterns more accurately. This enables you to make informed decisions about adjusting your HVAC settings or reducing other energy-intensive activities during peak usage periods. By proactively managing your energy usage, you can potentially save money on your energy bills and reduce your carbon footprint</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="background-color: 'orange'; padding: 20px; border-radius: 10px;">
            <h3>Peak Load Management</h3>
            <p>Peaks in energy demand can strain the power grid and increase the risk of power outages. Our model provides recommendations on reducing energy usage during peak times to help you actively manage your energy consumption. By following these recommendations, you can potentially reduce the overall load on the grid, contributing to a more stable and reliable energy supply for everyone.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("    ")
# Second row
col3, col4 = st.columns(2)

with col3:
    st.markdown(
        """
        <div style="background-color: #F7D08A; padding: 20px; border-radius: 10px;">
            <h3>Cost Savings</h3>
            <p>By actively managing your energy usage during peak periods, you can potentially lower your energy bills. Additionally, our model can help utility providers avoid investing in additional infrastructure to meet peak demands. These cost savings can have a wider economic impact and potentially result in more affordable energy for consumers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div style="background-color: #5DA5C; padding: 20px; border-radius: 10px;">
            <h3>Environmental Impact</h3>
            <p>At Energy Board, we are committed to promoting sustainable practices and reducing carbon footprints. By encouraging energy reduction during peak periods, our model promotes environmentally-friendly habits and supports efforts to reduce greenhouse gas emissions. If more people adopt our recommendations, it can collectively contribute to a positive environmental impact.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
