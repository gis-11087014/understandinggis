# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 12:38:29 2025

@author: p48883db
"""

from rasterio import open as rio_open
from rasterio.transform import rowcol

def coord_2_img(transform, x, y):
	""" 
	* Convert from coordinate space to image space using the 
	* 	Affine transform object from a rasterio dataset
	"""
	r, c = rowcol(transform, x, y)
	return (int(r), int(c))


# open the raster dataset
with rio_open("../data/helvellyn/Helvellyn-50.tif") as dem:

    # read the data out of band 1 in the dataset
    dem_data = dem.read(1)
    
    