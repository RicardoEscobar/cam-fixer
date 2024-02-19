"""This module contains the function to get the coordinates from a cam file (one line)."""

import re


def get_coordinates(line):
    """Get the coordinates from a cam file (one line).

    Args:
        line (str): A line from a cam file. e.g. "G03X+269.8Y-29.0I+264.2J-23.4"

    Returns:
        tuple: A tuple with the coordinates. e.g. (269.8, -29.0, 264.2, -23.4).
    """
    # pattern = r"G0[0123]X([+-]?\d+\.\d+)Y([+-]?\d+\.\d+)I([+-]?\d+\.\d+)J([+-]?\d+\.\d+)"
    pattern = r"G0[0123]X([+-]?\d+\.\d+)Y([+-]?\d+\.\d+)(I([+-]?\d+\.\d+))?(J([+-]?\d+\.\d+))?"
    match = re.search(pattern, line)
    if match:
        x, y, _, i, _, j = match.groups()
        # x, y, i, j = match.groups()
        if i and j:
            return float(x), float(y), float(i), float(j)
        else:
            return float(x), float(y)
    return None


if __name__ == "__main__":
    line = "G03X+269.8Y-29.0I+264.2J-23.4"
    line2 = "G00X+264.2Y-23.4"
    resultado = get_coordinates(line)
    resultado2 = get_coordinates(line2)
    print(resultado)
    print(resultado2)
    # Output: (269.8, -29.0, 264.2, -23.4)
