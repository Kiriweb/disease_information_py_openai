# Disease Information Tool

An interactive Streamlit application that provides comprehensive information about diseases using the OpenAI API. Enter the name of a disease and select a year to receive key statistics, recovery options, and medication details, all displayed in a user-friendly dashboard with visualizations.

## Features

- **Comprehensive Disease Information**: Retrieves key statistics such as total cases, recovery rates, and mortality rates for a specified disease and year.
- **Recovery Options**: Provides detailed explanations of available recovery options for the disease.
- **Medication Details**: Lists recommended medications along with their side effects and dosages.
- **Interactive Visualizations**: Displays recovery and mortality rates in a pie chart for easy understanding.
- **User-Friendly Interface**: Simple input fields for disease name and year selection, making it accessible to users without technical expertise.
- **Secure API Integration**: Uses Streamlit's secrets management to securely handle the OpenAI API key.

## Technologies Used

- **Python 3**
- **Streamlit**
- **OpenAI API**
- **Pandas**
- **Matplotlib**

## Getting Started

### Prerequisites

- **Python 3.x** installed on your system.
- An **OpenAI API key**. Obtain one by signing up on the [OpenAI website](https://openai.com/).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/healthcare_analysis_py_openai.git
   cd healthcare_analysis_py_openai
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up OpenAI API Key**

   - Create a `.streamlit` directory in the root of your project:

     ```bash
     mkdir .streamlit
     ```

   - Inside `.streamlit`, create a `secrets.toml` file:

     ```toml
     # .streamlit/secrets.toml
     OPENAI_API_KEY = "your_openai_api_key_here"
     ```

   - **Important**: Replace `"your_openai_api_key_here"` with your actual OpenAI API key.

### Running the Application

```bash
streamlit run disease_dashboard.py
```

- Replace `disease_dashboard.py` with the name of your main Python script if it's different.

## Usage

1. **Enter Disease Name**

   - Type the name of the disease you want to research in the input field (e.g., `Influenza`, `COVID-19`).

2. **Select Year**

   - Choose the year for which you want to retrieve data from the dropdown menu (options: 2020-2024).

3. **View Results**

   - The application will display:
     - **Statistics**: Total cases, recovery rate, and mortality rate.
     - **Pie Chart**: Visual representation of recovery and mortality rates.
     - **Recovery Options**: Detailed explanations of available treatments.
     - **Medication**: Recommended medications with side effects and dosages.

## Acknowledgments

- Thanks to the developers of Streamlit, OpenAI, Pandas, and Matplotlib for their powerful tools.
- Inspired by healthcare professionals and data scientists who strive to make medical information accessible.This description should give potential users and contributors a clear understanding of your application's purpose, features, and how to get started. Let me know if you need any more assistance!
