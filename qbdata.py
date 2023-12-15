import pandas as pd 
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('nflData.csv.gz', compression='gzip', low_memory=False)

# filter data to only include passing plays and plays where cpoe and air_yards are not null
data = data.loc[(data.play_type == 'pass') & (data.cpoe.notna()) & (data.air_yards.notna())]

# create a database that groups by quarterbacks
qb = data.groupby(['passer_id', 'passer']).agg({
    'pass': ['sum'],
    'epa': ['mean', 'sum'],
    'cpoe': ['mean'],
    'air_yards': ['mean'],
    'qb_scramble': ['mean'],
    'sack': ['mean'],
}).reset_index()

qb.columns = ['_'.join(col) if type(col) is tuple else col for col in qb.columns]

# filter for quarterbacks with at least 200 pass attempts 
qb = qb.loc[qb['pass_sum'] >= 200]

# standardize the statistics
scaler = StandardScaler()
stats_columns = ['pass_sum', 'epa_mean', 'epa_sum', 'cpoe_mean', 'air_yards_mean', 'qb_scramble_mean', 'sack_mean']
qb[stats_columns] = scaler.fit_transform(qb[stats_columns])

# define weights 
weights = {
    'pass_sum': 0.5, 
    'epa_mean': 2.0, 
    'epa_sum': 1.0, 
    'cpoe_mean': 1.5, 
    'air_yards_mean': 2.0, 
    'qb_scramble_mean': 2.0, 
    'sack_mean': 2.0
}

# compute aggregate statistic
qb['aggregate_stat'] = sum(qb[col] * weight for col, weight in weights.items())

# save the data to a csv file 
qb.to_csv('processed_qb_data.csv', index=False)