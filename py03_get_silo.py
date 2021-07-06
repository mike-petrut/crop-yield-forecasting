# %% Define function for spatially modelling monethly rain

import pandas as pd
import geopandas as gpd

from py01_helper_fucntions import pull_rainfall

# %%

sa_croplands = gpd.read_file('sa-cereals/sa_cereals_class.shp')

# %%

try:
    sa_crop_rain = pd.read_csv('sa_crop_rain.csv')
except: 
    sa_crop_rain = pull_rainfall(sa_croplands, 1989, 2020)
    sa_crop_rain.to_csv('sa_crop_rain.csv', index = False)
    sa_crop_rain = pd.read_csv('sa_crop_rain.csv', index_col = 'year')

