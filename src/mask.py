#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 01:14:45 2021

@author: albertosr
"""

import geopandas as gpd
from rasterio import features
from affine import Affine
import xarray as xr
import numpy as np
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import zipfile
from send_email import Send_email


class Raise_alert:
    
    var_name = 'COLUMN_ASH_kmax'
    shapefile = 'ne_10m_admin_0_sovereignty'
    
    def __init__(self, ds_loc, out_folder):
        
        self.ds_loc = ds_loc
        self.out_folder = out_folder

    def transform_from_latlon(self, lat, lon):
        ''' Translation of latitudes and longitudes'''
        
        lat = np.asarray(lat)
        lon = np.asarray(lon)
        trans = Affine.translation(lon[0], lat[0])
        scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
        return trans * scale
    
    
    def rasterize(self, shapes, coords, fill=np.nan, **kwargs):
        """Rasterize a list of (geometry, fill_value) tuples onto the given
        xray coordinates. This only works for 1d latitude and longitude
        arrays.
        """
        
        transform = self.transform_from_latlon(coords['lat'], coords['lon'])
        out_shape = (len(coords['lat']), len(coords['lon']))
        raster = features.rasterize(shapes, out_shape=out_shape,
                                    fill=fill, transform=transform,
                                    dtype=float, **kwargs)
        return xr.DataArray(raster, coords=coords, dims=('lat', 'lon'))
    
    
    def mask_sea(self):
        ''' To mask the sea out based on a shapefile with Norwegian geometry.
            Also to drop unnecessary variables.
            
            ds: xarray dataset produced by reading a netcdf with xaarray
            
            returns a masked xarray dataset
            '''
    
        var_list = [Raise_alert.var_name]
        unwanted_vars = [x for x in list(self.ds_loc.data_vars) if x not in var_list]
        ds2 = self.ds_loc.drop(unwanted_vars)
        
        #For copying coords for a new variable
        new = xr.Dataset(coords={'lat':(['lat'], ds2['lat'].values),
                                 'lon':(['lon'], ds2['lon'].values)})
        
        # shapefile from natural earth data
        states = gpd.read_file(Raise_alert.shapefile)
        norway = states.query("SOVEREIGNT == 'Norway'").reset_index(drop=True)
        shapes = [(shape, 1) for n, shape in enumerate(norway.geometry)]
        ds2['land'] = self.rasterize(shapes, new.coords)
        
        # Applying sea mask
        mask = ds2.where(ds2['land'] == 1, drop=True)
    
        return mask
     
    
    def mapping_regular_grid(self, lons, lats, data, title, outname):
        '''This function is to plot a map on a regular grid with lat/lon as dimensions.
        Adequate for L3 products'''        
        
        add = ' (g/m2)'
        levels = 20
        cmap= plt.cm.get_cmap("jet", levels)
        levs = np.arange(0, levels, 1)
        #prj = ccrs.Orthographic(np.nanmean(lons), np.nanmean(lats))
        prj = ccrs.PlateCarree()
        #prj = ccrs.Mercator()
        #prj = ccrs.RotatedPole(pole_longitude=8.45, pole_latitude=60.47)
        #prj = ccrs.Orthographic(8.45, 60.47)
        
        plt.close('all')
        plt.figure(figsize=(10,10), dpi=200)
    
        ax = plt.axes(projection=prj) 
        ax.set_extent([np.min(lons), np.max(lons), np.min(lats), np.max(lats)],
                       prj)
        ax.coastlines(resolution='50m')
        #ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        
        ax.contourf(lons, lats, data, levels, cmap=cmap, transform=prj)
         
        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, 
                     values = levs, label = Raise_alert.var_name+add, fraction=0.026, pad=0.04)
        #cbar.ax.get_yaxis().set_ticks(levs)
        #cbar.ax.set_ylabel(labis)
        xticks = list(np.arange(np.min(lons), np.max(lons),5))
        yticks = list(np.arange(np.min(lats), np.max(lats),5))
        ax.set_xticks(xticks, crs=prj)
        ax.set_yticks(yticks, crs=prj)
        
        out_path = os.path.join(self.out_folder, ''.join([outname, '.png']))
        plt.savefig(out_path, bbox_inches="tight")   
    
    
    def zipdir(self, name):
        '''Creation of zip file from all files in a folder
        
        folder: str, folder path
        name: str, name of the zip file to be created
        '''
        
        zip_path = os.path.join(self.out_folder, name)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.out_folder):
                for file in files:
                    if file == name:
                        continue
                    else:
                        fpath = os.path.join(root, file)
                        zipf.write(fpath, os.path.basename(fpath))
                        
    
    def detection(self, ds, threshold=0.2):
        '''Checking for values above threshold and creating outputs.
        In this case a csv file and a map'''
        
        overall_name = ''.join([ds.attrs['SIMULATION_START_DATE'], '.zip'])
        
        a = 0
        for i in ds['time'].values:
            print (i)
            shot = ds[Raise_alert.var_name].sel(time=i)
            ash = shot.where(shot >= threshold, drop=True)
            if np.isnan(ash.values).all():
                continue
            else:
               df = ash.to_dataframe().dropna(how='any')
               timestamp = np.datetime_as_string(i, unit='m')
               df_name = ''.join(['eemep_forecast_', timestamp, '.csv'])
               df.to_csv(os.path.join(self.out_folder, df_name))
               self.mapping_regular_grid(shot['lon'].values, shot['lat'].values,
                                    shot.values, 
                                    ''.join(['Forecast for ', timestamp]), 
                                    timestamp)
               a += 1
        
        if a > 0:
            self.zipdir(overall_name)
            zip_path = os.path.join(self.out_folder, overall_name)
            send = Send_email(zip_path)
            send.send_email()
        









    
    