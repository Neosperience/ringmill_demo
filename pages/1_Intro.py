import os
import streamlit as st
import PyPDF2
import requests
import io
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Intro")

st.title("RingMill Data Extraction")
#st.write("Upload your PDFs in the appropriate sections below.")

def handle_empty(dictionary):
    for key, value in dictionary.items():
        if len(value) == 0:
            dictionary[key] = "null"
    return dictionary

# ---------------------------
# PDF with Intro
# ---------------------------
st.header("PDF con Intro")
intro_pdf = st.file_uploader("Carica il PDF che contiene l'Intro", type="pdf", key="intro_pdf")


if intro_pdf is not None:
    try:
        st.divider()


        # Define the API endpoint, common query parameters, and data
        url = "https://vm11.yonderlabs.com/2.0/text/extractstructured"
        params = {
            "template": "ringmill-intro::001",
            "access_token": os.environ["YONDER_ACCESS_TOKEN"],
            "model_name": "gemini-2.0-flash",
            "cheap_mode": "false"
        }
        data = {
            "refinement": "{}"
        }
                    # Prepare the file payload for the API call
        files = {
            'data': (intro_pdf.name, intro_pdf, 'application/pdf')
        }

        with st.spinner("Extracting Data...", show_time=True):
        # Send the POST request for the current page
            response = requests.post(url, params=params, files=files, data=data, verify=False)

        #st.write(f"Page - Response Body: {response.text}")
        output = response.json()
        output = handle_empty(output)
        df = pd.DataFrame([output])
        st.table(df)
        st.badge("Success", icon=":material/check:", color="green")
        st.divider()
        st.subheader("PDF Preview")
        binary_data = intro_pdf.getvalue()
        pdf_viewer(input=binary_data,width=700)

    except Exception as e:
        st.error(f"Error processing PDF: {e}")
