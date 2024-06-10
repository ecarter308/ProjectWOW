# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 11:07:10 2023

@author: ec308
"""

import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4 as nc

#get sst dataset
sst_dataset = xr.open_dataset("https://thredds.jpl.nasa.gov/thredds/dodsC/ncml_aggregation/OceanTemperature/modis/aqua/11um/4km/aggregate__MODIS_AQUA_L3_SST_THERMAL_DAILY_4KM_DAYTIME_V2019.0.ncml")
chla_dataset = xr.open_dataset("https://coastwatch.noaa.gov/erddap/griddap/noaacwNPPVIIRSSQchlaDaily")

#extract only sst column
sst = sst_dataset['sst']
chlor_a = chla_dataset['chlor_a']
 
#format 'time' as datetime
sst['time'] =  pd.to_datetime(sst['time'],format='%Y-%m-%d')
chlor_a['time'] =  pd.to_datetime(chlor_a['time'],format='%Y-%m-%d')

#create a list of years
year = [2017, 2018, 2019, 2020, 2021] 
#create a list of months in a year
wint_months = [12,1,2]
spr_months = [3,4,5]
sum_months = [6,7,8]
fall_months = [9,10,11]

#create a dictionary of seasons
month_dict = {'wint_months': wint_months, 'spr_months': spr_months, 
              'sum_months': sum_months, 'fall_months': fall_months}

#subset data to each season and area and export     
for key in month_dict:

    month_sub_sst = sst[sst['time'].dt.year.isin(year) & sst['time'].dt.month.isin(month_dict[key])].sel(lon=slice(-80,-65), lat=slice(45,25))
    month_sub_sst.to_netcdf("Z:/Members/Maps/ec308_sites_project_WOW/Data/MODIS/sst_{}.nc".format(key))
    
    month_sub_chlor = chlor_a[chlor_a['time'].dt.year.isin(year) & chlor_a['time'].dt.month.isin(month_dict[key])].sel(longitude=slice(-80,-65), latitude=slice(45,25))
    month_sub_chlor.to_netcdf("Z:/Members/Maps/ec308_sites_project_WOW/Data/MODIS/chlor_a_{}.nc".format(key))
