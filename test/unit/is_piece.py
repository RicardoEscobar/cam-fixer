"""This module compare a block with another block with all the other blocks to determine if it is contained within another"""

from typing import List, Dict


def is_inside(max_min1: Dict[str,float], max_min2: Dict[str,float]) -> bool:
        """This function compare a block with another block to determine if it is contained within another.
        The order of the coordinates is [min_x, max_x, min_y, max_y].
        Args:
            max_min1 (Dict[str,float]): A dict of floats with the max and min coordinates of the first block.
            max_min2 (Dict[str,float]): A dict of floats with the max and min coordinates of the second block.
        Returns:
            bool: A boolean value that is True if the first block is contained within the second block, False otherwise.
        """
        return (
            max_min1["min_x"] >= max_min2["min_x"]
            and max_min1["max_x"] <= max_min2["max_x"]
            and max_min1["min_y"] >= max_min2["min_y"]
            and max_min1["max_y"] <= max_min2["max_y"]
        )


def is_piece(block: Dict, blocks: List[Dict]) -> bool:
        """This function compare a block with all the other blocks to determine if it is contained within another.
        The structure of a block is a dictionary with this data:
        block = {
            "start": List[str],
            "arc": List[str],
            "main": List[str],
            "end": List[str],
            "text": str,
            "max_min": Dict[str, float],
        }

        Args:
            block (Dict): A dictionary with the data of the block to compare.
            blocks (List[Dict]): A list of dictionaries with the data of the other blocks.
        Returns:
            bool: A boolean value that is True if the block is contained within another, False otherwise.
        """
        result = True
        # Gets the maximum and minimum coordinates of the block.
        max_min1 = block["max_min"]
        # Iterates over the blocks.
        for block2 in blocks:
            if block2 == block:
                continue
            # Gets the maximum and minimum coordinates of the block.
            max_min2 = block2["max_min"]
            # Compares the blocks.
            if is_inside(max_min1, max_min2):
                result = False
                break

        return result


def main():
    from block_generator import _block_generator
    proccessed_blocks = []
    block_gen = _block_generator("archivo.cam")
    blocks = list(block_gen)
    for block in blocks:
        block["is_piece"] = is_piece(block, blocks)
        proccessed_blocks.append(block)
    print(proccessed_blocks)


if __name__ == "__main__":
    main()
