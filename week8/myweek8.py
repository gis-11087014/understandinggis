# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 12:25:20 2025

@author: p48883db
"""

from numpy import zeros
from rasterio import open as rio_open
from rasterio.plot import show as rio_show
from matplotlib.pyplot import subplots, savefig
from matplotlib.colors import LinearSegmentedColormap
from rasterio.transform import rowcol
from geopandas import GeoSeries
from shapely.geometry import Point
from skimage.draw import line
from numpy import column_stack
from skimage.draw import circle_perimeter

# set origin 
LOCATION = (334170, 515165)

def coord_2_img(transform, x, y):
	""" 
	* Convert from coordinate space to image space using the 
	*   Affine transform object from a rasterio dataset
	"""
	r, c = rowcol(transform, x, y)
	return int(r), int(c)

# open the elevation data file
with rio_open("../../data/helvellyn/Helvellyn-50.tif") as dem:

    # read the data out of band 1 in the dataset
    dem_data = dem.read(1)

    # create a new 'band' of raster data the same size
    output = zeros(dem_data.shape)
    
    # transform the coordinates for the summit of Helvellyn into image space
    #storing these into image space to be used later
    row, col = coord_2_img(dem.transform, 334170, 515165)

    # set the cell at x, y to 1
    #setting the value in the array position that coresponds to these coords as 1 so it is setting the peak of the mountain as a new colour
    dem_data[dem.index(334170, 515165)] = 1
    
    #list of pixel locations that describe a line between 2 locations - produces tuple of numpy arrays
    #print(line(row, col, row, col+50))
    
    #column stack will stack the 1D arrays and return them in a 2D array 
    #print(column_stack(line(row, col, row, col+50)))
    
    #makes all the coords red through loopign onto output layer
    #dont need .index cuz not flattening it
    for r, c in column_stack(line(row, col, row, col+50)):
        
        #turns transparent coords into a red layer 
        output[r, c] = 1
        
        print(output)
    
    #makes circle and makes it red yay
    for r, c in column_stack(circle_perimeter(row, col, 50)):
        
        output[r,c] = 1
        
        print(output)

# plot the dataset
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add the DEM
rio_show(
  dem_data,
  ax=my_ax,
  transform = dem.transform,
)
# add the drawing layer
rio_show(
    output,
    ax=my_ax,
    transform=dem.transform,
    cmap = LinearSegmentedColormap.from_list('binary_viewshed', [(0, 0, 0, 0), (1, 0, 0, 0.5)], N=2)
    )

savefig('./out/bresenham.png', bbox_inches='tight')

#empty layer over map, (1) and anything added will appear as red 
#start by drawing a poitnt 
    #convert coord pair from coord space to image space 
    #set pixel at this location in output suface to 1