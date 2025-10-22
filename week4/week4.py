from geopandas import read_file
from math import sqrt
from sys import exit
from shapely.geometry import LineString

# set the percentage of nodes that you want to remove
SIMPLIFICATION_PERC = 98
#setting variable right at the top to easily find

#working out effective area of each point - area of trinagle from both neighbour points
#set formular for calculating trignale areas
def get_effective_area(a, b, c):
	"""
	* Calculate the area of a triangle made from the points a, b and c using Heron's formula
	* 	https://en.wikipedia.org/wiki/Heron%27s_formula
	"""
	# calculate the length of each side
	side_a = distance(b[0], b[1], c[0], c[1])
	side_b = distance(a[0], a[1], c[0], c[1])
	side_c = distance(a[0], a[1], b[0], b[1])

	# calculate semi-perimeter of the triangle (perimeter / 2)
	s = (side_a + side_b + side_c) / 2

	# apply Heron's formula and return
	return sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

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

def visvalingam_whyatt(node_list, n_nodes):
    #create empty function with def, below inputs but above rest 
    #put arguements in brakctes 
    #node list is points to simplify and n nodes is number of nodes returned in list
    #cant make effective area (EA) for end points as only 1 touching so no trignale therefore we use raneg to skip end points 
    #range from second in until second last 
    #then calc EA and store in dictionary in list called areas 
    #dic will have point and EA connected 
    # loop through each node, excluding the end points
   areas = []
   for i in range(1, len(node_list)-1):
  # get the effective area
          area = get_effective_area(node_list[i-1], node_list[i], node_list[i+1])	# COMPLETE THIS LINE
#nodelist i-1 is the point before nodelist i which we need to make a triangle, same with i+1 
  # append the node and effective area to the list
          areas.append({"point": node_list[i], "area": area})
#now makign 'fake EA' for that end points w/ .insert() at index locations 0 (start) and len(area) (the end)
#len is length 
    # add the end points back in at the start (0) and end (len(areas))
    #need to add this after loop cuz otherwise you would add them everytime so would be wrong
   areas.insert(0, {"point": node_list[0], "area": 0})
   areas.insert(len(areas), {"point": node_list[len(node_list)-1], "area": 0})
   print("areas:", len(areas), "node_list:", len(node_list))
   
   # take a copy of the list so that we don't edit the original - can edit nodes and not areas 
   nodes = areas.copy()

   #now need loop statement to find desired no of nodes - a while loop 
   #keeps going until certain condition is met not all of it 
   #we are looping until no of nodes = n_nodes value 
   # keep going as long as the number of nodes is greater than the desired number - until nodes<n_nodes
   while len(nodes) > n_nodes:
       
       min_area = float("inf")
       
       for i in range(1, len(nodes)-1): 
           #needs to be i not area - idk why 
           if nodes[i]['area'] < min_area:
               min_area = nodes[i]['area']
               node_to_delete = i 
               # remove the current point from the list
       nodes.pop(node_to_delete)
   #inside while but not for cuz dont wnat to remove every single interation 
   #now need to find the EA of the new point pattern which is when the node to delete is gone so now has new neighbours 
   # recalculate effective area to the left of the deleted node
       nodes[node_to_delete-1]['area'] = get_effective_area(nodes[node_to_delete-2]['point'], nodes[node_to_delete-1]['point'], nodes[node_to_delete]['point'])	# COMPLETE THIS LINE
# if there is a node to the right of the deleted node, recalculate the effective area
       if node_to_delete < len(nodes)-1:
            nodes[node_to_delete]['area'] = get_effective_area(nodes[node_to_delete-1]['point'], nodes[node_to_delete]['point'], nodes[node_to_delete+1]['point']  )		# COMPLETE THIS LINE
   # extract the nodes and return
   #list comprehension to get the coords not the EA form the nodes list
   #much neater than running a normal loop 
   return [ node['point'] for node in nodes ]

#DEF NEED TO BE SEPERATE TO CALL BACK TO THEM INDIVIDUALLOY AND AVOID REPETITION - THIS IS WHY FUNCTION  

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[(world.ISO_A3 == 'GBR')].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE

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

# report geometry type
print(f"geometry type: {uk.geom_type}")

# now we dont have a MultiPolygon, we need to work out which of its parts is the largest Polygon... 

# initialise variables to hold the coordinates and area of the largest polygon
biggest_area = 0
coord_list = []
#coord_list is a coordinate list, typoing this is basically saying this is what we will work otu 

# loop through each polygon in the multipolygon and find the biggest (mainland Great Britain)
for poly in uk.geoms:

	# if it is the biggest so far
	if poly.area > biggest_area:	# COMPLETE THIS LINE
    #this means if the polygon now being looked at is bigger than the previosly largets one found, this will now be the new compartions polygon until all have been compared and the largest is found
    
		biggest_area = poly.area
		coord_list = list(poly.boundary.coords) 
        
#this extracts the boundary of the Polygon which then etxracts list of coord paits using .coords whihc is converted into a list 

#REMEMBER TO REMOVE UNNEEDED PRINT STATEMENTS THIS WILL BE BAD FOR ASSESSMENTS 

#VW tringle methog makes a line recuced into node (defined number)
#a percentage of nodes removed - type % we want remaining 

# how many nodes do we need?
n_nodes = int(len(coord_list) / 100.0 * (100 - SIMPLIFICATION_PERC))

# ensure that there are at least 3 nodes (minimum for a polygon otherwise it wont work)
if n_nodes < 3:
	n_nodes = 3
    
#going to use a function instead of just adding VW algroithm directly so it can be called numlitpl times and its neater 

  # remove one node and overwrite it with the new, shorter list
simplified_nodes = visvalingam_whyatt(coord_list, n_nodes)

#now need loop to remove the repeatedly found smallest EA until we are left with the desired no. of nodes 
#cuz removing items from list, we want to take a copy - need OG to compare later 
#need to make shallow copy - new items references not also copied (deep) 

# make a linestring out of the coordinates
before_line = LineString(coord_list)
print(f"original node count: {len(coord_list)}")
print(f"original length: {before_line.length / 1000:.2f}km\n")

# make the resulting list of coordinates into a line
after_line = LineString(simplified_nodes)
print(f"simplified node count: {len(simplified_nodes)}")
print(f"simplified length: {after_line.length / 1000:.2f}km\n") #using \n makes a blank line in the run bit 

