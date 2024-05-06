import streamlit as st
import json
import requests

key= st.secrets.api_key
MINDAT_API_URL = "https://api.mindat.org"
headers = {'Authorization': 'Token '+ key}
fields_str ='name,ima_formula,ima_status,ima_notes,description_short,mindat_formula,mindat_formula_note'
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
results = json_data["results"]


