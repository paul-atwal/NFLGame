from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the processed QB data
qb_data = pd.read_csv('processed_qb_data.csv')

stats_columns = ['epa_mean', 'cpoe_mean', 'air_yards_mean', 'qb_scramble_mean', 'sack_mean', 'interception_mean', 'success_mean', 'complete_pass_mean']

def euclidean_distance(vec1, vec2):
    return np.sqrt(np.sum((vec1 - vec2) ** 2))

def find_similar_qbs(qb_name, qb_data, stats_columns, n_similar=5):
    # Ensure the QB name is in the data
    if qb_name not in qb_data['passer_'].values:
        return []

    # Get the vector for the selected quarterback
    qb_vector = qb_data[qb_data['passer_'] == qb_name].iloc[0]

    # Calculate distance to every other quarterback
    distances = qb_data.apply(lambda row: euclidean_distance(row[stats_columns], qb_vector[stats_columns]), axis=1)

    # Get the n_similar most similar quarterbacks, excluding the selected QB
    closest_qbs = qb_data.loc[distances.nsmallest(n_similar + 1).index]
    closest_qbs = closest_qbs[closest_qbs['passer_'] != qb_name]

    # Return the list of similar QB names
    return closest_qbs['passer_'].tolist()

@app.route('/random-qb')
def random_qb():
    # Select a random QB name from the data
    return jsonify(np.random.choice(qb_data['passer_'].unique()))

@app.route('/similar-qbs/<string:qb_name>')
def similar_qbs(qb_name):
    similar = find_similar_qbs(qb_name, qb_data, stats_columns)
    return jsonify(similar)

@app.route('/qb-names')
def qb_names():
    return jsonify(list(qb_data['passer_'].unique()))

if __name__ == '__main__':
    app.run(debug=True)
