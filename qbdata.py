import pandas as pd 
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('nflData.csv.gz', compression='gzip', low_memory=False)

# filter data to only include qb dropbacks
data = data.loc[data.qb_dropback == 1]

# create a database that groups by quarterbacks
qb = data.groupby(['passer_id', 'passer']).agg({
    'pass': ['sum'],
    'epa': ['mean', 'sum'],
    # Calculate mean cpoe only for plays where cpoe is not NaN
    'cpoe': [('mean', lambda x: x.dropna().mean())],
    # Calculate mean air_yards only for plays where air_yards is not NaN
    'air_yards': [('mean', lambda x: x.dropna().mean())],
    'qb_scramble': ['mean'],
    'sack': ['mean'],
    'interception': ['mean'],
    'success': ['mean'],
    'complete_pass': ['mean']
}).reset_index()

# Flatten the MultiIndex in columns created by the aggregation
qb.columns = ['_'.join(col) if type(col) is tuple else col for col in qb.columns]

# filter for quarterbacks with at least 500 pass attempts 
qb = qb.loc[qb['pass_sum'] >= 500]

# standardize the statistics
scaler = StandardScaler()
# Ensure that 'mean' is appended to 'cpoe' and 'air_yards' to match the new column names
stats_columns = ['epa_mean', 'cpoe_mean', 'air_yards_mean', 'qb_scramble_mean', 'sack_mean', 'interception_mean', 'success_mean', 'complete_pass_mean']
qb[stats_columns] = scaler.fit_transform(qb[stats_columns])

# define weights 
weights = {
    'pass_sum': 0.3, 
    'epa_mean': 3.0, 
    'epa_sum': 0.3,   
    'cpoe_mean': 2.0, 
    'air_yards_mean': 2.0, 
    'qb_scramble_mean': 9.0, 
    'sack_mean': -4.5,  
    'interception_mean': -4.5, 
    'success_mean': 0.5,  
    'complete_pass_mean': 1.0  
}

# compute aggregate statistic
qb['aggregate_stat'] = sum(qb[col] * weight for col, weight in weights.items())

# save the data to a csv file 
qb.to_csv('processed_qb_data.csv', index=False)
