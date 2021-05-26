
import os
import glob
import rioxarray as rxr
import xarray as xr
import numpy as np
from index_functions import evi2, ndvi, ndmi

 
def landsat_comp(path):
 
    tif_list = glob(os.path.join('landsat_imagery', path, "*_B*"))[0:6]
 
    out_xr = []
    for i, tif_path in enumerate(tif_list):
        out_xr.append(rxr.open_rasterio(tif_path, masked = True).squeeze())
        out_xr[i]["band"] = i + 1
 
    return xr.concat(out_xr, dim = "band")

def process_landsat(image, boundary, model):
 
    #project LGA bound polygon to input image
    bound_crs = boundary.to_crs(image.rio.crs)
    #clip the input image to the LGA boundary geometry
    image_clip_crop = image.rio.clip(bound_crs.geometry)
    
    if model == "EVI2":
        index = evi2(image_clip_crop)
    elif model == "NDVI":
        index = ndvi(image_clip_crop)
    elif model == "NDMI":
        index = ndmi(image_clip_crop)
    else : image_clip_crop
 
    #assign no data values for interpolation
    index.rio.write_nodata(np.nan, inplace = True)
    #interpolate the cropped out cells using a linear interpolation algorithem 
    int = index.rio.interpolate_na(method = 'nearest')
    #interpolating creates TIN overlap, crop back to lga bounds
    processed = int.rio.clip(bound_crs.geometry)
    
    return processed