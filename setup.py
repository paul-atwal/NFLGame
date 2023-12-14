import pandas as pd

YEARS = range(1999, 2023) 

data = pd.DataFrame()

for year in YEARS:  
    url = f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.csv.gz'
    i_data = pd.read_csv(url, compression='gzip', low_memory=False)
    data = data._append(i_data, sort=True)

# Data cleanup. Removing special teams plays and kneeldowns 
data = data.loc[(data.play_type.isin(['no_play','pass','run'])) & (data.epa.isna()==False)]

# Updating play type to properly reflect QB scrambles as passing plays 
data.loc[data['pass'] == 1, 'play_type'] = 'pass'
data.loc[data['rush'] == 1, 'play_type'] = 'run'

data.to_csv('nflData.csv.gz', compression='gzip', index=False)