from geopandas import read_file
from sys import exit

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[(world.ISO_A3 == 'GBR')].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")

#the EPSD:... bit is telling the code the UK (british national grid) area we want so insert that to make it not world
#and the world.ISO... is where you make the code know its GBR from the ww defined country bs (week 2)

#good practice to combine .geom_type prperty with a conditional to ensure code is robust where the analysis depends upon geometry type of the dataset 
  # anything in here would only run if the geometry is a MultiPolygon - MP cuz UK has islands 
  #for todasy though we want to extact mainland UK 
  #do this with by looping through each Polygon and calculated area 
  #cant do with only Polygon
  #therefore must check the .geom_type first ... 
# quit the analysis if we are dealing with any geometry but a MultiPolygon
if uk.geom_type != 'MultiPolygon':
  print("Geometry is not a MultiPolygon, exiting...")
  exit()
  #extracts largest polygon and EXIT() to check it wont cause error before we try it 
#!= (not equal to
#exit wont include rest of code - a solution to MultiPolygons 

# now we dont have a MultiPolygon, we need to work out which of its parts is the largest Polygon... 

# initialise variables to hold the coordinates and area of the largest polygon
biggest_area = 0
coord_list = []
#coord_list is a coordinate list 

# loop through each polygon in the multipolygon and find the biggest (mainland Great Britain)
for poly in uk.geoms:

	# if it is the biggest so far
	if poly.area > biggest_area:	# COMPLETE THIS LINE
    
		# store the new value for biggest area
		biggest_area = poly.area
        
     # store the coordinates of the polygon
coord_list = list(poly.boundary.coords)	# COMPLETE THIS LINE (look at the variables that you defined before the loop
#this extracts the boundary of the Polygon which then etxracts list of coord paits using .coords whihc is converted into a list 
print(coord_list)
print(biggest_area)
