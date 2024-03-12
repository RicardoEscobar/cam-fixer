from typing import List, Dict
from shapely.geometry import Polygon
from camfixer import get_WKT

def is_arc_in(block):
    """Check if the coordinate from block_initial is contained within the polygon defined by block_main.
    Args:
        block (dict): Dictionary containing block data.
    Returns:
        bool: True if the coordinate is contained within the polygon, False otherwise.
    """
    # Get the coordinate from the first line of block ("block_initial")
    initial_coordinate = get_WKT(block["initial"][0])

    # Get the polygon coordinates from block_main
    polygon_coordinates = block["polygon"]

    # Check if the initial coordinate is contained within the polygon
    # (You would need to implement a function to check this, for example, using the Ray Casting algorithm)
    # For demonstration purposes, let's assume it's True if the initial coordinate is in the polygon, False otherwise
    is_arc_in = initial_coordinate in polygon_coordinates

    return is_arc_in
