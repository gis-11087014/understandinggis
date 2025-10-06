big_fat_variable = "twat"
little_bitch_variable = "cunt"
the_perfect_variable = big_fat_variable + little_bitch_variable
print (the_perfect_variable)


from geopandas import read_file #used to get into a GeoDataFrame, makes functionality from libraries, no import first means code will have no idea.

world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp") #imported from geopandas library, new variable called world
print(world.columns)
graticule = read_file("../../data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("../../data/natural-earth/ne_110m_wgs84_bounding_box.shp")

print(world.head()) #convinience function that returns the first 5 rows of the dataset aka the head. therefore prints head 

from matplotlib.pyplot import subplots, savefig
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add bounding box and graticule layers
bbox.plot(
    ax = my_ax,
    color = 'skyblue',
    linewidth = 0,
    )

# plot the countries
world.plot(
    ax = my_ax,
    color = 'darkgreen',
    linewidth = 0.5,
    )

# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 0.5,
    )
# turn off the visible axes on the map
my_ax.axis('off')
# save the result
savefig('week1/out/1.png')
print("done!")
