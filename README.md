# Dryland Cropping Performance Forecasting 

Dryland cropping performance prediction based on temporal analysis of Landsat 8 imagery. 

This is a repository for an experimental projection model which aims to project broadacre harvest crop performance based on limited reference data and without ground-truth sampling.

## Background 

Projecting the performance of dryland broadacre cropping in Australia has long been a challenge for earth observation professions in Australia including the Commonwealth Scientific and Industrial Research Organisation (CSIRO). Research to date in this field has focused on drawing predictive results using machine learning techniques across smaller localised samples of data, modelling results against ground truth sample points at the farm and paddock level. With growing concern about the impacts of climate change on the overall Australian agriculture industry, I see the opportunity for a broader approach to crop performance modelling, using gridded weather indicators and vegetation index modelling from Landsat 8 imagery to estimate indicators of crop performance across larger regions were ground truth control samples are not available at scale. 

## Project Goals

This project aims to provide a scalable and reproducible model for predicting yield across cereals and canola in Australia. The project will utilise temporal satellite and weather data to model the relationship between climate and different vegetation and moisture indices such as NDMI, EVI, and NDVI.

The project will aim to do the following

- Automate the download, mosaicking and spectral processing of Landsat 8
- Crop the imagery to the relevant grain growing regions, mask to dryland cropping land use areas, and interpolate and resample the cells to the same specifications as the gridded weather data (1ha squared)
- Perform regression modelling between weather indicators and vegetation indices. 
- Aggregate results up to the agricultural region and model relationship between vegetation indices and crop performance over time


## Tools and Packages Used

- geopandas
- matplotlib
- earthpy
- rasterio
- rioxarray

**TBC**: Project may need to use some geo-databasing or API tools for handling large temporal satellite datasets.

## Data Used

- Landsat 8 imagery sourced through the AWS and Google portals 
- Longpaddock SILO weather data (gridded raster weather data to 1ha squared resolution (https://www.longpaddock.qld.gov.au/silo/gridded-data/)
- ABARES (Australian Bureau of Agricultural and Resource Economics and Sciences) Classification and Land Use Raster (2018) (https://www.agriculture.gov.au/abares/aclump/land-use/data-download)


## Description of Files in this Repository

**TBC**
- weather_processing.ipynb
- landsat_processing.ipynb 
- regression_modelling.ipynb
- outputs.ipynb

## Running the Workflow

TBC

## Example Usage

TBC

## Future Developments

- Develop a web app with flask or dash that allows user to select a region to analyse

