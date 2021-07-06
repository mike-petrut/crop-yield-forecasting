

# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from py01_helper_fucntions import get_abares_crop_data

# %%

# Load the South AUstralia worksheet in the ABARES sorkbook.

sa_crops = get_abares_crop_data('South Australia')
sa_crops['year'] = sa_crops['year'].astype(int)

sa_crops = sa_crops[sa_crops['Crop'].isin(['Wheat', 'Barley', 'Triticale'])]

# %%

#Production Pivot
production = sa_crops[sa_crops['Key'] == 'Production']\
    .pivot(index = 'year',
           columns = 'Crop')['value']

production = production\
    .sort_values(production\
        .last_valid_index(), axis = 1, ascending = False)


#Hectares Pivot
hectares = sa_crops[sa_crops['Key'] == 'Area']\
    .pivot(index = 'year',
           columns = 'Crop')['value']

hectares = hectares\
    .sort_values(production\
        .last_valid_index(), axis = 1, ascending = False)


crop_yield = (production / hectares).replace(np.nan, 0)\
    .sort_values(production\
        .last_valid_index(), axis = 1, ascending = False)


# %%

sa_ceareals_prod = sa_crops[sa_crops['Key'].isin(['Production'])].groupby('year').sum()

sa_ceareals_ha = sa_crops[sa_crops['Key'].isin(['Area'])].groupby('year').sum()

# %%

sa_yield =  pd.concat([sa_ceareals_prod,
                       sa_ceareals_ha],
                       axis = 1)
                      
sa_yield.columns = ['production', 'hectares']

sa_yield['Yield'] = sa_yield['production'] / sa_yield['hectares']

sa_yield.to_csv('sa_yield.csv')


#%% PLOTTING

####################################
#              PLOT DATA           #
####################################

cmap = plt.cm.get_cmap('Paired', 10)

fig, (ax1, ax2) = plt.subplots(1, 2, 
                              figsize = (18,5),  
                              constrained_layout = True)


production.plot.bar(use_index = True, 
                    ax = ax1,
                    stacked = True,
                    cmap = cmap)           


# Set up formatting for graph 

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('Production (000 tonnes)', fontsize = 15)

ax1.legend(fontsize = 18,
           bbox_to_anchor = (1, 1.025), 
           loc = 'upper left')

ax1.tick_params(axis = 'both',
                which = 'major', 
                labelsize = 18)

ax1.grid(False)
ax1.set_title("South Australia Annual Production by Crop Type, \n 1989 - 2020", fontsize = 20)

for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
	label.set_fontsize(12)

### AREA ###

hectares.plot.bar(use_index = True, 
                  ax = ax2,
                  stacked = True,
                  cmap = cmap)           


# Set up formatting for graph 

ax2.set_xlabel('Year', fontsize=15)
ax2.set_ylabel('Planted Area (000 hectares)', fontsize = 15)

ax2.legend(fontsize = 18,
           bbox_to_anchor = (1, 1.025), 
           loc = 'upper left')

ax2.tick_params(axis = 'both',
                which = 'major', 
                labelsize = 18)

ax2.grid(False)
ax2.set_title("South Australia Annual Planed Area by Crop Type, \n 1989 - 2020", fontsize = 20)

for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
	label.set_fontsize(12)

plt.savefig('plot01_sa_historical_1.jpg')


#%% PLOTTING

####################################
#              PLOT DATA           #
####################################

cmap = plt.cm.get_cmap('Paired', 10)

fig, (ax) = plt.subplots(1, 1, 
                        figsize = (15, 5),  
                        constrained_layout = True)
### Yield ###

crop_yield.plot(use_index = True, 
                ax = ax,
                cmap = cmap,
                style = '.-',
                markersize = 12)           

# Set up formatting for graph 

ax.set_xlabel('Year', fontsize=18)
ax.set_ylabel('Crop Yield - Tonnes / ha', fontsize = 18)

ax.legend(fontsize = 18,
          bbox_to_anchor = (1, 1.025), 
          loc = 'upper left')

ax.tick_params(axis = 'both',
               which = 'major', 
               labelsize = 18)

ax.grid(False)
ax.set_title("South Australia Annual Average Yield by Crop Type, 1989 - 2020", fontsize = 20)

plt.savefig('plot02_sa_historical_2.jpg')



# %%
