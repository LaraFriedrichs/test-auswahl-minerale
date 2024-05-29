import streamlit as st
import requests

st.header('An Overview of the Most Important Minerals')
st.markdown('This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.')

selected_fields = st.multiselect(label='Which information do you want to get?', options=['name', 'mindat_formula', 'ima_formula', 'description_short'])
fields_str = ",".join(selected_fields)

# Lists of important minerals
garnets = ["Pyrope", "Almandine", "Spessartine", "Grossular"]
aluminosilicates = ["Kyanite","Sillimanite","Andalusite"]
sulfates        = ["Gypsum","Baryte","Anhydrite"]
sulfides        = ["Pyrite","Chalcopyrite"]
carbonates      = ["Calcite","Aragonite","Dolomite","Ankerite","Siderite","Magnesite"]
feldspars       = ["Orthoclase","Albite","Sanidine","Microcline","Anorthite"]
foids           = ["Nepheline","Leucite","Sodalite","Nosean","Haüyne"]
pyroxenes       = ["Enstatite","Ferrosilite","Diopside","Hedenbergite","Augite","Jadeite","Omphacite"]
clay_minerals   = ["Kaolinite","Illite","Montmorillonite","Vermiculite"]
micas           = ["Phlogopite","Annite","Eastonite","Muscovite","Phengite","Paragonite"]
amphiboles      = ["Tremolite","Actinolite","Glaucophane","Riebeckite"]
layered_silicates= ["Lizardite","Chrysotile","Antigorite","Talc","Chlorite","Clinochlore","Chamosite"]
ring_silicates  = ["Tourmaline"]
group_silicates = ["Lawsonite","Epidote","Zoisite"]
nesosilicates   = ["Olivine","Zircon","Titanite","Staurolite"]
phosphates      = ["Apatite","Monazite"]
oxides = ["Quartz", "Rutile", "Hematite", "Ilmenite", "Chromite", "Magnetite"]
important_minerals=["Pyrope", "Almandine", "Spessartine", "Grossular", "Kyanite",
            "Sillimanite", "Andalusite", "Gypsum", "Baryte", "Anhydryte",
            "Pyrite", "Chalcopyrite", "Calcite", "Aragonite", "Dolomite",
            "Ankerite", "Siderite", "Magnesite", "Orthoclase", "Albite",
            "Sanidine", "Microcline", "Anorthite", "Nepheline", "Leucite",
            "Sodalite", "Nosean", "Haüyne", "Enstatite", "Ferrosilite",
            "Diopside", "Hedenbergite", "Jadeite", "Omphacite",
            "Kaolinite", "Illite", "Montmorillonite", "Vermiculite",
            "Phlogopite", "Annite", "Eastonite", "Muscovite", "Phengite",
            "Paragonite", "Quartz", "Rutile", "Hematite", "Ilmenite",
            "Chromite", "Magnetite", "Tremolite", "Actinolite", "Glaucophane",
            "Riebeckite", "Lizadrdite", "Augite", "Chrysotile", "Antigorite",
            "Talc", "Chlorite", "Clinochlor", "Chamosite", "Tourmaline",
            "Lawsonite", "Epidote", "Zoisite", "Olivine", "Zircon", "Titanite", "Staurolite", "Apatite", "Monazite"
        ]
# Add more lists as needed


mineral_groups = {
        "Garnets": ["Pyrope", "Almandine", "Spessartine", "Grossular"],
        "Oxides": ["Quartz", "Rutile", "Hematite", "Ilmenite", "Chromite", "Magnetite"],
        "Micas": ["Phlogopite", "Annite", "Eastonite", "Muscovite", "Phengite", "Paragonite"],
        "Amphiboles": ["Tremolite", "Actinolite", "Glaucophane", "Riebeckite"],
        "Pyroxenes": ["Enstatite", "Ferrosilite", "Diopside", "Hedenbergite", "Jadeite", "Omphacite"],
        "Clay Minerals": ["Kaolinite", "Illite", "Montmorillonite", "Vermiculite"],
        "Carbonates": ["Calcite", "Aragonite", "Dolomite", "Ankerite", "Siderite", "Magnesite"],
        "Sulfates": ["Gypsum", "Baryte", "Anhydryte"],
        "Sulfides": ["Pyrite", "Chalcopyrite"],
        "Phosphates": ["Apatite", "Monazite"],
        "Nesoslicates": ["Olivine", "Zircon", "Titanite", "Staurolite"],
        "Ring silicates": ["Tourmaline"],
        "Group silicates": ["Lawsonite", "Epidote", "Zoisite"],
        "Layered silicates": ["Lizadrdite", "Chrysotile", "Antigorite", "Talc", "Chlorite", "Clinochlor", "Chamosite"],
        "Alumnosilicates": ["Kyanite", "Sillimanite", "Andalusite"],
        "Feldspars": ["Orthoclase", "Albite", "Sanidine", "Microcline", "Anorthite"],
        "Foids": ["Nepheline", "Leucite", "Sodalite", "Nosean", "Haüyne"],
        "all groups": [
            "Pyrope", "Almandine", "Spessartine", "Grossular", "Kyanite",
            "Sillimanite", "Andalusite", "Gypsum", "Baryte", "Anhydryte",
            "Pyrite", "Chalcopyrite", "Calcite", "Aragonite", "Dolomite",
            "Ankerite", "Siderite", "Magnesite", "Orthoclase", "Albite",
            "Sanidine", "Microcline", "Anorthite", "Nepheline", "Leucite",
            "Sodalite", "Nosean", "Haüyne", "Enstatite", "Ferrosilite",
            "Diopside", "Hedenbergite", "Jadeite", "Omphacite",
            "Kaolinite", "Illite", "Montmorillonite", "Vermiculite",
            "Phlogopite", "Annite", "Eastonite", "Muscovite", "Phengite",
            "Paragonite", "Quartz", "Rutile", "Hematite", "Ilmenite",
            "Chromite", "Magnetite", "Tremolite", "Actinolite", "Glaucophane",
            "Riebeckite", "Lizadrdite", "Augite", "Chrysotile", "Antigorite",
            "Talc", "Chlorite", "Clinochlor", "Chamosite", "Tourmaline",
            "Lawsonite", "Epidote", "Zoisite", "Olivine", "Zircon", "Titanite", "Staurolite", "Apatite", "Monazite"
        ]
    }


group_name = st.selectbox(label="Which group of minerals do you want to look at?", options=list(mineral_groups.keys()))
important_minerals = mineral_groups[group_name]

if st.button(label='Start',use_container_width=True):
    key = st.secrets["api_key"]
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
            st.markdown(f"### Details of Selected Important Minerals from the {group_name} Group")
            for result in filtered_results:
                with st.expander(f"**{result.get('name', 'N/A')}**"):
                    name = result.get("name", "N/A")
                    ima_formula = result.get("ima_formula", "N/A")
                    description_short = result.get("description_short", "N/A")
                    mindat_formula = result.get("mindat_formula", "N/A")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**IMA Formula:** {ima_formula}")
                        st.markdown(f"**MINDAT Formula:** {mindat_formula}")
                    with col2:
                        st.markdown(f"**Description:** {description_short}")

