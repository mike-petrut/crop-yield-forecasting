#%%

import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import matplotlib.pyplot as plt

from py01_helper_functions import ee_collection_pull, monthly_rain, process_gdf, process_index_table, process_index_table2

# %%

sa_cereals_class = gpd.read_file('sa-cereals/sa_cereals_class.shp')

# %%

####################################
#            FOLIUM MAPS           #
####################################

# Get the center of the map
xy = np.asarray(sa_cereals_class.head(1).centroid[0].xy).squeeze()
center = list(xy[::-1])

# Select a zoom
zoom = 10

# Create the most basic OSM folium map
m = folium.Map(location = center, 
               zoom_start = zoom, 
               control_scale = True)

# Iterate through each Polygon of paths and rows intersecting the area
for i, row in sa_cereals_class.iterrows():
    # Create the folium geometry of this Polygon 
    g = folium.GeoJson(row.geometry.__geo_interface__,
                       style_function = lambda x: {'color': '#000080', 
                                                   'alpha': 0,
                                                   'weight': 1,
                                                   'fill_opacity': 0.5})
    # Add the object to the map
    g.add_to(m)

folium.LayerControl().add_to(m)

m

# %%

####################################
#      SPECTRAL INDICIES PLOTS     #
####################################

sa_evi = process_index_table('sa_all_polygons_evi.csv')
sa_ndvi = process_index_table('sa_all_polygons_ndvi.csv')
sa_ndsi = process_index_table2('sa_all_polygons_ndsi.csv')
sa_nbr = process_index_table2('sa_all_polygons_nbrt.csv')
sa_yield = pd.read_csv('sa_yield.csv', index_col = 'year')
sa_rain = pd.read_csv('sa_crop_rain.csv', index_col = 'year')

# %%

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, 
                                             figsize = (18, 8),  
                                             constrained_layout = True)
### EVI ###

sa_evi.plot(use_index = True, 
            ax = ax1,
            color = 'green',
            style = '.-',
            markersize = 12)           

# Set up formatting for graph 

ax1.set_xlabel('Year', fontsize = 18)
ax1.set_ylabel('EVI', fontsize = 18)

ax1.legend(fontsize = 18)


ax1.tick_params(axis = 'both',
               which = 'major', 
               labelsize = 18)

ax1.grid(False)
ax1.set_title("SA Mean EVI (Aug-Oct), 1989 - 2020", fontsize = 18)


### NDSI ###

sa_ndsi.plot(use_index = True, 
             ax = ax2,
             color = 'blue',
             style = '.-',
             markersize = 12)           

# Set up formatting for graph 

ax2.set_xlabel('Year', fontsize = 18)
ax2.set_ylabel('NDSI', fontsize = 18)

ax2.legend(fontsize = 18)


ax2.tick_params(axis = 'both',
                which = 'major', 
                labelsize = 18)

ax2.grid(False)
ax2.set_title("SA Mean NSDI (May-Oct), 1989 - 2020", fontsize = 18)


### NDBR ###

sa_ndsi.plot(use_index = True, 
             ax = ax3,
             color = 'brown',
             style = '.-',
             markersize = 12)           

# Set up formatting for graph 

ax3.set_xlabel('Year', fontsize = 18)
ax3.set_ylabel('NBR', fontsize = 18)

ax3.legend(fontsize = 18)

ax3.tick_params(axis = 'both',
                which = 'major', 
                labelsize = 18)

ax3.grid(False)
ax3.set_title("SA Mean NBR (May-Oct), 1989 - 2020", fontsize = 18)

plt.savefig('plot03_all_spectral.jpg')


