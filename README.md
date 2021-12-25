# 🚀 Perform Time-Series Analysis of soil moisture from SMAP L3 Product 

> Product in use: SMAP L3 Radiometer Global Daily 36 km EASE-Grid Soil Moisture, Version 7

## ⚓ Description
We perform time-series analysis of soil moisture for Bengaluru city. 

The bounds assumed for this analysis is `N_lat =  13.07 ,S_lat =  12.82 , W_lon =  77.1 , E_lon =   77.9`. We then take average of the pixels which intersect the bounds to calculate the soil moisture.

The three main process we perform are:

- Download the SMAP L3 data for the latest one month ( August 2021 here).
- Extraction of the soil moisture values from SMAP L3 data over Lat, Lon of Bangalore in python.
- Plot the time series plot for the extracted soil moisture values for the latest one month. 



## 🛠️ Usage
To see it in action run the [colab notebook](https://github.com/amanbagrecha/smap_time_series_analysis/blob/main/colab_wrapper.ipynb) and follow the instructions there

## Files Explanation
In this section we look at the different files inside the repository as well as an explanation about their functionality


|File Name| Explanation / Function |
|---------|------------|
|[`colab_wrapper.ipynb`](https://github.com/amanbagrecha/smap_time_series_analysis/blob/main/colab_wrapper.ipynb)<img width=90/>| Colab wrapper to download, run and visualise the time series python scripts|
|[`main.py`](https://github.com/amanbagrecha/smap_time_series_analysis/blob/main/main.py) | contains the class and function to extract info from the downloaded files  |
|[`download_SPL3.py`](https://github.com/amanbagrecha/smap_time_series_analysis/blob/main/download_SPL3.py)|script by NASA to download data. can be modified to change the date of download for SMAP L3 |
|`EASE2_M36km.lats.964x406x1.double` | EASE grid latidues to intersection with bounds|
|`EASE2_M36km.lons.964x406x1.double`| EASE grid longitudes to intersection with bounds|



## 🚩 Output

![](https://i.imgur.com/PngGsda.png)


## 🏁 Requirements
- Python with Jupyter/ colab

> Data courtesy: O'Neill, P. E., S. Chan, E. G. Njoku, T. Jackson, R. Bindlish, and J. Chaubell. 2020. SMAP L3 Radiometer Global Daily 36 km EASE-Grid Soil Moisture, Version 7. [Indicate subset used]. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center. doi: https://doi.org/10.5067/HH4SZ2PXSP6A. [31st August, 2021].


