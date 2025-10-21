#CONDITIONAL STATEMENTS 

from geopandas import read_file

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[(world.ISO_A3 == 'GBR')].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")

#the EPSD:... bit is telling the code the UK (british national grid) area we want so insert that to make it not world
#and the world.ISO... is where you make the code know its GBR from the ww defined country bs (week 2)
