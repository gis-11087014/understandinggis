from math import radians 
from math import cos , sin	# IMPORT NECESSARY FUNCTIONS HERE
from geopandas import read_file
from pyproj import Geod

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

# get the bounds of the country - Iceland in this case - this is expanding the code
minx, miny, maxx, maxy = iceland.total_bounds

print(iceland.total_bounds)

#using WGS84 Datum as ellipsoidal for model - good for global scale project

# set the geographical proj string and ellipsoid (should be the same)
geo_string = "+proj=longlat +datum=WGS84 +no_defs"
g = Geod(ellps='WGS84')

# create a list of dictionaries for the projected CRS' to evaluate for distortion
projections = [
    {'name':"Web Mercator", 'description':"Global Conformal",   'proj':"+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs +type=crs"},
    {'name':"Eckert IV",    'description':"Global Equal Area",  'proj':"+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs"},
    {'name':"Albers equal-area conic", 'description':"Local Equal Area",   'proj':"+proj=aea +lon_0=-18.28125 +lat_1=61.2123032 +lat_2=67.3508634 +lat_0=64.2815833 +datum=WGS84 +units=m +no_defs"}
]
