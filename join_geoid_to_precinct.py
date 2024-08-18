import geopandas as gpd
import pandas as pd
import json

# Load the geoid and precinct shapefiles
geoids = gpd.read_file("/Users/joshuashapiro/Desktop/geoid.shp")
precincts = gpd.read_file("/Users/joshuashapiro/Desktop/precincts.shp")

# Check and set CRS
if geoids.crs is None:
    # Set the CRS to a known CRS; example uses WGS 84 (EPSG:4326)
    geoids.set_crs('epsg:4326', inplace=True)
if precincts.crs is None:
    # Set the CRS to a known CRS; example uses WGS 84 (EPSG:4326)
    precincts.set_crs('epsg:4326', inplace=True)

# Ensure both datasets are in the same coordinate system
if geoids.crs != precincts.crs:
    geoids = geoids.to_crs(precincts.crs)

intersections = gpd.sjoin(geoids, precincts, how="inner", predicate='intersects')

# Calculate the intersection area
intersections['intersection_area'] = intersections.apply(
    lambda row: geoids.geometry[row.name].intersection(precincts.geometry[row.index_right]).area,
    axis=1
)

intersections = intersections.merge(precincts.area.rename('precinct_area'), left_on='index_right', right_index=True)

# Now calculate the percentage coverage
intersections['precinct_pct'] = intersections['intersection_area'] / intersections['precinct_area'] * 100

# Filter rows where the containment is 85% or more of the geoid
intersections['geoid_pct'] = intersections['intersection_area'] / geoids.area.loc[intersections.index] * 100
contained_geoids = intersections[intersections['geoid_pct'] >= 0]

# Create a list of dictionaries mapping geoid to percentage of precinct coverage
contained_geoids['geoid_precinct_pct_map'] = contained_geoids.apply(
    lambda row: {row['LINK']: row['precinct_pct']},
    axis=1
)

mapping_df = contained_geoids.groupby('PRECINCTID')['geoid_precinct_pct_map'].agg(list).reset_index()

print(mapping_df)