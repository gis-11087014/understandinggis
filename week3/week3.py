#welcome to week 3!!! you're smashing it bitch!! 
#function - bit of code that does something 
#using a cunction is called 'calling it'
#values are called arguements
#return statement at end is thr product of the function, the function defintion 
#fucntion distance = spherical_distance(x1, y1, x2, y2) will calc distance between x1,y1 qand x2,y2 and will store the result as distance

#first import from maths library
#then defin (def) the function and define the list of arguments that it would reciece in () 
#multiple arguments are seperated by commas ,
#if no arguements the just leave () blank 
#finally put in : to tell python that the code that follows is what the function should do 
#the next section should be indented, python will see all indented after the : to be in the function until no londer indented 
#the maths then return distance value
#functions dont need returns if they dont return a value i.e. print() 

#to call function, simple write name of it followed by () containgin arguements 
#if function returns a value then we store that in a variable usign = 
#functions shoudl be at top of code but below imports 
 
# THIS IMPORTS A SQUARE ROOT FUNCTION, WHICH IS A BIG HINT!!
from math import sqrt

def distance(x1, y1, x2, y2):
	"""
	* Use Pythagoras' theorem to measure the distance. This is acceptable in this case because:
	*	 - the CRS of the data is a local projection
	*	 - the distances are short
	*  - computational efficiency is important (as we are making many measurements)
	"""
	return sqrt((x2-x1)**2 + (y2-y1)**2)
# complete this line to return the distance between (x1,y1) and (x2,y2)
#** is sqaure in code

result = distance (345678, 456789 , 445678, 556789)
#result is the end of the code and using ur specificvalues 

print(result) 

#BORE HOLES 
#will calc mean walking distance to holes 
#assumptions made cuz map data scarce here i.e. as the crow flies; people location doen with pop model on facebook labs; using already exsitsing boreholes even thoguh incom plete 
#use spatial index to make calcs as efficient as possible
#we will make our own spatial index with STRtree class in the shapley library. 

#need to use CRS so no distortiosn occur so must make sure all data is in same CRS and appropriate for Northen Uganada
#geopandas makes this easy from getting GDF back as an object so we can use .crs to check the CRS and .to_crs() to change it if needed

from geopandas import read_file

# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp")
gulu_district = read_file("../../data/gulu/district.shp")

#cuz three main CRS types, they could come out as any which is bad and hard to compare 
#but we can specifiy yay! using member functions 
#to use, just add on the end of .crs 

print(pop_points.crs.to_epsg()) 
print(water_points.crs.to_epsg()) 
print(gulu_district.crs.to_epsg()) 