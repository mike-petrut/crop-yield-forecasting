
#%%

import re
import datetime
import geopandas as gpd
import requests
import pandas as pd
import numpy as np
import rioxarray as rxr
import ee


####################################
# ABARES AND LAND COVER FUNCTIONS  #
####################################

def get_abares_crop_data(state): 

    try:
        abares_path = 'abares.xlsx'
    except:
        abares = 'https://daff.ent.sirsidynix.net.au/client/en_AU/search/asset/1032161/3'
        abares_r = requests.get(abares, allow_redirects=True)
        abares_path = 'abares.xlsx'

    crop_col = ['Wheat', 'Wheat', 
                'Barley', 'Barley',
                'Canola', 'Canola',
                'Chickpeas', 'Chickpeas', 
                'Faba beans', 'Faba beans',
                'Field peas', 'Field peas', 
                'Lentils', 'Lentils',
                'Lupins', 'Lupins', 
                'Oats', 'Oats', 
                'Triticale', 'Triticale']

    wb = pd.read_excel(abares_path, 
                       sheet_name = state,
                       header = 6,
                       usecols = "C:AJ",
                       nrows = 31)\
                           .dropna()\
                           .rename(columns = {'Crops': 'Key', 'Unnamed: 3': 'Unit'})

    wb['Crop'] = crop_col

    panel = wb.melt(id_vars = ['Crop', 'Key', 'Unit']).rename(columns = {'variable': 'year'})
    panel['year'] = panel['year'].astype(str).str[0:4]

    return panel


# %%

####################################
#          GOOGLE FUCNTIONS        #
####################################


def process_gdf(geopandas_frame, collection, index):

    """

    This function takes and processes a geodataframe and passes
    it through the ee_collection_pull function to output a finished 
    spectral indices pandas data frame. 

    Parameters
    ----------
    input : 
           geodataframe - geopandas frame of polygons or mutipolygons
           (the functions explodes the multipolygons in in the frame)

           collection - Google Earth Engine collection item (for ee_collection_pull)

           index - spectral indices as string (e.g 'EVI') (for ee_collection_pull)

           collection -  
    
    Returns
    ------
    output : pandas data frame
        a pandas data frame with a date index and values column of the selected 
        spectral index

    """

    index = str(index)
    index_band = [index]

    features = []
    pd_ls = []

    for index, gpd_row in geopandas_frame.iterrows():

        geom = gpd_row.geometry 
        x, y = geom.exterior.coords.xy
        coords = np.dstack((x,y)).tolist()

        ee_geom = ee.Geometry.Polygon(coords)          
        feature = ee.Feature(ee_geom)

        features.append(feature)
        
    ee_poly = ee.FeatureCollection(features)    

    print('Extracting data from selected imagery')

    ee_request = collection.getTimeSeriesByRegion(reducer = ee.Reducer.mean(),
                                                  geometry = ee_poly,
                                                  bestEffort = True,
                                                  bands = index_band,
                                                  scale = 125,
                                                  maxPixels = 1e20)


    processed = ee_collection_pull(ee_request, index)
    pd_ls.append(processed)
    full_table = pd.concat(pd_ls)
                                                             
    return full_table


def ee_collection_pull(ee_collection, index):

    """

    This function takes the GEE collection request that has been defined and
    formats it into a time series pandas dataframe

    Parameters
    ----------
    input : 
           ee_collection - Google Earth Engine collection item 
           index - spectral indices as string (e.g 'EVI')        
    
    Returns
    ------
    output : pandas data frame
        a pandas data frame with a date index and values column of the selected 
        spectral index

    """

    index = str(index)

    df = pd.DataFrame(pd.DataFrame\
        .from_dict(ee_collection.getInfo()['features'])['properties']\
        .to_list())

    date_list = []

    for index, row in df.iterrows():
        date_col = row['date']
        match = re.search(r'\d{4}.\d{2}.\d{2}', date_col)
        date_fill = datetime.datetime.strptime(match.group(), '%Y-%m-%d')
        date_list.append(date_fill)

    df['date'] = date_list
    df['month'] = df.date.dt.to_period('M')

    df_fin = df[df[df.columns[0]] != -9999]

    collection_pull = df_fin.groupby(by = df_fin['month']).mean()

    return collection_pull



# %%

####################################
#  SILO (CLIMATE) DATA FUNCTIONS   #
####################################

