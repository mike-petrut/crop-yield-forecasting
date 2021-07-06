
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
import matplotlib.pyplot as plt
import dload

from py01_helper_functions import ee_collection_pull, process_gdf

# %%

ee.Authenticate()
ee.Initialize()


# %% 

sa_cereals_class = gpd.read_file('sa-cereals/sa_cereals_class.shp')

#%% DEFINE COLLECTION 

# Landsat Spectral Indicies Collections 

l5_EVI = "LANDSAT/LT05/C01/T1_8DAY_EVI"
l5_NDVI = "LANDSAT/LT05/C01/T1_8DAY_NDVI"
l5_NDSI = "LANDSAT/LT05/C01/T1_8DAY_NDSI"
l5_NBR = "LANDSAT/LT05/C01/T1_8DAY_NBRT"

l7_EVI = "LANDSAT/LE07/C01/T1_8DAY_EVI"
l7_NDVI = "LANDSAT/LE07/C01/T1_8DAY_NDVI"
l7_NDSI = "LANDSAT/LE07/C01/T1_8DAY_NDSI"
l7_NBR = "LANDSAT/LE07/C01/T1_8DAY_NBRT"


# Initial date of interest (inclusive).
l5_start_date = '1989-01-01'
# Final date of interest (exclusive).
l5_end_date = '1999-12-31'

# Initial date of interest (inclusive).
l7_start_date = '2020-01-01'
# Final date of interest (exclusive).
l7_end_date = '2021-06-30'


#%%

####################################
#         EVI COLLECTIONS          #
####################################

try:
    sa_all_polygons_evi =  pd.read_csv('sa_all_polygons_evi.csv')

except: 

    l5_evi_collection = ee.ImageCollection(l5_EVI)\
    .filterDate(l5_start_date, l5_end_date)\
        .maskClouds()\
            .preprocess()

    l7_evi_collection = ee.ImageCollection(l7_EVI)\
        .filterDate(l7_start_date, l7_end_date)\
            .maskClouds()\
                .preprocess()

    landsat_5_evi = process_gdf(geopandas_frame = sa_cereals_class, 
                                collection = l5_evi_collection,
                                index = 'EVI')

    landsat_7_evi = process_gdf(geopandas_frame = sa_cereals_class, 
                                collection = l7_evi_collection,
                                index = 'EVI')

    sa_all_polygons_evi = pd.concat([landsat_5_evi, landsat_7_evi])

    sa_all_polygons_evi.to_csv('sa_all_polygons_evi.csv')

    sa_all_polygons_evi =  pd.read_csv('sa_all_polygons_evi.csv')

# %%

####################################
#         NDVI COLLECTIONS         #
####################################

try:

    sa_all_polygons_ndvi =  pd.read_csv('sa_all_polygons_ndvi.csv')
    
except: 

    l5_ndvi_collection = ee.ImageCollection(l5_NDVI)\
        .filterDate(l5_start_date, l5_end_date)\
            .maskClouds()\
                .preprocess()

    l7_ndvi_collection = ee.ImageCollection(l7_NDVI)\
        .filterDate(l7_start_date, l7_end_date)\
            .maskClouds()\
                .preprocess()

    landsat_5_ndvi = process_gdf(geopandas_frame = sa_cereals_class, 
                                 collection = l5_ndvi_collection,
                                 index = 'NDVI')

    landsat_7_ndvi = process_gdf(geopandas_frame = sa_cereals_class, 
                                 collection = l7_ndvi_collection,
                                 index = 'NDVI')

    sa_all_polygons_ndvi = pd.concat([landsat_5_ndvi, landsat_7_ndvi])

    sa_all_polygons_ndvi.to_csv('sa_all_polygons_ndvi.csv')

    sa_all_polygons_ndvi =  pd.read_csv('sa_all_polygons_ndvi.csv')

# %%

####################################
#          NDSI COLLECTIONS        #
####################################

try:
    sa_all_polygons_ndsi =  pd.read_csv('sa_all_polygons_ndsi.csv')

except: 

    l5_ndsi_collection = ee.ImageCollection(l5_NDSI)\
        .filterDate(l5_start_date, l5_end_date)\
            .maskClouds()\
                .preprocess()

    l7_ndsi_collection = ee.ImageCollection(l7_NDSI)\
        .filterDate(l7_start_date, l7_end_date)\
            .maskClouds()\
                .preprocess()

    landsat_5_ndsi = process_gdf(geopandas_frame = sa_cereals_class, 
                                 collection = l5_ndsi_collection,
                                 index = 'NDSI')

    landsat_7_ndsi = process_gdf(geopandas_frame = sa_cereals_class, 
                                 collection = l7_ndsi_collection,
                                 index = 'NDSI')

    sa_all_polygons_ndsi = pd.concat([landsat_5_ndsi, landsat_7_ndsi])

    sa_all_polygons_ndsi.to_csv('sa_all_polygons_ndsi.csv')

    sa_all_polygons_ndsi =  pd.read_csv('sa_all_polygons_ndsi.csv')

# %%

####################################
#         NBR COLLECTIONS          #
####################################

try:
    sa_all_polygons_nbr =  pd.read_csv('sa_all_polygons_nbrt.csv')

except: 

    l5_nbr_collection = ee.ImageCollection(l5_NBR)\
    .filterDate(l5_start_date, l5_end_date)\
        .maskClouds()\
            .preprocess()

    l7_nbr_collection = ee.ImageCollection(l7_NBR)\
        .filterDate(l7_start_date, l7_end_date)\
            .maskClouds()\
                .preprocess()

    landsat_5_nbr = process_gdf(geopandas_frame = sa_cereals_class, 
                                collection = l5_nbr_collection,
                                index = 'NBRT')

    landsat_7_nbr = process_gdf(geopandas_frame = sa_cereals_class, 
                                collection = l7_nbr_collection,
                                index = 'NBRT')

    sa_all_polygons_nbr = pd.concat([landsat_5_nbr, landsat_7_nbr])

    sa_all_polygons_nbr.to_csv('sa_all_polygons_nbrt.csv')

    sa_all_polygons_nbr =  pd.read_csv('sa_all_polygons_nbrt.csv')


# %%
