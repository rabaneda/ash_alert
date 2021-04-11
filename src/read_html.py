#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 12:24:51 2021

@author: albertosr
"""

import urllib.request
import shutil
import tempfile
import re
from datetime import datetime
import xarray as xr


class URL_dataset:
    
    site = 'https://thredds.met.no/thredds/catalog/metusers/heikok/ash/krisuvik/catalog.html'
    opendap = 'https://thredds.met.no/thredds/dodsC/metusers/heikok/ash/krisuvik/'
    http = 'https://thredds.met.no/thredds/fileServer/metusers/heikok/ash/krisuvik/'
    filename_example = 'eemep_hourInst_20210410T084602.nc'
    
    def get_dataset(self):
        '''
        This method will retrieve the newest eemep_hourInst_*.nc file added
        to the website as a xarray dataset object
        
        '''
        
        with urllib.request.urlopen(URL_dataset.site) as response:
           html = response.read().decode("utf-8")
           
        occs = [i.start() for i in re.finditer('eemep_hourInst_', html)]
        files = [html[x:x+len(URL_dataset.filename_example)] for x in occs]
        times = [datetime.strptime(f[15:-3], '%Y%m%dT%H%M%S') for f in set(files)]
        times.sort(reverse=True)
        new = times[0].strftime('%Y%m%dT%H%M%S')
        selected = ''.join(['eemep_hourInst_', new, '.nc'])

        opendap_url = ''.join([URL_dataset.opendap, selected])
        http_url = ''.join([URL_dataset.http, selected])
        
        try:
            #openning with xarray
            #This method may fail due to bug in pydap library:
            #check https://github.com/pydap/pydap/issues/196
            #Apparently pydap works in "ascii" standard instead of "utf-8" for strings  
            ds = xr.open_dataset(opendap_url)
            
        except OSError:
            print('Access with OPENDAP failed. Downloading dataset via HTTPS')
            with urllib.request.urlopen(http_url) as remote:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    shutil.copyfileobj(remote, tmp_file)
                    ds = xr.open_datraset(tmp_file)
            
        return ds




