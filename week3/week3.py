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
from shapely import STRtree

# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp").to_crs(pop_points.crs)
#add to the end to make the same CRS 
gulu_district = read_file("../../data/gulu/district.shp")

#cuz three main CRS types, they could come out as any which is bad and hard to compare 
#but we can specifiy yay! using member functions 
#to use, just add on the end of .crs 

print(pop_points.crs.to_epsg()) 
print(water_points.crs.to_epsg()) 
print(gulu_district.crs.to_epsg()) 

#these are the EPSG codes - so can look up to locate on map 
#UTM Zone 36N is a local conformal 
#full is called Arc 1960 / ... where this is the datum the CRS uses - the refenece frame that maps an ellipsoid to the earth, in this case Clark 1880 
#they also have local and global variants - we have only used WGS84 so far, the global datum so no we want local 
#other wats to project EPSG on the websire - we odnt need we alreayd have pop_points 
#we now want to match the CRS of all out data sets using the .to_crs function of GDF object 

#now we use Spatial Index (SI) in geopandas to automaticaly help with topological operations in GDF/GeoSeries objects 
#not great for undertsnaidng what it is even if easy 
#now creating own SI to undertsnd better and then covert to higher-level geopandas version for comparison 
#just useful innit 
#will be used laterin course when data cant be stores in GDF 
#there are also other opeiotn for SI libraries - both availabel on the UGIS website thing 

#BUILDING OWN SI WITH SHAPLEY.STRTREE

#FIRST need to rmeove all water pouints outside out areas of intrest - the Gulu District
#THEN we need to work out the nearest borehole to each house (well poitn to pop poitn) and calc the distance between 
#THEN we make a map and see patterns emerge! 
#sounds easy, just volume makes comlicated

print(f"Population points: {len(pop_points.index)}")
print(f"Initial wells: {len(water_points.index)}")

#f" is an f-string which means formattign strong literals - simple way to combine python with text output
#add an f to the start of a strign and statement in {} 
#when string used the python valuse are calced and results are added into strign 
 
# {len(pop_points.index) is used to calc the number of rows n the GDF to built in len() - need to use index or a column to get rows 
# if you pass GDF itself it will give u columsn 

#SI is used to reduce the number of calc that need doing at currenlty it would be 128 million distances so we are just making more efficient 
#STRtree is a read only, cannot add or remove objects from the index without a complete re-buid

# get the geometries from the water points geodataframe as a list
geoms = water_points.geometry.to_list()

# initialise an instance of an STRtree using the geometries
idx = STRtree(geoms)

#this extract all the geometriews form the WP GDF and converts it from a pandas.series object to a list and loads it into STRtree objects 
#the STRtree construtoe will calc bounding box (smallest reatngin aligned to axis) and load into the RTree SI 

#OPTIMISIGN INTERSECTIONS W/ SI 

#use SI to filtr wells to exclude all outside Gulu area - defined as polygon district 
#will do through ... 
    #get SI borehole ID outside bounding box (distrioct)
    # quetery the GDF to return rows that match ID - index - numbers 
    #use topological within text to assess results are inside distict or not 
    #re-build SI to only inlucde those within the distric polygon 

#1. retreive the polygon usign .icoc[0] - the first idex location and report boreholes in the set with f-stirng 
#2. .query to find intersectinf boreoles with bounds of distric 
#3. reults list used to query WP GDF using .iloc and report how many hole meet this 
#4. use a smaller data set and within queruy to test it worked 

# get the one and only polygon from the district dataset
polygon = gulu_district.geometry.iloc[0]
# how many rows are we starting with?
print(f"Initial wells: {len(water_points.index)}")
# get the indexes of wells that intersect bounds of the district
possible_matches_index = idx.query(polygon)
# use those indexes to extract the possible matches from the GeoDataFrame
possible_matches = water_points.iloc[possible_matches_index]
# how many rows are left now? 
print(f"Filtered wells: {len(possible_matches.index)}")
# then search the possible matches for precise matches using the slower but more precise method
precise_matches = possible_matches.loc[possible_matches.within(polygon)]
# how many rows are left now?
print(f"Filtered wells: {len(precise_matches.index)}")

#OPTIMISING NEAREST NEIGHBOUR W/ SI 

#need to know distance from each pop point to nearest hoel then calc mean distance 
#use SI to reduce calcs and efficeieny 
#need to rebuild SI to make sure no. of bore holes matches the amount we found in the section above as we want to use the SI again 
#then use idx.nearest to find nearest neighbour to reduce no. of calcs 
#to rebuild we need to ovrride previos shapley.STRtree as read only, need to reflect contents wanted 

# rebuild the spatial index using the new, smaller dataset
geoms = precise_matches.geometry.to_list()
idx = STRtree(geoms)
#this is where you fucked up - remembr to do geoms before each idx 

#NEAREST NEIGHBOUR 

#want to loop each pop point and calc nearest water point usign SI to determine distance 
#cant simply loop thorugh GDF rows contained w/in it as will loop columns. 
#need to use len(gdf) to retuen columns so need to use len(gdf.index) insteead 
#to loop GDF rows data rows, use .iterrows() function to retuen iterable rep. of data rows and loop though that. 
#.iterrows() returns 2 vlaues in each iteration loop as we haev both ID and Well 
#ID is the index of the data set - a unique ID for each lien 
#was .iloc last week - ID locator 
#Well is the actual row of data in the loop - columns access and geometry 
#remember to use len(GDF.index) for row no.s and gdf.itterrows() when interating rows 

#define an empty list in variabel called distances 
distances = []
#open a for loop that iterates throuigh pop-points usign variables ID and Hoise to storw the index and row respectivley 
for id, house in pop_points.iterrows(): 
    #now put code inside loop to get ID of nearest well, resuluign ID number, distance between pop and hole and call result distance 
    # use the spatial index to get the index of the closest well
    nearest_well_index = idx.nearest(house.geometry)
    # use the spatial index to get the closest well object from the original dataset
    nearest_well = precise_matches.iloc[nearest_well_index].geometry.geoms[0]
    #.iloc needs to have a value or list to read from which is NWI in this case 
    #wells are a MulitPoint return - collection of individual points 
    #so extract point objects from MultiPpoint usign .geoms to make list 
    #add .geoms[0] to extract individal point from MP 
    #FINALLY measure distance to nearest well usign diatcnae and appened result to distances list 
    # store the distance to the nearest well
    distances.append(distance(house.geometry.x, house.geometry.y, nearest_well.x, nearest_well.y))
print(f"distance: {len(distances)}")
#need to be an f-chain - i thin kcuz a list  


    