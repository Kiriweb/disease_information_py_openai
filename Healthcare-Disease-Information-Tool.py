import streamlit as st
import openai
import json
import pandas as pd
import matplotlib.pyplot as plt

# Set your OpenAI API key
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Missing OpenAI API Key. Please add it to .streamlit/secrets.toml or via the Streamlit Cloud Secrets UI.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_disease_info(disease_name, year):
    """
    Function to query OpenAI and return structured information about a disease.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Using GPT-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please provide information on {disease_name} for the year {year}. Include key statistics, recovery options, and recommended medications in JSON format."}
            ]
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        st.error(f"OpenAI API Error: {e}")
        st.stop()

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
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        st.write(f"## Statistics for {info['name']}")
        st.pyplot(fig)

        st.write("## Recovery Options")
        for option, description in info['recovery_options'].items():
            st.subheader(option)
            st.write(description)

        st.write("## Medication")
        for medication in info['medication']:
            st.subheader(medication['name'])
            st.write(f"Side Effects: {', '.join(medication['side_effects'])}")
            st.write(f"Dosage: {medication['dosage']}")
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON.")

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