def monthly_rain(year, from_month, x_months, bound):

    """

    This function downloaded the data embedded tif files from the SILO Longpaddock Dataset 
    and creates a cumulative annual total by stacking the xarrays. This function is embedded 
    in the get_rainfall function or can be used separately

    Parameters
    ----------
    input : 
            year (integer) value of the year for the data to be pulled
            month (integer) value of the first month for the data to be pulled
            x_months (integer) number of months to be pulled
            bound (shapefile) area of interest for the final calculated tif to be clipped to
    
    Returns
    ------
    output : rioxarray item representing each of the months pulled and 
    summed up for the months selected 

    """
 
    #create month string as pandas frame 
    mon_string = pd.DataFrame({'mon': ['01', '02', '03', '04', '05', '06',
                                       '07', '08', '09', '10', '11', '12']})
    #assign year column
    mon_string['year'] = str(year)
    #assign yearmon column
    mon_string['yearmon'] = mon_string['year'] + mon_string['mon']
    #filter to first x months
    mon_select = mon_string[from_month-1:x_months]
    #set base url
    base = 'https://s3-ap-southeast-2.amazonaws.com/silo-open-data/monthly/monthly_rain'
 
    rain_stack = []
    
    #loop to download tifs, reporoject, stack, sum and clip
    for index, i in mon_select.iterrows():
 
        call = base + '/' + i['year'] + '/' + i['yearmon'] + '.monthly_rain.tif'
        month_rain = rxr.open_rasterio(call, masked = True).squeeze()
        rain_stack.append(month_rain)  

    bound_crs =  bound.to_crs(rain_stack[1].rio.crs)        
    stacked_rain = sum(rain_stack).rio.clip(bound_crs.geometry)

    return stacked_rain


# %%


def pull_rainfall(shapefile, start_year, end_year):

    """

    This function repeats the monthly_rain function across multiple years and converts
    the stacked xarray item into a pandas dataframe

    Parameters
    ----------
    input : 
            shapefile (shapefile) area of interest for the final calculated tif to be clipped to  
            start_year (integer) value of the year for the data to be pulled
            end_year (integer) value of the first month for the data to be pulled
    
    Returns
    ------
    output : rioxarray item representing each of the months pulled and 
    summed up for the months selected 

    """

    years = list(range(start_year, end_year + 1))

    rain_list = []
    mean_values = []

    for year in years:

        print('processing data for year ' + str(year))

        rain_pull = monthly_rain(year, 
                                 from_month = 5, 
                                 x_months = 9,
                                 bound = shapefile)

        rain_list.append(rain_pull)

    for rain_xr in rain_list:

        rain_array = rain_xr.valuess
        mean_val = np.nanmean(rain_array)

        mean_values.append(mean_val)

    # MACV = Mean (of Land Cover) Annual Cumulative Rainfall (May - Sep)

    rainfall_table =  pd.DataFrame({'year': years, 'MACV Rainfall': mean_values})
    
    return rainfall_table


# %% 

####################################
#       REGRESSION MODELLING       #
####################################


def process_index_table(vi_link):

    vi_tbl = pd.read_csv(vi_link)

    vi_tbl['year'] = vi_tbl.month.astype(str).str[0:4]
    vi_tbl['month'] = vi_tbl.month.astype(str).str[5:7]

    vi_preharv = vi_tbl[vi_tbl['month'].isin(['08','09', '10'])]

    vi_final = vi_preharv.groupby('year').mean()

    vi_final.index = vi_final.index.astype(int)

    return vi_final


def process_index_table2(vi_link):

    vi_tbl = pd.read_csv(vi_link)

    vi_tbl['year'] = vi_tbl.month.astype(str).str[0:4]
    vi_tbl['month'] = vi_tbl.month.astype(str).str[5:7]

    vi_preharv = vi_tbl[vi_tbl['month'].isin(['05', '06', '07', '08', '09', '10'])]

    vi_final = vi_preharv.groupby('year').mean()

    vi_final.index = vi_final.index.astype(int)

    return vi_final

def process_index_table3(vi_link):

    vi_tbl = pd.read_csv(vi_link)

    vi_tbl['year'] = vi_tbl.month.astype(str).str[0:4]
    vi_tbl['month'] = vi_tbl.month.astype(str).str[5:7]

    vi_preharv = vi_tbl[vi_tbl['month'].isin(['03','04', '05'])]

    vi_final = vi_preharv.groupby('year').mean()

    vi_final.index = vi_final.index.astype(int)

    return vi_final


def process_index_pivot(vi_link, v_index):

    v_index = str(v_index)

    vi_tbl = pd.read_csv(vi_link)

    vi_tbl['year'] = vi_tbl.month.astype(str).str[0:4]
    vi_tbl['month'] = vi_tbl.month.astype(str).str[5:7]

    vi_tbl.index = vi_tbl.index.astype(int)
        
    vi_tbl = vi_tbl\
        .groupby(['year', 'month'])[v_index]\
            .aggregate('mean')\
                .unstack()\
                    .reset_index()

    vi_tbl.columns = v_index + "_" + vi_tbl.columns

    return vi_tbl




# %%
