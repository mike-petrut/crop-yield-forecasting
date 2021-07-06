#%%

import pandas as pd
import numpy as np
import geopandas as gpd
import folium

from py01_helper_fucntions import ee_collection_pull, monthly_rain, process_gdf, process_index_table, process_index_table2

# %%

try:
    sa_cereals_class = gpd.read_file('sa-cereals/sa_cereals_class.shp')
except:    
    sa_land_class = gpd.read_file('sa-shape/sa-shape.shp')

    sa_cereals_class = sa_land_class[\
        (sa_land_class['LU_CODE'] == '3.3.1') & \
            (sa_land_class['LUC_DATE'].str.contains('2016'))]\
                .explode()\
                .reset_index()

    sa_cereals_class.to_file('sa_cereals/sa_cereals_class.shp')

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

sa_evi.plot()

# %%

import matplotlib.pyplot as plt

cmap = plt.cm.get_cmap('Paired', 10)

fig, ax = plt.subplots(2, 2, 
                       figsize = (5, 5),  
                       constrained_layout = True)


ax = sa_evi.plot()

# %%
