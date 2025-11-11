from rasterio import open as rio_open
from rasterio.transform import rowcol
from rasterio.plot import show as rio_show
from matplotlib.pyplot import subplots, savefig
from numpy import zeros


def coord_2_img(transform, x, y):
	""" 
	* Convert from coordinate space to image space using the 
	* 	Affine transform object from a rasterio dataset
	"""
	r, c = rowcol(transform, x, y)
	return (int(r), int(c))

# open the raster dataset
with rio_open("../../data/helvellyn/Helvellyn-50.tif") as dem:

    # read the data out of band 1 in the dataset
    dem_data = dem.read(1)
    
    #zero() creates a list of 0s, makes a numpy array 2D dataset 
    # create a new 'band' of raster data the same size
    output = zeros(dem_data.shape)
    
    # plot the dataset
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add the DEM
rio_show(
  dem_data,
  ax=my_ax,
  transform = dem.transform,
)

#plotting empty 0s ontop of the DEM 
# add the empty layer
rio_show(
    output,
    ax=my_ax,
    transform=dem.transform
    )

# save the resulting map
savefig('./out/6.png', bbox_inches='tight')
    