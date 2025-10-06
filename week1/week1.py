big_fat_variable = "twat"
little_bitch_variable = "cunt"
the_perfect_variable = big_fat_variable + little_bitch_variable
print (the_perfect_variable)


from geopandas import read_file #used to get into a GeoDataFrame, makes functionality from libraries, no import first means code will have no idea.

world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp") #imported from geopandas library, new variable called world
print(world.columns)
graticule = read_file("../../data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("../../data/natural-earth/ne_110m_wgs84_bounding_box.shp")
ea_proj = ("+proj=eqearth +lon_0=0 +datum=WGS84 +units=m +no_defs")

# reproject all three layers to equal earth
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)

print(world.head()) #convinience function that returns the first 5 rows of the dataset aka the head. therefore prints head 

world['pop_density'] = world['POP_EST'] / (world.area / 1000000)
print(world.columns)

from matplotlib.pyplot import subplots, savefig
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add bounding box and graticule layers
bbox.plot(
    ax = my_ax,
    color = 'lightblue',
    linewidth = 0,
    )

# plot the countries
world.plot(								# plot the world dataset
    ax = my_ax,						# specify the axis object to draw it to
    column = 'pop_density',		# specify the column used to style the dataset
    cmap = 'YlGnBu',				# specify the colour map used to style the dataset based on POP_EST
    scheme = 'quantiles',	# specify how the colour map will be mapped to the values in POP_EST
    linewidth = 0.5,			# specify the line width for the country outlines
    edgecolor = 'gray',		# specify the line colour for the country outlines
    legend = 'True',
legend_kwds = {
    'loc': 'lower left',
    'title': 'Population Density'
    }
    )

# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 0.5,
    )
# turn off the visible axes on the map
my_ax.axis('off')

my_ax.set(title="Population Density: Equal Earth Coordinate Reference System")

# save the result
savefig('week1/out/1.png')
print("done!")
