from rasterio import open as rio_open
from rasterio.transform import rowcol
from rasterio.plot import show as rio_show
from matplotlib.pyplot import subplots, savefig
from numpy import zeros
from matplotlib.colors import LinearSegmentedColormap

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
    
    # set the cell at x, y to 1
    #setting the value in the array position that coresponds to these coords as 1 so it is setting the peak of the mountain as a new colour
    dem_data[dem.index(334170, 515165)] = 1
    
    # plot the dataset
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add the DEM
rio_show(
  dem_data,
  ax=my_ax,
  transform = dem.transform,
)

# add the empty layer, plotting empty 0s ontop of the DEM 
rio_show(
    output,
    ax=my_ax,
    transform=dem.transform,
    cmap = LinearSegmentedColormap.from_list('binary', [(0, 0, 0, 0), (0, 0.5, 1, 0.5)], N=2)
    )

#CMAP EXPLAINAITON 
#now edit colour map of layer so it doesnt obscure DEM by cretaing classified colout scheme
#add a list of tuples where 0=invisible and 1=blue (where we want new info), a scale of 0-1
#goes it goes red, green, blue, alpha to make colours 

# save the resulting map
savefig('./out/6.png', bbox_inches='tight')


#now edit colour map of layer so it doesnt obscure DEM by cretaing classified colout scheme
#add a list of tuples where 0=invisible and 1=blue (where we want new info), a scale of 0-1