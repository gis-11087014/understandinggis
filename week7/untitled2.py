# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 13:33:08 2025

@author: p48883db
"""

print("Testing imports...")

from geopandas import GeoSeries
print("geopandas OK")

from shapely.geometry import Point
print("shapely OK")

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.cm import ScalarMappable
print("matplotlib extras OK")

from matplotlib_scalebar.scalebar import ScaleBar
print("scalebar OK")
