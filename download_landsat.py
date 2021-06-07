
# %%

import os
import re
from datetime import datetime
from glob import glob
import rioxarray as rxr
import xarray as xr
import numpy as np
from index_functions import evi2, ndvi, ndmi, avi
from urllib import urllib 

# %%

def landsat_blocks(vector_polygons): 

    """ Filter WRS2 database with specified vector shapefiles. 
    
    Parameters
    ----------
    vector polygons:
        geodataframe of polygons or multipolygons
    
    Returns
    ----------
    geodataframe of WRS landsat frames that intersect with
    the input vectors

    """
 
    poly = vector_polygons
    wrs = gpd.read_file('wrs2/wrs2.shp').to_crs(poly.crs)
    landsat_list = []
    
    for geom in poly.iterrows():
        poly_isect = wrs[wrs.intersects(geom.geometry)]
        poly_isect['zone'] = geom['name']
        landsat_list.append(poly_isect)
        
    landsat_all = pd.concat(landsat_list)
    landsat_df = landsat_all[['zone', 'PATH', 'ROW', 'geometry']].rename(columns = {"ROW": "row", "PATH": "path"}).reset_index()
        
    return(landsat_df)
 
 
 
def filter_scenes_aws(scenes, blocks, cloud_cover): 

    """ Filter the AWS pandas frame to the landsat WRS blocks
    which cover the AOI. 
    
    Parameters
    ----------
    scenes, blocks, cloud cover:
        pandas frame, geodataframe, integer
    
    Returns
    ----------
    Filtered pandas frame of available landsat packages from AWS 
    that cover the AOI and is within the specific cloud cover

    """
    
    filter = scenes[(scenes['row'].isin(blocks['row'])) & (scenes['path'].isin(blocks['path']))]
    cloud_filter = filter[filter['cloudCover'] < cloud_cover]
 
    date_ls = []
 
    for index, row in cloud_filter.iterrows():
        path = row['acquisitionDate']
        match = re.search(r'\d{4}.\d{2}.\d{2}', path)
        date = datetime.strptime(match.group(), '%Y-%m-%d')
        date_ls.append(date)
 
    cloud_filter['date'] = np.array(date_ls)
    cloud_filter['month'] = cloud_filter.date.dt.to_period("M")
 
    final = cloud_filter.loc[cloud_filter.groupby(['month', 'path', 'row'])['cloudCover'].idxmin()]
 
    final['row'] = '0' + final['row'].astype(str)
    final['path'] = np.where(final['path'] < 100, '0' + final['path'].astype(str), final['path'].astype(str))
 
    return final
 
 
def download_list(aws_list, band):

    """ Transform the pandas dataframe of AWS available images 
    to downloadable urls. 
    
    Parameters
    ----------
    AWS_list, band

    pandas frame, integer or 'QA'  
    
    Returns
    ----------
    List of requestable urls which download landsat bands from AWS 

    """
 
    download_list = []
 
    for scene in aws_list.iterrows():
        
        aws_base = 'https://landsat-pds.s3.amazonaws.com/'
        L8 = 'c1/L8/'
        path = str(scene['path']) + '/'
        row = str(scene['row']) + '/'
        product = str(scene['productId'])
        band =  str(band) 
 
        download = aws_base + L8 + path + row + product + '/' + product + "_B" + band + '.TIF'
 
        download_list.append(download)
            
    return download_list
 
 
def download_list_zone(zone_polygon, scenes_list): 

    """ Generate a list of landsat bands that covers
    / intersects the polygons in the input geodataframe. 
    
    Parameters
    ----------
    vector polygons, scenes list:
        geodataframe of polygons or multipolygons, AWS list of landsat products
    
    Returns
    ----------
    List of bands ready to be downloaded from the AWS server

    """
 
    bands =  [1, 2, 3, 4, 5, 6, 'QA']
 
    zone_shape = zone_polygon
    l_block = landsat_blocks(zone_shape)
    scenes = filter_scenes_aws(scenes_list, l_block, 100)
 
    band_list = []
 
    for b in bands:
        
        dl_list = download_list(scenes, b)
    
        band_list.append(dl_list)
 
    list_flat =  [y for x in band_list for y in x]
  
    return(list_flat)
 
 
def landsat_download(bands_list, dir_name):

    """ Download the landsat bands created with the 
    download_list_zone function to a specified file. 
    
    Parameters
    ----------
    bands_list, dir_name : list, string
        list of landsat bands, list of file names.
    
    Returns
    ----------
    Does not retrun an item, prints the name being downloaded and stores to disk

    """

    landsat_dir = 'landsat_imagery'
    try:
        os.makedirs(landsat_dir + '/' + dir_name)    
        print("Directory " , dir_name ,  " Created ")
    except FileExistsError:
        print("Directory " , dir_name ,  " already exists")  
 
    for band in bands_list:

        print('downloading' + ' ' + band)
        url = band
        urllib.request.urlretrieve(url, filename = os.path.join(landsat_dir + '/' + dir_name, band[51:91] + band[132:135]))
