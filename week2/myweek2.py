# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 12:47:55 2025

@author: p48883db
"""
#geopandas uses the object GeoDataFrame to hold the data and the geometry in the dataset
from geopandas import read_file, GeoSeries
from matplotlib.pyplot import subplots, savefig, title
from pyproj import Geod

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

 #open the graticule dataset
graticule = read_file("../../data/natural-earth/ne_110m_graticules_5.shp")

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


#use ellipsodial distance claculations to avoid erros when using projections too big 
#pyproj is the most accurate as it does the complex maths invloved in this projetcion

# set which ellipsoid you would like to use
#creates a Geod object based on WGS84 - common general model of the shape of the earth 
#stored in variable g 
#gives access to vincenty equations (pair of equations) for ellipsoid measurements to be made 
#forward and inverse equations - Geod.fwd and Geod.inv 
#fwd calcs point on sphere a given distance and direction away from another - locates and finds the point based on a distance
#inv calcs the distance and direction between a pair of points - calculates the distacne 
#cuz earth is round, the equations calc the distored striaght line that actually follows the earth - liek a plane 
#to do this inv returns 2 directions (fwd azimuth - diuirection from point A u set off from - and back azimuth - direstion set of from B to A) 
g = Geod(ellps='WGS84')

#g.inv function makes a list of 3 values which is made into variables by python 
#we dont want these - it makes azF and azB and rthen the result, we only want the reuslt 
# so we use a code that only give us the 3rd value which is teh actual reuslt. 
#basically choosing not to store them cuz they useless
#to calc a distance we need to put in 4 arguments for the function to run - the long and lat of both points

print(border)

#multilinestign is made up of linestring (segemnts) where the end point of one is the start of another 
#to work out length, we need to work out the lengeth of each segment and add the together 
#so we make a loop - measure the distances and add them together to make a total 
#to make loop, convert it to a list of its constituent LineString using .geoms property 
#this gives access to the start and end of the coords of each segemtn usign segment.coords[0] and segemnt.coords[1] and so on 

# loop through each segment in the line and print the coordinates
for segment in border.geoms:
	print(f"from:{segment.coords[0]}\tto:{segment.coords[1]}")

#the /t makes it a neat list 
#now the pairs of coords are stores as a tuple (list but unchangebale)
#to access a single tuple, use [] to specify the index value 
#but as its a list of tuples we need to use 2 index references (the []), one to reference coord pair (start n end) and one to ref the coord (llong n lat) 
# cux long before lat the long value from the start point (sengment.coords[0])woudl be segmemnt segment.coords[0][0] whereas the lat from the end point would be [1] etc 
#(segment.coords[0] is the start point so putting another [0] makes it longitute and [1] is the end or the lat )

# initialise a variable to hold the cumulative length
cumulative_length = 0

# loop through each segment in the line

for segment in border.geoms:
    print(f"from:{segment.coords[0]}\tto:{segment.coords[1]}")
    
	# THIS LINE NEEDS COMPLETING
    # segment.coords[0] is the start point and [1] is the end so putting a second [0] on the end makes it long cuz that was first and then addign a [1] is lat 
    distance = g.inv(segment.coords[0][0], segment.coords[0][1], segment.coords[1][0], segment.coords[1][1])[2]

	# add the distance to our cumulative total
    cumulative_length += distance

#REMEMBER - cum length and distance need to be forward or it wont pritn 
#initialise startign value 0 as cum length, then a loop through the list, then addign the distcances with += to 0 

print(cumulative_length)

lambert_conic = ("+proj=lcc +lon_0=-106.3476562 +lat_1=22.645838 +lat_2=37.3130861 +lat_0=29.979462 +datum=WGS84 +units=m +no_defs")
#this is the porjection from the wizard website made into a varible 

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# set title
title(f"Trump's wall would have been {cumulative_length / 1000:.2f} km long.")

# project border
border_series = GeoSeries(border, crs=world.crs).to_crs(lambert_conic)

# extract the bounds from the (projected) GeoSeries Object
minx, miny, maxx, maxy = border_series.geometry.iloc[0].bounds

# set bounds (10000m buffer around the border itself, to give us some context)
buffer = 10000
my_ax.set_xlim([minx - buffer, maxx + buffer])
my_ax.set_ylim([miny - buffer, maxy + buffer])

# plot data
usa.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#ccebc5',
    edgecolor = '#4daf4a',
    linewidth = 0.5,
    )
mex.to_crs(lambert_conic).plot(
    ax = my_ax,
    color = '#fed9a6',
    edgecolor = '#ff7f00',
    linewidth = 0.5,
    )
border_series.plot(     # note that this has already been projected above!
    ax = my_ax,
    color = '#984ea3',
    linewidth = 2,
    )
graticule.to_crs(lambert_conic).plot(
    ax=my_ax,
    color='grey',
    linewidth = 1,
    )

# save the result
savefig('out/2.png', bbox_inches='tight')
print("done!")


