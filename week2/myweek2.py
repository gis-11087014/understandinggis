# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 12:47:55 2025

@author: p48883db
"""
#geopandas uses the object GeoDataFrame to hold the data and the geometry in the dataset
from geopandas import read_file, GeoSeries
from matplotlib.pyplot import subplots, savefig, title

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# print a list of all of the columns in the shapefile
#a simple list of all the columns avaliable 
print(world.columns)

#extractuing the 3 letter country code from each data set list to be a standard 
#type is a class i.e. GeoDataFrame is a class with objects in 
#class is the code that defines an object 
#from  the GDF set, .loc property extracts a new GDF only containing the ISO3 codes - the standardised country codes
#we use a query to check that the outcome is true for one we knwo is certain i.e. USA 

# extract the country rows as a GeoDataFrame object with 1 row
usa = world.loc[(world.ISO_A3 == 'USA')]

print(type(usa))

#.geometry extracts the geometry from the 3 letter codes only (1 row x 1 column not many)
#this is now a GeoSeries (1x1)
#a GDF object comprised a GeoSeries and a table of attributes 

# extract the geometry columns as a GeoSeries object
usa_col = usa.geometry

print(type(usa_col))

#.iloc is index location and is another propert of the GDF object 
#creates a number to reprsent the row ID 
#only 1 row in this sections, which returns underlying geometry - the MultiPolygon object in the shapley library 

# extract the geometry objects themselves from the GeoSeries
usa_geom = usa_col.iloc[0]

print(type(usa_geom))

#Here we use the the .loc (location) property of the GeoDataFrame object 

mex = world.loc[(world.ISO_A3 == 'MEX')]
print(type(mex))
mex_col = mex.geometry
print(type(mex_col))
mex_geom = mex_col.iloc[0]
print(type(mex_geom))

#extracting the shared boundary between the USA and MEX shapes using intersection  functionn 
#the countries are just geometyr objects 
border = usa_geom.intersection(mex_geom)

print(border)

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# plot the border
GeoSeries(border).plot(
  ax = my_ax
	)

# save the image
savefig('./out/first-border.png')