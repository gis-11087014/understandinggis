from math import radians 
from math import cos , sin	# IMPORT NECESSARY FUNCTIONS HERE

def compute_offset(origin, distance, direction):
    """
    Compute the location of a point at a given distance and direction from a specified location using trigonometry
    """
    
    angle = radians(direction)
    offset_x =	origin[0] + cos(angle) * distance 
    offset_y =	origin[1] + sin(angle) * distance 
    return (offset_x, offset_y)
#need to use [1] or [0] to specifi which value to calculate 

# this code tests whether your function works correctly
origin = (345678, 456789)
destination = compute_offset(origin, 1011, 123)	# move 1011m in a direction of 123 degrees 
print("CORRECT!!" if (int(destination[0]), int(destination[1])) == (345127, 457636) else f"INCORRECT!! Error: {(int(destination[0])-345127, int(destination[1])-457636)}")
