import geopandas as gpd
import os

current_directory = os.getcwd()

# Path to your GeoJSON file
file_path = current_directory + '/data/geojson/michigan_2022.geojson'

# Reading the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(file_path)

AGE_CATEGORIES = ['age_18_19', 'age_20_24' ,'age_25_29', 'age_35_44', 'age_45_54', 'age_55_64', 'age_65_74', 'age_75_84', 'age_85over']
PARTY_ID_CATEGORIES = ['party_dem', 'party_rep', 'party_npp']

# Note: in MI eth1_oth is likely arab voters
DEMOGRAPHIC_CATEGORIES = ['eth1_eur', 'eth1_hisp', 'eth1_aa', 'eth1_esa', 'eth1_oth']

# TODO: Income and Education data is not directly available from precinct data and must be pulled from census reports.

total_filters = ['PRECINCTID', 'Precinct_L'] + AGE_CATEGORIES + PARTY_ID_CATEGORIES + DEMOGRAPHIC_CATEGORIES

gdf_filtered = gdf[total_filters]

# Display the GeoDataFrame
print(gdf_filtered.columns)