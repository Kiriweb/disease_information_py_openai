import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import matplotlib.pyplot as plt

# Set your OpenAI API key here
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_disease_info(disease_name, year):
    """
    Function to query OpenAI and return structured information about a disease.
    """
    medication_format = '''"name":""
    "side_effects":[
    0:""
    1:""
    ...
    ]
    "dosage":""'''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please provide information on the following aspects for {disease_name} in the year {year}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications. Format the response in JSON with keys for 'name', 'statistics', 'total_cases' (this always has to be a number), 'recovery_rate' (this always has to be a percentage), 'mortality_rate' (this always has to be a percentage) 'recovery_options', (explain each recovery option in detail), and 'medication', (give some side effect examples and dosages) always use this json format for medication : {medication_format} ."}
        ]
    )
    return response.choices[0].message.content

def display_disease_info(disease_info):
    """
    Function to display the disease information in a structured way using Streamlit.
    """
    try:
        info = json.loads(disease_info)

        recovery_rate = float(info['statistics']["recovery_rate"].strip('%'))
        mortality_rate = float(info['statistics']["mortality_rate"].strip('%'))

        # Pie chart to display Recovery and Mortality Rates
        labels = ['Recovery Rate', 'Mortality Rate']
        sizes = [recovery_rate, mortality_rate]
        colors = ['#4CAF50', '#FF6347']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
        
        st.write(f"## Statistics for {info['name']}")
        st.pyplot(fig)  # Display the pie chart

        st.write("## Recovery Options")
        recovery_options = info['recovery_options']
        for option, description in recovery_options.items():
            st.subheader(option)
            st.write(description)
            
        st.write("## Medication")
        medication = info['medication']
        medication_count = 1
        for option, description in medication.items():
            st.subheader(f"{medication_count}. {option}")
            st.write(description)
            medication_count += 1
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")

# Streamlit app title
st.title("Disease Information Dashboard")

# Input for disease name
disease_name = st.text_input("Enter the name of the disease:")

# Year selection
year = st.selectbox("Select Year", options=[2020, 2021, 2022, 2023, 2024])

# Fetch and display disease information
if disease_name:
    with st.spinner("Fetching disease information..."):
        disease_info = get_disease_info(disease_name, year)
    if disease_info:
        display_disease_info(disease_info)
