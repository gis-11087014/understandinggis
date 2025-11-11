from rasterio import open as rio_open #importing rasterio
from rasterio.transform import rowcol, xy

#Now convert COORD -> IMAGE use the .rowcol() and .xy() methods to convert between x,y coordinates in a spatial reference system (coordinate space), and column,row locations in a raster dataset (image space).
#Pre-written code to convert (there are otherones but we only need this today)
def coord_2_img(transform, x, y):
    """ 
    * Convert from coordinate space to image space using the 
    * 	Affine transform object from a rasterio dataset
    *
    * Note that rowcol() returns floats so they need to be 
    * 	converted to integers to be used as cell references
    """
    row, col = rowcol(transform, x, y)
    return (int(row), int(col))

# open a raster file into a variable called dem
with rio_open('../../data/helvellyn/Helvellyn-50.tif') as dem:

	# everything inside the with block can access dem
    
    print(dem.profile)
    #needs to be inside so it can access dem
    
    #Raster data is organised into bands - or layers - each perfectly alligns 
    #they must be projected - we use OS that is already porjected onto BNG 
    #raster bands are ordered in a list - access using .read() 
    #intrested in band 1 - bands start at 1 not 0
    
    # get the single data band from a dem
    band_1 = dem.read(1)
    dem_data = band_1
    
    # print out the elevation at that location by reading it from the dataset
    #this does the working for me - dont need another line of code
    print(f"{dem_data[coord_2_img(dem.transform, 334170, 515165)]:.0f}m")

    
# once you leave the block, the file automatically closes for you

#Save as a GeoTiff - faster to read and more space efficient than CRS
#When we are inside the with statement, we have access to the dem variable (which you could call anything that you like as it is a variable). As soon as you leave the with block (the indented bit), the file is safely closed by Python and the dem variable is destroyed

#each band is stored in the dataset as a two dimensional list, which can be accessed in the form dem[row][column]
#to extract - use row and column to read values in the list aka the band
