# Crop Yield Forecasting with Landsat Imagery

## A general spatial approach to predicting crop yield for broadacre cropping with cloud processing of remote sensing imagery

[![DOI](https://zenodo.org/badge/366886513.svg)](https://zenodo.
org/badge/latestdoi/366886513) 

This repository for an experimental projection model which aims to project broadacre harvest crop yield based on limited reference data and without ground-truth sampling.

## Background 


## Project Goals


## Tools and Packages Used

#### General science packages
- pandas
- numpy
- datetime
- re
- jupyter
- dload

#### Statistics 
- scipy
- statsmodels.api
- sklearn

#### Geospatial packages
- geopandas
- rasterio
- rioxarray
- xarray
- shapely

#### Visualisation
- matplotlib
- folium
- seaborn

### Google Earth Engine Packages 
- ee
- eemont

The project includes a function file which includes custom functions which are imported into the working calculation sheets

## Data Used

- Landsat 5 imagery sourced through the Google Earth Engine 
- Landsat 7 imagery sourced through the Google Earth Engine  
- Longpaddock SILO weather data (gridded raster weather data to 1ha squared resolution - [Link](https://www.longpaddock.qld.gov.au/silo/gridded-data/)
- ABARES (Australian Bureau of Agricultural and Resource Economics and Sciences) Classification and Land Use Raster (2018) - [Link](https://www.agriculture.gov.au/abares/aclump/land-use/data-download)
- ABARES Australian Crop Report - [Link](https://www.agriculture.gov.au/abares/research-topics/agricultural-outlook/australian-crop-report)

## Description of Files in this Repository

1. py01_helper_functions.py (Functions)
     * This file sets out all the functions required to run the model. 

2. py02_model_data_setup.py (Functions)
     * This file sets up the non-cloud data needed for the model such as feature engineering of the ABARES crop report and import and formatting of the land classification geodataframe 

3. py03_get_silo.py (Functions)
     * This file pulls the weather data from the SILO AWS server. The weather data is not sued in the primary analysis but had been included for future random forest model testing. 

4. py04_earth_engine.py (Functions)
     * This file

5. py05_regression_modelling.py (Functions)
     * This file

6. py06_random_forrest.py (Functions)
     * *File is a test model* This file tests a workflow for formatting the data into a random forest panel table and runs a simple scikit regression model across all the features

7. py07_mapping.py (Functions)
     * This file is used for mapping data and printing images from the analysis

## Activate environment and install requirements

To set up the environment for this model, with Git and Miniconda/Anaconda installed, run the following in the command terminal (this model is tested using Bash)

```bash

git clone https://github.com/mike-petrut/crop-yield-forecaasting
cd crop-yield-forecasting
conda env create --file environment.yml
conda activate crop-yield-forecasting

```

Then install the required packages into the environment using

```bash 

pip install -r requirements.txt

```

## Running the Workflow

Once the model is set up, the python files can be run in order using the following code in Bash

```bash

for f in *.py; do python "$f"; done

```

The model will ask for an authentication key and open your default browser, prompting you to log onto your Gmail account which has an associated Google Earth Engine key. The authentication code provided in Google can then be copy-paste into Bash and the model will continue to run. 

## Example Usage

An example of how to run this model will be to define a link to the geodataframe that you would like to be the area of interest. The file used in this document is all the croplands for South Australia, but this can be reproduced using another region of Australia. Note that the actual data for yield used is for South Australia, this can be changed to other states or territories by changing the test on line 15 of 'py02_model_data_setup'. If the user wants to test a geography outside Australia they will need to add their data source of historical values into the model in this same notebook. 

Land use data for other states and territories are [available from this link](https://www.agriculture.gov.au/abares/aclump/land-use/data-download). To run the model as is, set up for South Australia, simply run the py00_run_full_model.py file in the repository. ​

## Future Developments

[![DOI](https://zenodo.org/badge/366886513.svg)](https://zenodo.org/badge/latetdoi/366886513)