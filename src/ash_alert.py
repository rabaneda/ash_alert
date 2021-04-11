#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 00:32:49 2021

@author: albertosr
"""

from mask import Raise_alert
from read_html import URL_dataset

#=============================================================================
'''For this short tool, only 2 variables must be set. 

The folder where to keep all the outputs. Default is ./tmp.
But it is highly recommend to change the folder path.

Second the threshold to raise an alert. Default is 0.2 g/m2 of ash column.

'''

outputs = '/tmp'
threshold = None

#=============================================================================

if __name__ == "__main__":
    url = URL_dataset()
    data = url.get_dataset()
    alert = Raise_alert(data, outputs)
    masked = alert.mask_sea()
    if type(threshold) == int or type(threshold) == float:
        alert.detection(masked, threshold=threshold)
    else:
        alert.detection(masked)