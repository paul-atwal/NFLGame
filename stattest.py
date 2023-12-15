import pandas as pd
import numpy as np

def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

# Load the processed data
qb_data = pd.read_csv('processed_qb_data.csv')  # Update with your actual filename

stats_columns = ['pass_sum', 'epa_mean', 'epa_sum', 'cpoe_mean', 'air_yards_mean', 'qb_scramble_mean', 'sack_mean']

# List of quarterbacks to compare (in the format "Initial.LastName")
quarterbacks_to_compare = ['T.Brady', 'M.Vick', 'P.Mahomes', 'P.Manning', 'B.Favre', 'J.Allen']

# Ensure the name and id columns match your DataFrame
for qb_name in quarterbacks_to_compare:
    # Get the vector for the selected quarterback
    qb_vector = qb_data[qb_data['passer'] == qb_name].iloc[0]

    # Calculate distance to every other quarterback
    distances = qb_data.apply(lambda row: euclidean_distance(row[stats_columns], qb_vector[stats_columns]), axis=1)
    
    # Get the three most similar quarterbacks
    closest_qbs = qb_data.loc[distances.nsmallest(4).index]  # Top 4 because it includes the quarterback itself
    closest_qbs = closest_qbs[closest_qbs['passer'] != qb_name]  # Exclude the quarterback itself

    print(f"Quarterbacks most similar to {qb_name}:")
    print(closest_qbs[['passer_id', 'passer']])
    print("\n")

