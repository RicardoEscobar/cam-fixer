""" Esta funcion me arma el recorrido de cada bloque como si fuesen poligonos para utilizar con Shapely  """
import re


def get_WKT(lines):
    """Get the coordinates from a list of cam file lines.

    Args:
        lines (list): A list of lines from a cam file.

    Returns:
        list: A list of tuples with the coordinates for each line.
    """
    polygon_coordinates = []
    pattern = r"G0[0123]X([+-]?\d+\.\d+)Y([+-]?\d+\.\d+)(I([+-]?\d+\.\d+))?(J([+-]?\d+\.\d+))?"

    for line in lines:
        match = re.search(pattern, line)
        if match:
            x, y, _, i, _, j = match.groups()
            polygon_coordinates.append((float(x), float(y)))

    return polygon_coordinates


if __name__ == "__main__":
    lines = [
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
    coordinates = get_WKT(lines)
    print(coordinates)