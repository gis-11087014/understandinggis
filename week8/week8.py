from rasterio import open as rio_open
from rasterio.plot import show as rio_show
from rasterio.transform import rowcol
from sys import exit
from numpy import zeros
from numpy import column_stack
from skimage.draw import circle_perimeter, line
from math import hypot

# set origin for viewshed
x0, y0 = 330000, 512500

#convert x0, y0 from coorf to image space
def coord_2_img(transform, x, y):
    """ 
    * Convert from coordinate space to image space using the 
    *   Affine transform object from a rasterio dataset
    """
    r, c = rowcol(transform, x, y)
    return int(r), int(c)
                    
#def = function
def viewshed(x0, y0, radius_m, observer_height, traget_height, dem_data, transform):
    """
    works out endpoint for each line of sight (each cell in circle)
    """
    
    # convert from coordinate space to image space
    r0, c0 = rowcol(transform, x0, y0)
    
    #returning the height and width of the dataset with .shape and exits if the origin are largest that 0 and smaller than width/hight of dataset
    # make sure that we are within the dataset
    if not 0 <= r0 < dem_data.shape[0] or not 0 <= c0 < dem_data.shape[1]:
        print(f"Sorry, {x0, y0} is not within the elevation dataset.")
        exit()
        
    #WE NEED TO KNOW LENGTH OF CELL IRL 
    #can access resolution of dataset by storign in transform[0] which takes the value of x or y as they are both the same
    # convert the radius (m) to pixels
    radius_px = int(radius_m / transform[0])
    
    #we now know starting location and radius so now need to find starting height 
    #height means elevation of origin location PLUS the obsever height 
    #so read DEM and add it to obsever height
    # get the observer height (above sea level)
    #remeber [] not () so it knows it numerical !!!
    height0 = dem_data[r0, c0] + observer_height
    print(height0)
    
    # get pixels in the perimeter of the viewshed
    for r, c in column_stack(circle_perimeter(r0, c0, radius_px)):

    # calculate line of sight to each pixel, pass output and get a new one back each time
    #output = line_of_sight(r0, c0, height0, r, c, target_height, radius_px, dem_data, transform, output)
        pass

    # return the resulting viewshed
    return output
    
def line_of_sight(r0, c0, height0, r1, c1, height1, radius, dem_data, transform, output):
    """
    works out the visibility of each poitn on a line from the origin of that locaiton
    """
    # init variable for biggest dydx so far (starts at -infinity)
    max_dydx = -float('inf')     

    # loop along the pixels in the line (excluding the first one)
    for r, c in column_stack(line(r0, c0, r1, c1))[1:]:
        
        dx = hypot(r - r0, c- c0)
        
        # if we go too far, or go off the edge of the data, stop looping
        if dx > radius or not 0 <= r < dem_data.shape[0] or not 0 <= c < dem_data.shape[1]:
            break 
        
        # calculate the current value for dy / dx
        base_dydx = (dem_data[(r, c)] - height0) / dx
        tip_dydx = (dem_data[(r, c)] + height1 - height0) / dx

        # if the tip dydx is bigger than the previous max, it is visible
        if (tip_dydx > max_dydx):
            output[(r, c)] = 1

        # if the base dydx is bigger than the previous max, update
        max_dydx = max(max_dydx, base_dydx)

    # return updated output surface
    return output

# open the elevation data file
with rio_open("../../data/helvellyn/Helvellyn-50.tif") as dem:

    # read the data out of band 1 in the dataset
    dem_data = dem.read(1)
    
    #transform into image space
    r0, c0 = coord_2_img(dem.transform, x0, y0)
    
    output = zeros(dem_data.shape)

    dem_data[r0, c0] = 1
    
    # calculate the viewshed
    output = viewshed(x0, y0, 20000, 1.8, 100, dem_data, dem.transform)
    
    
    
    
    
    
    
    
    