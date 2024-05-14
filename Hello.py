import streamlit as st
import requests

st.header('An Overview of the Most Important Minerals')
st.divider()
st.markdown('This app can be used to get information about the most important minerals in geoscience. The information provided here is requested from mindat.org.')
st.divider()
selected_fields = st.multiselect(label='Which information do you want to get?', options=['name', 'mindat_formula', 'ima_formula', 'description_short'])
fields_str = ",".join(selected_fields)

# Lists of important minerals

garnets         = ["Pyrope", "Almandine", "Spessartine", "Grossular"]
oxides          = ["Quartz", "Rutile", "Hematite", "Ilmenite", "Chromite", "Magnetite"]
alumnosilicates = ["Kyanite","Sillimanite","Andalusite"]
sulfates        = ["Gypsum","Baryte","Anhydryte"]
Sulfides        = ["Pyrite","Chalkopyrite"]
carbonates      = ["Calcite","Aragonite","Dolomite","Ankerite","Siderite","Magnesite"]
feldspars       = ["Orthoclas","Albite","Sanidine","Microclin","Anorthite"]
foids           = ["Nepheline","Leucite","Sodalite","Nosean","Hayun"]
Pyroxenes       = ["Enstatite","Ferrosilite","Diopside","Hedenbergite","Augite","Jadeite","Omphacite"]
clay_minerals   = ["Kaolinite","Illit","Montmorillonite","Vermiculite"]
micas           = ["Phlogopite","Annite","Eastonite","Muscovite","Phengite","Paragonite"]
Amphiboles      = ["Tremolite","Aktinolite","Glaucophane","Riebeckite"]
layeredsilicates= ["Lizadrdit","Chrysotile","Antigorite","Talk","Chlorite","Clinochlor","Chamosite"]
ringsilicates   = ["Tourmaline"]
groupsilicates  = ["Lawsonite","Epidote","Zoisite"]
nesosilicates   = ["Olivine","Zircon","Titanite","Staurolite"]
phosphates      = ["Apatite","Monazite"]

all_important_minerals=["Pyrope","Almandine","Spessartine","Grossular","Kyanite",
                        "Sillimanite","Andalusite","Gypsum","Baryte","Anhydryte",
                        "Pyrite","Chalkopyrite","Calcite","Aragonite","Dolomite",
                        "Ankerite","Siderite","Magnesite","Orthoclas","Albite",
                        "Sanidine","Microclin","Anorthite","Nepheline","Leucite",
                        "Sodalite","Nosean","Hayun","Enstatite","Ferrosilite",
                        "Diopside","Hedenbergite","Jadeite","Omphacite",
                        "Kaolinite","Illit","Montmorillonite","Vermiculite",
                        "Phlogopite","Annite","Eastonite","Muscovite","Phengite",
                        "Paragonite","Quartz","Rutile","Hematite","Illmenite",
                        "Chromite","Magnetite","Tremolite","Aktinolit","Glaucophane",
                        "Riebeckite","Lizadrdit","Augite"
                        "Chrysotile","Antigorite","Talk","Chlorite","Clinochlor",
                        "Chamosite","Tourmaline","Lawsonite","Epidote","Zoisite",
                        "Olivine","Zircon","Titanite","Staurolite","Apatite","Monazite"]

mineral_groups = {
    "Garnets": garnets,
    "Oxides": oxides,
    "Micas":micas,
    "Amphiboles":Amphiboles,
    "Pyroxenes":Pyroxenes,
    "Clay Minerals":clay_minerals,
    "Carbonates":carbonates,
    "Sulfates":sulfates,
    "Sulfides":Sulfides,
    "Phosphates":phosphates,
    "Neso slicates":nesosilicates,
    "Ring silicates":ringsilicates,
    "Group silicates":groupsilicates,
    "Layered silicates":layeredsilicates,
    "Alumnosilicates":alumnosilicates,
    "Feldspars":feldspars,
    "Foids":foids,
    "all groups":all_important_minerals
}

group_name = st.selectbox(label="Which group of minerals do you want to look at?", options=list(mineral_groups.keys()))
important_minerals = mineral_groups[group_name]
st.divider()

if st.button(label='Start requesting Information!'):
    st.write("The selectes Information for your choosen group of minerals are requested from Mindat.org. This process can take some minutes....")
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
