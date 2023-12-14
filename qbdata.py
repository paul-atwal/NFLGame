import pandas as pd 

data = pd.read_csv('nflData.csv.gz', compression='gzip', low_memory=False)

# create new column for 

# create a database that groups by quarterbacks (including their entire career) 
qb = data.groupby(['passer_id', 'passer']).agg({
    'epa': ['mean', 'sum'],
    'cpoe': ['mean'],
    'air_yards': ['mean'],
    'qb_scramble': ['mean'],
    'sack': ['mean'],
    }).reset_index()

print(qb.head())