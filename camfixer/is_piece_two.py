from typing import List, Dict
from shapely.geometry import Polygon


def is_piece_two(block: Dict, blocks: List[Dict]) -> bool:
    """This function compares a block with all the other blocks to determine if it is contained within another.
    
    Args:
        block (Dict): A dictionary with the data of the block to compare.
        blocks (List[Dict]): A list of dictionaries with the data of the other blocks.
        
    Returns:
        bool: A boolean value that is True if the block is contained within another, False otherwise.
    """
    result = None
    # Gets the polygon of the block.
    polygon1 = Polygon(block["polygon"])
    # Iterates over the blocks.
    for block2 in blocks:
        if block2 == block:
            continue
        # Gets the polygon of the other block.
        polygon2 = Polygon(block2["polygon"])
        # Compares the polygons.
        if polygon2.contains(polygon1):
            result = block2["main"]
            print(result)
            break

    return result


def main():
    from block_generator import _block_generator
    from shapely.wkt import loads
    
    processed_blocks = []
    block_gen = _block_generator("archivo.cam")
    blocks = list(block_gen)
    
    for block in blocks:
        # Convert the coordinates to a Shapely polygon
        polygon = loads(block["polygon_wkt"])
        block["is_piece"] = is_piece_two(block, blocks)
        processed_blocks.append(block)
    
    print(processed_blocks)


if __name__ == "__main__":
    main()