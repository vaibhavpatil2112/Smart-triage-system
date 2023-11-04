from PIL import Image
import streamlit as st
import geopy.distance
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import pandas as pd
import pickle


hospital_data = pickle.load(open('model_pickle.pkl','rb'))

# Define hospitals and their locations
hospitals = {
    'City Hospital': (40.741895, -74.11),
    'Nulife Hospital': (40.742150, -76.48),
    'Apex Hospital': (40.743009, -77.98),
    'Jupiter Hospital': (40.742663, -78.98),
    'Kem Hospital': (40.741835, -79.98),
    'Parth Hospital': (40.743029, -72.11),
    'Navjeevan Hospital': (41.742743, -70.66),
    'Fortis Hospital': (42, -73.80),
    'Global Hospital': (43, -75.45),
    'Kokilaben Hospital': (44, -73.98),
    'Hinduja Hospital': (41, -72.55)
}

# Define bed availability for each hospital
beds_available = {
    'City Hospital': 5,
    'Nulife Hospital': 10,
    'Apex Hospital': 7,
    'Jupiter Hospital': 3,
    'Kem Hospital': 9,
    'Parth Hospital': 2,
    'Navjeevan Hospital': 8,
    'Fortis Hospital': 5,
    'Global Hospital': 10,
    'Kokilaben Hospital': 7,
    'Hinduja Hospital': 3
}

# img_contact_form = Image.open("Images/image1.jpg")

# Define a function to calculate distance between two points
def calculate_distance(loc1, loc2):
    return geopy.distance.distance(loc1, loc2).miles

# Define a function to assign patient to nearest hospital
def assign_hospital(patient, hospitals):
    patient_loc = (patient['latitude'], patient['longitude'])
    nearest_hospital = ''
    nearest_distance = float('inf')
    for name, loc in hospitals.items():
        distance = calculate_distance(patient_loc, loc)
        if distance < nearest_distance and beds_available[name] > 0:
            nearest_hospital = name
            nearest_distance = distance
    if nearest_hospital:
        beds_available[nearest_hospital] -= 1
    return nearest_hospital

# Define a function to calculate triage level
def calculate_triage_level(patient):
    triage_level = 0
    if patient['age'] >= 65:
        triage_level += 2
    elif patient['age'] >= 50:
        triage_level += 1
    if patient['heart_rate'] > 100:
        triage_level += 1
    if patient['body_temp'] >= 103:
        triage_level += 1
    if patient['oxygen_sat'] < 90:
        triage_level += 1
    if patient['blood_pressure'] >= 140:
        triage_level += 1
    return triage_level

# Define a function to plot hospital locations
def plot_hospitals():
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, loc in hospitals.items():
        ax.scatter(loc[1], loc[0], s=50, label=name)
    ax.set_xlabel('Longitude', fontsize=6)
    ax.set_ylabel('Latitude', fontsize=6)
    ax.set_title('Hospital Locations', fontsize=6)

    # Adjust the font size of the x-axis tick labels
    ax.tick_params(axis='x', labelsize=5)

    # Remove scientific notation from the y-axis tick labels
    formatter = ticker.StrMethodFormatter('{x:.6f}')
    ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis='y', labelsize=5)

    # Adjust the font size of the legend
    legend = ax.legend(fontsize=5)
    legend.set_title('Hospitals', prop={'size': 5})

    st.pyplot(fig)


# Define a function to plot bed availability
def plot_beds_available():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.bar(beds_available.keys(), beds_available.values())
    ax.set_xlabel('Hospitals', fontsize=8)
    ax.set_ylabel('Beds Available', fontsize=7)
    ax.set_title('Bed Availability', fontsize=7)
    ax.tick_params(axis='y', labelsize=6)
    ax.tick_params(axis='x', labelsize=8)
    st.pyplot(fig)

# Define the Streamlit UI
def main():
    st.set_page_config()
    st.title('Triage System')
    st.markdown('This is a Triage System that helps in prioritizing patients based on their health parameters.')
    st.sidebar.header('Patient Data')
    gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
    age = st.sidebar.number_input('Age', min_value=0, max_value=120, value=30)
    heart_rate = st.sidebar.number_input('Heart Rate', min_value=0, value=70)
    body_temperature = st.sidebar.number_input('Body Temperature (°C)', min_value=35.0, max_value=42.0, value=36.5)
    oxygen_saturation = st.sidebar.number_input('Oxygen Saturation (%)', min_value=0, max_value=100, value=95)
    blood_pressure = st.sidebar.number_input('Blood Pressure (mmHg)', min_value=0, value=120)
    latitude = st.sidebar.number_input('Latitude')
    longitude = st.sidebar.number_input('Longitude')
    patient = {
        'gender': gender,
        'age': age,
        'heart_rate': heart_rate,
        'body_temp': body_temperature,
        'oxygen_sat': oxygen_saturation,
        'blood_pressure': blood_pressure,
        'latitude': latitude,
        'longitude': longitude
    }

    # with st.container():
        # left_column, right_column = st.columns(2)
        # with left_column:
        #     st.image(img_contact_form)

    triage_level = calculate_triage_level(patient)
    if triage_level == 0:
        st.sidebar.success('Low')
    elif triage_level <= 2:
        st.sidebar.warning('Medium')
    else:
        st.sidebar.error('High')

    st.sidebar.markdown('---')

    if st.sidebar.button('Assign Hospital'):
        assigned_hospital = assign_hospital(patient, hospitals)
        if assigned_hospital:
            st.sidebar.success(f'Hospital Assigned: {assigned_hospital}')
        else:
            st.sidebar.error('No available hospitals')


    st.header('Plot Hospitals')
    st.markdown('This plot shows the locations of hospitals:')
    plot_hospitals()

    st.header('Plot Bed Availability')
    st.markdown('This plot shows the bed availability in hospitals:')
    plot_beds_available()


if __name__ == '__main__':
    main()


