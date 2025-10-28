from math import radians 
from math import cos , sin	# IMPORT NECESSARY FUNCTIONS HERE
from geopandas import read_file , GeoDataFrame

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given distance and direction from a specified location using trigonometry
    """
    angle = radians(direction)
    offset_x =	origin[0] + cos(angle) * distance 
    offset_y =	origin[1] + sin(angle) * distance 
    return (offset_x, offset_y)
#need to use [1] or [0] to specify which value to calculate 
#direction is the angle but not in radians so need to input that line to make into radians 

# this code tests whether your function works correctly
origin = (345678, 456789)
destination = compute_offset(origin, 1011, 123)	# move 1011m in a direction of 123 degrees 
print("CORRECT!!" if (int(destination[0]), int(destination[1])) == (345127, 457636) else f"INCORRECT!! Error: {(int(destination[0])-345127, int(destination[1])-457636)}")

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the Iceland from it 
iceland = world[(world.ISO_A3 == 'ISL')]

# open iceland data 
land_cover = read_file("../../data/iceland/gis_osm_natural_a_free_1.shp")

# extract land cover that is ice from it 
ice = land_cover[(land_cover.fclass == "glacier")]

# get the bounds of the country - Iceland in this case 
minx, miny, maxx, maxy = iceland.total_bounds

# extract the tuple into 4 variables
print(f"minx: {minx}, miny: {miny}, maxx: {maxx}, maxy: {maxy}")

print(iceland.total_bounds)