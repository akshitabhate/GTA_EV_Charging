import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd

# Load GTA and Toronto Hydro service area GeoJSON files
gta_geojson = 'data/Toronto2.geojson'
ev_charing_station_geojson = 'data/Toronto_City_EV_Chargers_WGS84.geojson'

gta = gpd.read_file(gta_geojson)
ev_stations = gpd.read_file(ev_charing_station_geojson)

# Load EV sales data for each quarter
ev_sales_files = {
    "Q1 2022": 'data/ev_sales/q1_2022.csv',
    "Q2 2022": 'data/ev_sales/q2_2022.csv',
    "Q3 2022": 'data/ev_sales/q3_2022.csv',
    "Q4 2022": 'data/ev_sales/q4_2022.csv',
    "Q1 2023": 'data/ev_sales/q1_2023.csv',
    "Q2 2023": 'data/ev_sales/q2_2023.csv',
    "Q3 2023": 'data/ev_sales/q3_2023.csv',
    "Q4 2023": 'data/ev_sales/q4_2023.csv',
    "Q1 2024": 'data/ev_sales/q1_2024.csv',
    "Q2 2024": 'data/ev_sales/q2_2024.csv'
}

# Initialize session state for the selected quarter
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = 0

# Slider to select the quarter dynamically
quarter_names = list(ev_sales_files.keys())
selected_index = st.slider("Select Quarter", 0, len(quarter_names) - 1, step=1, key='slider', value=st.session_state.selected_index)

# Update session state whenever slider moves manually
st.session_state.selected_index = selected_index

# Get the selected quarter
selected_quarter = quarter_names[st.session_state.selected_index]

# Load the selected quarter's EV sales data
ev_sales = pd.read_csv(ev_sales_files[selected_quarter])

# Merge the EV sales data with the GTA GeoDataFrame
gta = gta.merge(ev_sales, left_on='CFSAUID', right_on='FSA')

# Initialize a Folium map centered on the GTA
m = folium.Map(location=[43.7, -79.4], zoom_start=10)

# Add the GTA boundaries
folium.GeoJson(gta, name='GTA').add_to(m)

# Filter Level 2 and Level 3 stations
level_2_stations = ev_stations[ev_stations['Level2_Charging_Ports'] > 0]
level_3_stations = ev_stations[ev_stations['Level3_Charging_Ports'] > 0]

# Sidebar or main area checkboxes for toggling layers
show_level_2 = st.checkbox('Show Level 2 Chargers', value=True)
show_level_3 = st.checkbox('Show Level 3 Chargers', value=True)
show_heatmap = st.checkbox('Show EV Sales Heatmap', value=True)

# Conditionally add Level 2 chargers to the map
if show_level_2:
    for _, station in level_2_stations.iterrows():
        centroid = station.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=station['Location'],  # Replace with the appropriate field name
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

# Conditionally add Level 3 chargers to the map
if show_level_3:
    for _, station in level_3_stations.iterrows():
        centroid = station.geometry.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=station['Location'],  # Replace with the appropriate field name
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

# Conditionally add EV sales heatmap to the map
if show_heatmap:
    # Use the geographic CRS for computing centroids
    heat_data = [[point.y, point.x, value] for point, value in zip(gta.geometry.centroid, gta['TotalEV'])]
    HeatMap(heat_data).add_to(m)

# Display the map in Streamlit
st.title("City-Operated EV Charging Stations in Greater Toronto Area")
st.write(f"This map displays the locations of city-operated electric vehicle charging stations in the Greater Toronto Area with options to view Level 2 or Level 3 chargers, and an EV sales heatmap for {selected_quarter}.")
st_folium(m, width=800, height=600)