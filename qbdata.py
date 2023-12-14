import pandas as pd 

data = pd.read_csv('nflData.csv.gz', compression='gzip', low_memory=False)

# create new column for 

# filter data to only include passing plays and plays where cpoe and air_yards are not null
data = data.loc[(data.play_type == 'pass') & (data.cpoe.isna()==False) & (data.air_yards.isna()==False)]

# create a database that groups by quarterbacks (including their entire career) 
qb = data.groupby(['passer_id', 'passer']).agg({
    'pass': ['sum'],
    'epa': ['mean', 'sum'],
    'cpoe': ['mean'],
    'air_yards': ['mean'],
    'qb_scramble': ['mean'],
    'sack': ['mean'],
    }).reset_index()

# filter for quarterbacks with at least 200 pass attempts 
qb = qb.loc[qb['pass']['sum'] >= 200]

print(qb.head())