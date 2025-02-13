import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader

@st.cache_data
def load_diseases_from_pdf(pdf_path):
    """
    Load a list of diseases from a PDF file.
    """
    diseases = set()
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                diseases.add(line.strip().lower())  # Add each disease to the set in lowercase
    except Exception as e:
        st.error(f"Error loading diseases from PDF: {e}")
    return diseases

PDF_PATH = "diseases.pdf"
DISEASES_LIST = load_diseases_from_pdf(PDF_PATH)

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
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please provide information on the following aspects for {disease_name} in the year {year}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications. Format the response in JSON with keys for 'name', 'statistics', 'total_cases' (this always has to be a number), 'recovery_rate' (this always has to be a percentage), 'mortality_rate' (this always has to be a percentage), 'recovery_options' (explain each recovery option in detail), and 'medication' (give some side effect examples and dosages). Always use this JSON format for medication: {medication_format}. Ensure the response is valid JSON and do not include any additional text before or after the JSON object."}
            ]
        )
        response_content = response.choices[0].message.content.strip()

        # Clean and extract JSON if needed
        if not response_content.startswith("{") or not response_content.endswith("}"):
            response_content = response_content[response_content.find("{"):response_content.rfind("}") + 1]

        # Parse and return JSON
        return json.loads(response_content)
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")
        return None
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return None

def display_disease_info(disease_info):
    """
    Function to display the disease information in a structured way using Streamlit.
    """
    try:
        recovery_rate = float(disease_info['statistics']["recovery_rate"].strip('%'))
        mortality_rate = float(disease_info['statistics']["mortality_rate"].strip('%'))

        # Pie chart to display Recovery and Mortality Rates
        labels = ['Recovery Rate', 'Mortality Rate']
        sizes = [recovery_rate, mortality_rate]
        colors = ['#4CAF50', '#FF6347']
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
        
        st.write(f"## Statistics for {disease_info['name']}")
        st.pyplot(fig)  # Display the pie chart

        st.write("## Recovery Options")
        recovery_options = disease_info['recovery_options']
        for option, description in recovery_options.items():
            st.subheader(option)
            st.write(description)
            
        st.write("## Medication")
        medication = disease_info['medication']
        medication_count = 1
        for option, description in medication.items():
            st.subheader(f"{medication_count}. {option}")
            st.write(description)
            medication_count += 1
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")

st.title("Disease Information Dashboard")

disease_name = st.text_input("Enter the name of the disease:")
year = st.selectbox("Select Year", options=[2020, 2021, 2022, 2023, 2024])

if disease_name:
    if disease_name.lower() not in DISEASES_LIST:
        st.error(f"'{disease_name}' is not found in the list of diseases. Please enter a valid disease.")
    else:
        with st.spinner("Fetching disease information..."):
            disease_info = get_disease_info(disease_name, year)
        if disease_info:
            display_disease_info(disease_info)
