# %% Define function for spatially modelling monethly rain

import pandas as pd 
import rioxarray as rxr

def monthly_rain(year, from_month, x_months, proj, bound):
 
    #project boundary to working crs
    bound_crs = bound.to_crs(proj.rio.crs)
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
        month_rain = rxr.open_rasterio(call, masked = True).squeeze().rio.reproject(proj.rio.crs)
        rain_stack.append(month_rain)      
 
    stacked_rain = sum(rain_stack).rio.clip(bound_crs.geometry)
 
    return stacked_rain


