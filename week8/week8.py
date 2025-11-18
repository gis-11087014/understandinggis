from rasterio import open as rio_open
from rasterio.plot import show as rio_show

# set origin for viewshed
x0, y0 = 330000, 512500

# open the elevation data file
with rio_open("../../data/helvellyn/Helvellyn-50.tif") as dem:

    # read the data out of band 1 in the dataset
    dem_data = dem.read(1)
    
    # calculate the viewshed
    output = viewshed(x0, y0, 20000, 1.8, 100, dem_data, dem.transform)