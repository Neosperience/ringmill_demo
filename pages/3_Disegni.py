import os
import streamlit as st
import PyPDF2
import requests
import io
import pandas as pd
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Disegni")

st.title("RingMill Data Extraction")
#st.write("Upload your PDFs in the appropriate sections below.")

def handle_empty(dictionary):
    for key, value in dictionary.items():
        if len(value) == 0:
            dictionary[key] = "null"
    return dictionary

# ---------------------------
# PDF with Images
# ---------------------------
st.header("PDF con Disegni")
image_pdf = st.file_uploader("Carica il PDF che contiene disegni", type="pdf", key="image_pdf")

if image_pdf is not None:
    try:
        st.divider()
        # Read the PDF using PyPDF2
        pdf_reader = PyPDF2.PdfReader(image_pdf)
        num_pages = len(pdf_reader.pages)

        # Define the API endpoint, common query parameters, and data
        url = 'https://vm11.yonderlabs.com/2.0/text/extractstructured'
        params = {
            'template': 'ringmill-drawing::001',
            'access_token': os.environ["YONDER_ACCESS_TOKEN"],
            "model_name": "gemini-2.0-flash",
            "cheap_mode": "false"
        }
        data = {
            'refinement': '{}'
        }

        # Iterate over each page in the PDF
        for i in range(0,num_pages):
            pdf_writer = PyPDF2.PdfWriter()
            page = pdf_reader.pages[i]
            pdf_writer.add_page(page)
           

            # Write the single page to an in-memory bytes buffer
            page_pdf_io = io.BytesIO()
            pdf_writer.write(page_pdf_io)
            page_pdf_io.seek(0)
      

            # Prepare the file payload for the API call
            files = {
                'data': (image_pdf.name, page_pdf_io, 'application/pdf')
            }

            with st.spinner("Extracting Data...", show_time=True):
            # Send the POST request for the current page
                response = requests.post(url, params=params, files=files, data=data, verify=False)

            #st.write(f"Page {i+1} - Response Body: {response.text}")
            output = response.json()
            output = handle_empty(output)
            df = pd.DataFrame([output])
            #st.table(df)
            st.dataframe(df)
        st.badge("Success", icon=":material/check:", color="green")
        st.divider()
        st.subheader("PDF Preview")
        binary_data = image_pdf.getvalue()
        pdf_viewer(input=binary_data,width=700)

    except Exception as e:
        st.error(f"Error processing Intro PDF: {e}")
