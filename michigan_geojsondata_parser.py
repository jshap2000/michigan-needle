import geopandas as gpd
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt

from scipy.spatial import distance
from sklearn.metrics import pairwise_distances
from scipy.stats import entropy
import numpy as np



current_directory = os.getcwd()

# Path to your GeoJSON file
file_path = '/Users/joshuashapiro/Desktop/michigan-needle/data/geojson/michigan_2022.geojson'

# Reading the GeoJSON file into a GeoDataFrame
gdf = gpd.read_file(file_path)

AGE_CATEGORIES = ['age_18_19', 'age_20_24' ,'age_25_29', 'age_35_44', 'age_45_54', 'age_55_64', 'age_65_74', 'age_75_84', 'age_85over']
PARTY_ID_CATEGORIES = ['party_dem', 'party_rep', 'party_npp']

# Note: in MI eth1_oth is likely arab voters
DEMOGRAPHIC_CATEGORIES = ['eth1_eur', 'eth1_hisp', 'eth1_aa', 'eth1_esa', 'eth1_oth']

# TODO: Income and Education data is not directly available from precinct data and must be pulled from census reports.

total_filters = ['PRECINCTID', 'Precinct_L'] + AGE_CATEGORIES + PARTY_ID_CATEGORIES + DEMOGRAPHIC_CATEGORIES

all_categorical_features = AGE_CATEGORIES + PARTY_ID_CATEGORIES + DEMOGRAPHIC_CATEGORIES

data = gdf[total_filters]

data = data[:2000]

# Function to calculate percentages
def calculate_percentages(df, categories):
    total = df[categories].sum(axis=1)
    df[categories] = df[categories].div(total, axis=0)

# Apply the function to each category group
calculate_percentages(data, AGE_CATEGORIES)
calculate_percentages(data, PARTY_ID_CATEGORIES)
calculate_percentages(data, DEMOGRAPHIC_CATEGORIES)

for category in [AGE_CATEGORIES, PARTY_ID_CATEGORIES, DEMOGRAPHIC_CATEGORIES]:
       data[category] = data[category].fillna(data[category].median())

print((data[AGE_CATEGORIES].sum(axis=1) == 0).any())

# Function to calculate Jensen-Shannon Divergence
def jensen_shannon_divergence(p, q):
    m = 0.5 * (p + q)
    return 0.5 * (entropy(p, m) + entropy(q, m))

# Compute pairwise Jensen-Shannon Divergence for each category
def compute_category_distances(data, categories):
    # Normalize data if not already percentages
    data_normalized = data[categories].div(data[categories].sum(axis=1), axis=0)
    dist_matrix = pairwise_distances(data_normalized, metric=lambda x, y: jensen_shannon_divergence(x, y))
    return dist_matrix

# Compute distances for each category
age_distances = compute_category_distances(data, AGE_CATEGORIES)
print("Age computed")
party_distances = compute_category_distances(data, PARTY_ID_CATEGORIES)
print("Party computed")
demographic_distances = compute_category_distances(data, DEMOGRAPHIC_CATEGORIES)
print("Demographics computed")
print()

# Aggregate these distances (simple average)
total_distances = (age_distances + party_distances + demographic_distances) / 3

# Find nearest neighbors manually
def find_nearest_neighbors(dist_matrix, index, n_neighbors=10):
    distances = dist_matrix[index]
    nearest_indices = np.argsort(distances)[:n_neighbors + 1]  # +1 because the nearest is itself
    return nearest_indices, distances[nearest_indices]

# Example usage: Find 10 nearest neighbors for precinct at index 0
indices, dists = find_nearest_neighbors(total_distances, 0, 10)
print("10 closest precincts to the precinct at index 0:")
for rank, (idx, dist) in enumerate(zip(indices, dists)):
    print(f"Rank {rank}: Precinct Index = {idx}, Distance = {dist}")
    print(data.iloc[idx])