# Ringmill Demo

Questo progetto contiene il codice necessario per far girare una demo su Streamlit Cloud che utlizza Yonder API per fare estrazione dati da PDF.

Il codice si trova nella cartella "pages". I file python sono numerati in ordine crescente: 1, 2, 3. Questo serve a Streamlit per creare una App Multipage (https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app). 

Per utilizzare access token in una app di Streamlit Cloud, bisogna tenere conto che vanno scritte in "Secrets" nel momento in cui si crea un app: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management. Al momento l'app di Streamlit (https://ringmilldemo-pfyif5ngahybprhjdorxmd.streamlit.app) ha già un file Secrets con all'interno l'Access Token per Yonder API.

L'entrypoint dell'app è il file RingMill_Data_Extraction.py.

Prendendo ad esempio il file 1_Intro.py:

La chiamata alla Yonder API avviene nelle seguenti righe di codice (line 36-54):

```    # Define the API endpoint, common query parameters, and data
        url = "https://vm11.yonderlabs.com/2.0/text/extractstructured"
        params = {
            "template": "ringmill-intro::001",
            "access_token": os.environ["YONDER_ACCESS_TOKEN"],
            "model_name": "gemini-2.0-flash",
            "cheap_mode": "false",
        }
        data = {
            "refinement": refinement   
        }
                    # Prepare the file payload for the API call
        files = {
            'data': (intro_pdf.name, intro_pdf, 'application/pdf')
        }

        with st.spinner("Extracting Data...", show_time=True):
        # Send the POST request for the current page
            response = requests.post(url, params=params, files=files, data=data, verify=False)
```

Nel caso si voglia modificare il refinement, si può fare modificandolo (ln 27-28):
```#adds refinement to the LLM prompt
refinement = (
    '{"NomeCliente": "All capitalized, must be a company name not a person name you can find in the email. Remove company type from the name like spa, srl, ltd, etc. The company name can not be Ring Mill, Ringmill, Ring-mill, and all other possible combinations","TechnicalRequirements":"Retrieve only Technical Requirements explicitly mentioned and requested in the text or tables. Do not pick them from file names in the fields attachments. Sometimes Technical Requirements appears as separated strings on subsequent rows of a table e.g. EN 10204 3.1"}'
)
```

Per trattare le risposte nulle, ho scritto una piccola funzione che scrive queste riposte nulle come stringa "null". Questa funzione si trova in ln 14-18: 
```def handle_empty(dictionary):
    for key, value in dictionary.items():
        if len(value) == 0:
            dictionary[key] = "null"
    return dictionary
```

Il restante codice serve per mostrare la risposta della API in Streamlit.

