import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Configure page layout to be wider
st.set_page_config(layout="wide")

# Retrieve the API key from environment variable
# api_key = "AIzaSyAjI68HV0sCLFW9G5tVWJOlcWh2QbQm74w"
# if not api_key:
#    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
# else:
genai.configure(api_key="AIzaSyAjI68HV0sCLFW9G5tVWJOlcWh2QbQm74w")  # Use the API key from the environment variable

# Model configuration (outside the function for efficiency)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048  # Adjust as needed
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


def process_data_and_prompt(df, prompt):
    """Processes DataFrame and prompt with Gemini, handling visuals."""
    if df is not None:  # Check if a DataFrame was provided
        df_string = df.to_string()  # Or another suitable string representation
        full_prompt = f"{prompt}\n\nData:\n{df_string}"
    else:
        full_prompt = prompt  # Use the prompt directly if no DataFrame

    chat_session = model.start_chat(history=[])  # New session for each prompt
    response = chat_session.send_message(full_prompt)
    return response.text


# Custom CSS for layout
st.markdown("""
   <style>
   .main {
       padding: 0;
   }
   .stTextArea textarea {
       border-radius: 10px;
   }
   .stButton button {
       border-radius: 20px;
       width: 100px !important;
       height: 45px !important;
   }
   div[data-testid="stSidebarContent"] {
       background-color: white !important;
       color: #0066cc !important;  /* Blue color for text */
   }
   section[data-testid="stSidebar"] {
       background-color: white !important;
   }
   /* Add these styles for file uploader */
   .st-emotion-cache-1v04i6g {
       color: black !important;
   }
   .st-emotion-cache-1v04i6g p {
       color: black !important;
   }
   button.st-emotion-cache-1aw8i8e {
       color: black !important;
   }
   /* Updated styles for the file remove/cancel button */
   .st-emotion-cache-u8hs99 {
       color: black !important;
   }
   .st-emotion-cache-u8hs99 svg {
       fill: black !important;
   }
   .st-emotion-cache-u8hs99 path {
       fill: black !important;
   }
   button[kind="secondary"] svg path {
       fill: black !important;
   }
   /* Style for all text in sidebar */
   div[data-testid="stSidebarContent"] p {
       color: #0066cc !important;
   }

   div[data-testid="stSidebarContent"] .st-emotion-cache-1erivf3 {
       color: #0066cc !important;
   }

   div[data-testid="stSidebarContent"] .st-emotion-cache-1gulkj5 {
       color: #0066cc !important;
   }

   div[data-testid="stSidebarContent"] .st-emotion-cache-16idsys p {
       color: #0066cc !important;
   }


   /* Style for file upload success message */
   div[data-testid="stSuccess"] {
       background-color: #D4EDDA !important;
       color: #155724 !important;
       padding: 16px !important;
       border-radius: 4px !important;
       border: 1px solid #C3E6CB !important;
       margin: 16px 0 !important;
       font-weight: bold !important;
   }
   </style>
""", unsafe_allow_html=True)

# Sidebar for file upload and data preview
with st.sidebar:
    st.image("innovapptive logo.png", width=250)
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"File uploaded: {uploaded_file.name}")  # Show the file name
        except pd.errors.ParserError:
            st.error("Invalid CSV format.")
            df = None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            df = None
    else:
        df = None

# Main content area
st.image("OpsGenie-Logo-3.png", width=250)  # Adjust width as needed

# Create a container for chat history
chat_container = st.container()

# Initialize session state for storing the current response
if 'current_response' not in st.session_state:
    st.session_state.current_response = None

# Input area at the bottom
with st.container():
    st.markdown("<br>" * 2, unsafe_allow_html=True)  # Add some space

    # Create a horizontal container for prompt and button
    input_container = st.container()

    # Use columns with different ratio for better layout
    with input_container:
        col1, col2 = st.columns([15, 2])

        with col1:
            prompt = st.text_area("", placeholder="Enter your prompt here...", height=100, label_visibility="collapsed")

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.button("Submit", type="primary")

# Handle submission
if submit_button and prompt:
    with st.spinner("Processing..."):
        try:
            # Clear previous response by setting new response
            output = process_data_and_prompt(df, prompt)
            st.session_state.current_response = output

            # Display current prompt and response
            st.write("Your prompt:")
            st.write(prompt)
            st.write("Response:")
            st.write(st.session_state.current_response)

            # Clear the prompt input (this will happen on next rerun)
            prompt = ""

        except Exception as e:
            st.error(f"An error occurred: {e}")
elif submit_button:
    st.warning("Please enter a prompt.")