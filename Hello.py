import streamlit as st
import requests

st.header('An Overview of the Most Important Minerals')
st.markdown('This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.')

selected_fields = st.multiselect(label='Which information do you want to get?', options=['name', 'mindat_formula', 'ima_formula', 'description_short'])
fields_str = ",".join(selected_fields)

# List of important minerals to display
#important_minerals = garnets #["Olivine","Quarz","Calcite","Aragonite","Pyrope","Almandine", "Rhodolite","Spessartine","Grossular","Andradite","Uvarovite"]

garnets=["Pyrope","Almandine","Spessartine","Grossular"]
alumnosilicates=["Kyanite","Sillimanite","Andalusite"]
sulfates=["Gypsum","Baryte","Anhydryte"]
Sulfides=["Pyrite","Chalkopyrite"]
carbonates=["Calzite","Aragonite","Dolomite","Ankerite","Siderite","Magnesite"]
feldspars=["Orthoclas","Albite","Sanidine","Microclin","Anorthite"]
foids=["Nepheline","Leucite","Sodalite","Nosean","Hayun"]
Pyroxenes=["Enstatite","Ferrosilite","Diopside","Hedenbergite","Jadeite","Augit","Omphazite"]
clay_minerals=["Kaolinite","Illit","Montmorrilonite","Vermiculite"]
micas=["Phlogopite","Annit","Eastonite","Muscovite","Phengit","Paragonite"]
oxides=["Quartz","Rutile","Hematite","Illmenite","Chromite","Magnetite"]
Amphiboles=["Tremolit","Aktinolit","Glaukophan","Riebeckit","Hornblende","Anthophyllit","Gredit"]
layeredsilicates=["Lizadrdit","Chrysotile","Antigorite","Talk","Chlorite","Clinochlor","Chamosite"]
ringsilicates=["Tourmaline"]
groupsilicates=["Lawsonite","Epidote","Zoisite"]
nesosilicates=["Olivine","Zircon","Titanite","Staurolite"]
phosphates=["Apatite","Monazite"]

all_important_minerals=["Pyrope","Almandine","Spessartine","Grossular","Kyanite",
                        "Sillimanite","Andalusite","Gypsum","Baryte","Anhydryte",
                        "Pyrite","Chalkopyrite","Calzite","Aragonite","Dolomite",
                        "Ankerite","Siderite","Magnesite","Orthoclas","Albite",
                        "Sanidine","Microclin","Anorthite","Nepheline","Leucite",
                        "Sodalite","Nosean","Hayun","Enstatite","Ferrosilite",
                        "Diopside","Hedenbergite","Jadeite","Augit","Omphazite",
                        "Kaolinite","Illit","Montmorrilonite","Vermiculite",
                        "Phlogopite","Annit","Eastonite","Muscovite","Phengit",
                        "Paragonite","Quartz","Rutile","Hematite","Illmenite",
                        "Chromite","Magnetite","Tremolit","Aktinolit","Glaukophan",
                        "Riebeckit","Hornblende","Anthophyllit","Gredit","Lizadrdit",
                        "Chrysotile","Antigorite","Talk","Chlorite","Clinochlor",
                        "Chamosite","Tourmaline","Lawsonite","Epidote","Zoisite",
                        "Olivine","Zircon","Titanite","Staurolite","Apatite","Monazite"]
important_minerals = st.selectbox(label="Which group of minerals you want to look at?",options=[garnets,oxides])

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
