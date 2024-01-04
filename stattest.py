import pandas as pd
import numpy as np

def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

# Load the processed data
qb_data = pd.read_csv('processed_qb_data.csv') 

stats_columns = ['epa_mean','cpoe_mean', 'air_yards_mean', 'qb_scramble_mean', 'sack_mean', 'interception_mean', 'success_mean', 'complete_pass_mean']

quarterbacks_to_compare = ['T.Brady', 'M.Vick', 'P.Mahomes', 'P.Manning', 'B.Favre', 'J.Allen']

for qb_name in quarterbacks_to_compare:
    # Get the vector for the selected quarterback
    qb_vector = qb_data[qb_data['passer_'] == qb_name].iloc[0]

    # Calculate distance to every other quarterback
    distances = qb_data.apply(lambda row: euclidean_distance(row[stats_columns], qb_vector[stats_columns]), axis=1)
    
    # Get the five most similar quarterbacks
    closest_qbs = qb_data.loc[distances.nsmallest(6).index] 
    # closest_qbs = closest_qbs[closest_qbs['passer_'] != qb_name] 

    print(f"Quarterbacks most similar to {qb_name}:")
    # Include scores for each category in addition to the quarterback names
    display_columns = ['passer_id_', 'passer_'] + stats_columns
    print(closest_qbs[display_columns])
    print("\n")
