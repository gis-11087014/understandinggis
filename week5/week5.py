from math import radians 
from math import cos , sin, hypot # IMPORT NECESSARY FUNCTIONS HERE
from geopandas import read_file
from pyproj import Geod , CRS , Transformer 
from numpy.random import uniform
from numpy import arange
from shapely.geometry import Polygon

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

def evaluate_distortion(g, transformer, minx, miny, maxx, maxy, minr, maxr, sample_number=1000, vertices=16):
    # calculate the required number of random locations (x and y separately) plus radius
    xs = uniform(low=minx, high=maxx, size=sample_number) 
    ys = uniform(low=miny, high=maxy, size=sample_number)
    rs = uniform(low=minr, high=maxr, size=sample_number)
    # rs = random circle radii 
    # uniform draws random numbers from a uniform distibution
    # offset distances (constructing circles - preparation)
   
    forward_azimuths = arange(0, 360, 22.5)
    # FA thingy is a given dist and direction 
    # defines 16 directions, same as range but permits use of non integer numbers
    
    #create 3 empty lists 
    area_indices = []
    shape_indices = []
    distance_indices = []
    
    for x, y, r in zip(area_indices, shape_indices, distance_indices):
        # each random circle is deifned by x, y, r in each iteration of the loop 
        # zip allos us to loop thorugh them all at once - built in function
        # construct a circle around the centre point on the ellipsoid
        
        lons, lats = g.fwd([x]*vertices, [y]*vertices, forward_azimuths, [r]*vertices)[:2]
        # this multiplys the [??] value by the whole list of veritcles 
        # add [:2] on the end cuz we dont want the back azimuth which is auto in this list so we slice it to ignore it
        
        #LOOPING THROUGH TO PROJECT COORDS 
        # project the result, calculate area, append to the list
        e_coords = [ transformer.transform(lon, lat, direction='FORWARD') for lon, lat in zip(lons, lats) ]
        # forward means geographical -> porjected trandformation and backward is the otherway around 
        # get the area of the resulting circle
        ellipsoidal_area = Polygon(e_coords).area
        
        #doing same thing (area) for a circle consturcted on a projection plane (not ellipsoid) 
        #transforming x,y coord (centre of circle) and calc the 16 points around the edge using compute_offset() - created in pt1. 
        #will use list comprehension for elegance and effeciency
        
        # transform the centre point to the projected CRS
        centre_x, centre_y = transformer.transform(x, y, direction='FORWARD')
        # construct a circle around the projected point on a plane, calculate area
        planar_area = Polygon([ compute_offset(centre_x, centre_y, r, az) for az in forward_azimuths ]).area
   
        # code to calc area distortion (Jonny's equation)
        area_indices.append(abs(ellipsoidal_area - planar_area) / abs(ellipsoidal_area + planar_area))         
        # abs makes it always a postive number
        
        # now do the same for shape distortion
        # get radial distances from the centre to each of the 16 points on the circle
        ellipsoidal_radial_distances = [ hypot(centre_x - ex, centre_y - ey) for ex, ey in e_coords ]
        # get the absolute proportional difference between the expected and actual radial distance for each 'spoke'
        shape_distortion = [abs((1 / vertices) - (d / sum(ellipsoidal_radial_distances))) for d in ellipsoidal_radial_distances]
        # gets 16 absolute proportions (aka differences in expected length) and then tyring to find the sum and append to shape_indicies list 
        
    print(area_indices, shape_indices)
    return 

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

# loop through each CRS
for ax_num, projection in enumerate(projections):
    # initialise a PyProj Transformer to transform coordinates
    transformer = Transformer.from_crs(CRS.from_proj4(geo_string), CRS.from_proj4(projection['proj']), always_xy=True)
    # calculate the distortion
    Ep, Es, Ea = evaluate_distortion(g, transformer, minx, miny, maxx, maxy, 10000, 1000000, 1000)
    