#%% 

import ee
from ee.data import exportTable
import eemont
import re
from datetime import datetime
import pandas as pd
import numpy as np
from pandas.core import frame
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

from py01_helper_fucntions import ee_collection_pull, monthly_rain, process_gdf, process_index_table, process_index_table2

#%%

sa_evi = process_index_table('sa_all_polygons_evi.csv')
sa_ndvi = process_index_table('sa_all_polygons_ndvi.csv')
sa_ndsi = process_index_table('sa_all_polygons_ndsi.csv')
sa_nbr = process_index_table('sa_all_polygons_nbrt.csv')
sa_yield = pd.read_csv('sa_yield.csv', index_col = 'year')
sa_rain = pd.read_csv('sa_crop_rain.csv', index_col = 'year')

#%%

sa_regression_table = pd.concat([sa_evi, sa_ndvi, sa_ndsi, 
                                 sa_nbr, sa_yield, sa_rain], axis = 1)

sa_regression_table = sa_regression_table[sa_regression_table.index != 2021]

sa_regression_pred = pd.concat([sa_evi, sa_ndsi, sa_nbr], axis = 1)

sa_regression_pred = sa_regression_pred[sa_regression_pred.index == 2021].to_numpy()

# %%

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), constrained_layout = True)

sns.regplot('EVI', 
            'Yield', 
             ax = ax1, 
             data = sa_regression_table,
             color="purple")

# Add a diagonal line
ax1.plot((0, 1), (0, 1), transform = ax1.transAxes, ls='--', c='k')

ax1.set_title("EVI vs Crop Yield; \n South Australia, 1989 - 2020", fontsize = 24)

ax1.set_xlabel('Enhanced Vegetation Index (EVI)', fontsize=20)
ax1.set_ylabel('Cereals Crop Yield (tonnes / ha)', fontsize=20)

# Set tick font size
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
	label.set_fontsize(18)


sns.regplot('NDVI', 
            'Yield', 
            ax = ax2,
            data = sa_regression_table,
            color="blue")

# Add a diagonal line
ax2.plot((0, 1), (0, 1), transform = ax2.transAxes, ls='--', c='k')

ax2.set_title("NDVI vs Crop Yield; \n South Australia, 1989 - 2020", fontsize = 24)
ax2.set_xlabel('Normalized Difference Vegetation Index', fontsize=20)
ax2.set_ylabel('Cereals Crop Yield (tonnes / ha)', fontsize=20)

# Set tick font size
for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
	label.set_fontsize(18)

plt.savefig('plot03_evi_vs_ndvi.jpg')

# %%

### EVI VS YIELD ###

x = sa_regression_table['EVI'].to_numpy()
y = sa_regression_table['Yield'].to_numpy() 

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# To get coefficient of determination (_squared)

print("r-squared:", r_value**2)
print("p-value:", p_value)

# %%

### NDVI VS YIELD ###

x = sa_regression_table['NDVI'].to_numpy()
y = sa_regression_table['Yield'].to_numpy() 

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# To get coefficient of determination (_squared)

print("r-squared:", r_value**2)
print("p-value:", p_value)


####################################
#         REGRESSION TESTING       #
####################################

# %%

from sklearn.linear_model import LinearRegression

yield_np = sa_regression_table['Yield'].to_numpy()
exog_np = sa_regression_table[['EVI', 'NDSI', 'NBRT']].to_numpy()

model = LinearRegression().fit(exog_np, yield_np)

r_sq = model.score(exog_np, yield_np)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)

y_pred = model.predict(sa_regression_pred)
y_pred

# %%

# %%
