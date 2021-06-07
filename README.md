# Dryland Cropping Performance Forecasting 

[![DOI](https://zenodo.org/badge/366886513.svg)](https://zenodo.org/badge/latestdoi/366886513)

Dryland cropping performance prediction based on temporal analysis of Landsat 8 imagery. 

This is a repository for an experimental projection model which aims to project broadacre harvest crop performance based on limited reference data and without ground-truth sampling.

## Background 

Projecting the performance of dryland broadacre cropping in Australia has long been a challenge for earth observation professions in Australia including the Commonwealth Scientific and Industrial Research Organisation (CSIRO). Research to date in this field has focused on drawing predictive results using machine learning techniques across smaller localised samples of data, modelling results against ground truth sample points at the farm and paddock level. With growing concern about the impacts of climate change on the overall Australian agriculture industry, I see the opportunity for a broader approach to crop performance modelling, using gridded weather indicators and vegetation index modelling from Landsat 8 imagery to estimate indicators of crop performance across larger regions were ground truth control samples are not available at scale. 

## Project Goals

This project aims to provide a scalable and reproducible model for predicting yield across cereals and canola in Australia. The project will utilise temporal satellite and weather data to model the relationship between climate and different vegetation and moisture indices such as NDMI, EVI, and NDVI.

The project will aim to do the following

- Automate the download, mosaicking and spectral processing of Landsat 7 & 8
- Crop the imagery to the relevant grain growing regions, mask to dryland cropping land use areas, and interpolate and resample the cells to the same specifications as the gridded weather data (1ha squared)
- Perform regression modelling between weather indicators and vegetation indices both spatially across the gridded imagery and across the time-series. 
- Aggregate results up to the agricultural region and model relationship between vegetation indices and crop performance over time. Crop performance is typically measured by tonnes/hectare and total regional yield. 

## Tools and Packages Used

- geopandas
- matplotlib
- earthpy
- rasterio
- rioxarray
- dvc

The project includes fucntions files which can be imported into the processing notebooks

Project may need to use some geo-databasing or API tools for handling large temporal satellite datasets.

## Data Used

- Landsat 8 imagery sourced through the AWS and Google portals 
- Longpaddock SILO weather data (gridded raster weather data to 1ha squared resolution (https://www.longpaddock.qld.gov.au/silo/gridded-data/)
- ABARES (Australian Bureau of Agricultural and Resource Economics and Sciences) Classification and Land Use Raster (2018) (https://www.agriculture.gov.au/abares/aclump/land-use/data-download)

## Description of Files in this Repository

1. get_silo.py (Functions)
     * This python file sets out the nessesery fucntions for the climate analyis part of the modelling. The fucntion uses the AWS server that hosts all SILO weather data to download all monthly geotiff files within a certain range of months. At this stage only the monthly_rain has been added which aggrigates cumulative rain over the year by summing the rioxarray files that are preclipped to the AOI by the fucntion.

2. index_fucntions.py (Functions)
     * This python file includes fucntions for running different spectral models on landsat 7 and 8 imagery, because I want to look back pre-2013 the fucntions define the bands based on whether the image is Landsat 7 or 8. The main models I intend to use are EVI2, AVI, NDWI and NDVI. 

3. landsat_processing.py (Functions)
     * This functions file includes the necessary fucntions for 

4. silo-data-run-test.ipynb (Processing Notebook)
     * This short notebook demonstrates the fucntionality of get_silo.py for pulling monthly weather data and accumulating it for the time-series range. 

5. silo-data-run-test.html (Output)
     * Exported html of the above name-related jupyter notebook

** More processing files to be uploaded earth June-2021 once compete and tested.

## Activate environment and install requirements

1. In terminal, cd to the dryland-crop performance-modelling-project file
2. Activate the environment
3. Pip install from the requirements.txt file

$ cd dryland-crop performance-modelling-project file
$ conda activate cropping-env
$ pip3 install -r requirments.txt

## Running the Workflow

To run the model, start by running all function files then move onto running the processing files. Output files such as plots and tables will be saved down automatically as PDF or HTML. Note: this is not a final workflow, I intend to have the workflow automated with a dvc pipeline. 

1. Functions
     * get_silo.py
     * index_functions.py
     * landsat_processing.py

2. Processing
     * silo-data-run-test.ipynb
     * donwload_landsat.py
     * landsat_processing.py


3. Outputs
    * ** More to come - work in progress

## Example Usage

An example of how the model can be run will be to select a region for analysis then run the model dvc pipeline to get the output. Because the model will source and download all temporal satelite imagery within the specified region, it will take a long-time to run and may require some cloud solution. As part of the dcv pipeline i intend to include a parameters file which includes a start and tend date for the temporal analysis then a option for the region. This will enable reproducability and scaleability of the model. 

## Future Developments

- Develop a web app with flask or dash that allows user to select a region to analyse

[![DOI](https://zenodo.org/badge/366886513.svg)](https://zenodo.org/badge/latestdoi/366886513)
