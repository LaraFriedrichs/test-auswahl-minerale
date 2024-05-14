import streamlit as st
import requests

st.header('An Overview of the Most Important Minerals')
st.markdown('This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.')

selected_fields = st.multiselect(label='Which information do you want to get?', options=['name', 'mindat_formula', 'ima_formula', 'description_short'])
fields_str = ",".join(selected_fields)

# List of important minerals to display
important_minerals = ["Abelsonite"]

if st.button(label='Start'):
    key = st.secrets["api_key"]  # Adjusted to use square brackets
    MINDAT_API_URL = "https://api.mindat.org"
    headers = {'Authorization': 'Token ' + key}

    params = {
        'fields': fields_str,
        'format': 'json'
    }
    
    response = requests.get(MINDAT_API_URL + "/minerals_ima/", params=params, headers=headers)
    if response.status_code != 200:
        st.error("Failed to fetch data from the API.")
    else:
        json_data = {"results": response.json().get("results", [])}
        
        while response.json().get("next"):
            next_url = response.json()["next"]
            response = requests.get(next_url, headers=headers)
            if response.status_code == 200:
                json_data["results"] += response.json().get("results", [])
            else:
                break
        
        # Filter results for important minerals
        filtered_results = [result for result in json_data["results"] if result.get("name") in important_minerals]
        
        if not filtered_results:
            st.warning("No data found for the selected minerals.")
        else:
            st.markdown("### Details of Selected Important Minerals")
            for result in filtered_results:
                name = result.get("name", "N/A")
                ima_formula = result.get("ima_formula", "N/A")
                description_short = result.get("description_short", "N/A")
                mindat_formula = result.get("mindat_formula", "N/A")
                st.markdown(f"**Name:** {name}\n\n**IMA Formula:** {ima_formula}\n\n**Description:** {description_short}\n\n**MINDAT Formula:** {mindat_formula}")
