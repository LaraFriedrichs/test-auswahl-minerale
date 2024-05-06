import streamlit as st
import json
import requests
st.header('An Overview of the most important minerals')
st.markdown('This App can be used to get information about the most important minerals in geosience. The information provided here are requested from mindat.org.')

if st.button(label='go on'):
    key= st.secrets.api_key
    MINDAT_API_URL = "https://api.mindat.org"
    headers = {'Authorization': 'Token '+ key}
    selected_fields=st.multiselect(label='Which Information do you want to get?',options=['name','mindat_formula','ima_formula','desccription_short'])#fields_str ='name,ima_formula,description_short,mindat_formula'
    field_str =selected_fields[0:]
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

#for result in json_data["results"]:
    #name = result["name"]
    #ima_formula = result["ima_formula"]
    #description_short = result["description_short"]
    #mindat_formula = result["mindat_formula"]
    #print(f"Name: {name}, IMA Formula: {ima_formula},Description: {description_short}, MINDAT Formula: {mindat_formula}")
##################################################################################################################################
#for v in json_data.values():
    #if 'Si' in str:
        #print(v)
