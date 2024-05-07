import streamlit as st
import requests

st.header('An Overview of the most important minerals')
st.markdown('This App can be used to get information about the most important minerals in geoscience. The information provided here are requested from mindat.org.')

selected_fields = st.multiselect(label='Which Information do you want to get?',options=['name', 'mindat_formula', 'ima_formula', 'description_short'])
fields_str = ",".join(selected_fields)

if st.button(label='Start'):
    key= st.secrets.api_key
    MINDAT_API_URL = "https://api.mindat.org"
    headers = {'Authorization': 'Token '+ key}

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
    
    for result in json_data["results"]:
        name = result.get("name")
        ima_formula = result.get("ima_formula")
        description_short = result.get("description_short")
        mindat_formula = result.get("mindat_formula")
        st.write(f"Name: {name}, IMA Formula: {ima_formula}, Description: {description_short}, MINDAT Formula: {mindat_formula}")

    #el=st.checkbox(label='Si')
    #for v in json_data.values():
        #if el in str:
            #print(v)

