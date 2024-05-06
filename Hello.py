import streamlit as st
import json
import requests

#st.write('Hallo')

key= st.secrets.api_key
MINDAT_API_URL = "https://api.mindat.org"
headers = {'Authorization': 'Token '+ key}
fields_str ='name,ima_formula,description_short,mindat_formula'
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

for result in json_data["results"]:
    # Accessing specific fields of each result
    name = result["name"]
    ima_formula = result["ima_formula"]
    description_short = result["description_short"]
    mindat_formula = result["mindat_formula"]
    print(f"Name: {name}, IMA Formula: {ima_formula},Description: {description_short}, MINDAT Formula: {mindat_formula}")

#for v in json_data.values():
    #if 'Si' in str:
        #print(v)
