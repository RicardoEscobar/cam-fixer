"""This module process each block separately to calculate maximum and minimum coordinates"""

from typing import List, Dict

from camfixer.get_coordinates import get_coordinates


def get_max_min(main_block: List[str]) -> Dict[str, float]:
    """This function process each block separately to calculate maximum and minimum coordinates.
    args:
        main_block (List[str]): A list of strings with the main block of the cam file.
    Returns:
        Dict[str, float]: A dictionary with the maximum and minimum coordinates.
    """
    result = {
        "max_x": float("-inf"),
        "min_x": float("inf"),
        "max_y": float("-inf"),
        "min_y": float("inf"),
    }
    # Iterates over the lines of the main block.
    for line in main_block:
        # Gets the coordinates from the line.
        coordinates = get_coordinates(line)
        if coordinates:
            x, y, *_ = coordinates
            # Updates the maximum and minimum coordinates.
            result["max_x"] = max(result["max_x"], x)
            result["min_x"] = min(result["min_x"], x)
            result["max_y"] = max(result["max_y"], y)
            result["min_y"] = min(result["min_y"], y)

    return result


if __name__ == "__main__":
    block = [
        "G01X+1928.2Y-892.4",
        "G01X+1921.2Y-884.5",
        "G02X+1914.6Y-884.5I+1914.6J-899.5",
        "G01X+1901.4Y-892.6",
        "G03X+1866.9Y-958.8I+1849.2J-949.5",
        "G01X+1831.4Y-958.8",
        "G02X+1797.0Y-892.6I+1783.7J-899.5",
        "G01X+1783.7Y-884.5",
        "G01X+1777.2Y-884.5",
        "G02X+1763.0Y-900.3I+1774.2J-910.3",
        "G01X+1759.2Y-910.3",
        "G02X+1759.2Y-1089.5I+1849.2J-1089.5",
        "G01X+1939.2Y-1089.5",
        "G02X+1939.2Y-910.3I+1924.2J-910.3",
        "G01X+1935.3Y-900.3",
    ]
    resultado = get_max_min(block)
    print(resultado)
