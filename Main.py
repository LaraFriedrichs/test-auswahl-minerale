import streamlit as st
import json
import requests
from pathlib import Path

# API Request der Daten von Mindat.org im Hintergrund

key= st.secrets["api_key"]
WORKING_DIR = st.secrets["speicherort"]

Path(WORKING_DIR).mkdir(parents=True, exist_ok=True)
MINDAT_API_URL = "https://api.mindat.org"
headers = {'Authorization': 'Token '+ key}
fields_str ='name,ima_formula,ima_status,ima_notes,description_short,mindat_formula,mindat_formula_note'

select_file_name = "mindat_data_IMA_download_2.json" 
select_file_path = Path(WORKING_DIR,select_file_name) 
select_file_path


with open(select_file_path, 'w') as f:
    params = {
        'fields': fields_str,
        'format': 'json'
    }
    response = requests.get(MINDAT_API_URL+"/minerals_ima/",
            params=params,
            headers=headers)

    result_data = response.json()["results"]
    json_data = {"results": result_data}

    while True:
        try:
            next_url = response.json()["next"]
            response = requests.get(next_url, headers=headers)
            json_data["results"] += response.json()['results']

        except requests.exceptions.MissingSchema as e:
            break

    json.dump(json_data, f, indent=4)

st.header("Die Wichtigsten Minerale im Überblick")
st.divider()
st.markdown("Text")
        #with open('test.json','r') as file:
    #obj = json.load(file)