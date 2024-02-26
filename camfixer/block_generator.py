"""This module contains the function to get the text that defines a block from a cam file.

from camfixer.get_max_min import get_max_min
"""

from camfixer.is_piece_two import is_piece_two
from camfixer.get_WKT import get_WKT

def _block_generator(cam_file):
    """This generator function yields the text that defines blocks from a cam file.
    The start of a block is defined by the line "M04" and the previous two lines, ignoring empty white lines.
    The arc of the block is defined by the next two lines after the start of the block.
    Anything between the arc and end of a block is considered the block.
    The end of a block is defined by the line "M03" and the next line "G40", ignoring empty white lines.

    example file:
    BOF
    G90
    G00X+226.2Y-8.2
    G00X+264.2Y-23.4
    G41
    M04
    G01X+258.5Y-29.0
    G03X+269.8Y-29.0I+264.2J-23.4
    G01X+276.0Y-22.8
    G02X+346.7Y-22.8I+311.4J-58.2
    G01X+371.5Y-47.6
    G02X+392.2Y-81.4I+311.4J-107.7
    G01X+502.9Y-422.0
    G02X+490.7Y-472.8I+455.3J-437.5
    G01X+428.8Y-534.7
    G03X+417.2Y-553.0I+464.2J-570.0
    G01X+391.3Y-624.5
    G02X+226.4Y-595.6I+311.4J-595.6
    G01X+226.4Y-107.7
    G02X+251.3Y-47.6I+311.4J-107.7
    G01X+263.6Y-35.2
    G01X+269.8Y-29.0
    M03
    G40

    Output:
    {
        'start': ['G00X+264.2Y-23.4', 'G41', 'M04'],
        'arc': ['G01X+258.5Y-29.0', 'G03X+269.8Y-29.0I+264.2J-23.4'],
        'main': ['G01X+269.8Y-29.0', 'G01X+263.6Y-35.2', 'G02X+251.3Y-47.6I+311.4J-107.7', 'G01X+226.4Y-107.7', 'G02X+226.4Y-595.6I+311.4J-595.6', 'G01X+391.3Y-624.5', 'G03X+417.2Y-553.0I+464.2J-570.0', 'G01X+428.8Y-534.7', 'G02X+490.7Y-472.8I+455.3J-437.5', 'G01X+502.9Y-422.0', 'G02X+392.2Y-81.4I+311.4J-107.7', 'G01X+371.5Y-47.6', 'G02X+346.7Y-22.8I+311.4J-58.2', 'G01X+276.0Y-22.8'],
        'end': ['M03', 'G40'],
        'text': 'G00X+264.2Y-23.4\nG41\nM04\nG01X+258.5Y-29.0\nG03X+269.8Y-29.0I+264.2J-23.4\nG01X+269.8Y-29.0\nG01X+263.6Y-35.2\nG02X+251.3Y-47.6I+311.4J-107.7\nG01X+226.4Y-107.7\nG02X+226.4Y-595.6I+311.4J-595.6\nG01X+391.3Y-624.5\nG03X+417.2Y-553.0I+464.2J-570.0\nG01X+428.8Y-534.7\nG02X+490.7Y-472.8I+455.3J-437.5\nG01X+502.9Y-422.0\nG02X+392.2Y-81.4I+311.4J-107.7\nG01X+371.5Y-47.6\nG02X+346.7Y-22.8I+311.4J-58.2\nG01X+276.0Y-22.8\nM03\nG40'
        'max_min': {'max_x': 502.9, 'min_x': 226.4, 'max_y': -22.8, 'min_y': -624.5}
    }

    Args:
        cam_file (str): The path to the cam file.

    Yields:
        dict: The dict that defines a block from a cam file.
    """
    coordinates = []
    block_initial = []
    block_start = []
    block_arc = []
    block_main = []
    block_end = []
    block_main_start = 0
    with open(cam_file, "r", encoding="utf-8") as file:
        cam_text = file.read()

    # Gets the lines from the cam file.
    lines = cam_text.split("\n")
    # Removes empty lines.
    lines = list(filter(None, lines))
    # Iterates over the lines.
    for i, line in enumerate(lines):
        if line == "M04":
            # Gets the initial coordinate of the arc.
            block_initial = [lines[i - 2]]
            # Gets the previous two lines.
            block_start = lines[i - 1 : i + 1]
            # Gets the next two lines.
            block_arc = lines[i + 1 : i + 3]
            block_main_start = i + 3
        if line == "M03" and lines[i + 1] == "G40":
            # Gets the next two lines.
            block_end = lines[i : i + 2]
            """ # Gets the maximum and minimum coordinates of the block.
            max_min = get_max_min(block_main)
            """
            # Joins the lines and yields the block.
            text = "\n".join(block_initial + block_start + block_arc + block_main + block_end)
            coordinates = get_WKT(block_main)
            result = {
                "initial":block_initial,
                "start": block_start,
                "arc": block_arc,
                "main": block_main,
                "end": block_end,
                "text": text,
                "polygon": coordinates,
            }
            """
                "max_min": max_min,
            """            
            yield result
            # Resets the block variables.
            block_initial = []
            block_start = []
            block_arc = []
            block_main = []
            block_end = []
            block_main_start = 0
        elif block_main_start > 0 and i >= block_main_start:
            block_main.append(line)


def block_generator(cam_file):
    """This function process each block separately to calculate maximum and minimum coordinates.
    Args:
        cam_file (str): The path to the cam file.
    Returns:
        List[Dict]: A list of dictionaries with the data of the blocks.
    """
    block_gen = _block_generator(cam_file)
    blocks = list(block_gen)
    for block in blocks:
        # Sets the is_piece key of the block dictionary.
        block["is_piece"] = is_piece_two(block, blocks)

        if not block["is_piece"]:
            # There is no arc if the block is a piece. So, move the arc to the
            # main block.
            block["main"] = block["arc"] + block["main"]
            block["arc"] = []
            """
            # Recalculate the maximum and minimum coordinates.
            block["max_min"] = get_max_min(block["main"])
            """
        else:
            # The block is not a piece. So, replace the "G02" with "G03" in the
            # main block.
            block["main"] = [line.replace("G02", "G03") for line in block["main"]]

        # # Reverse the main block list.
        # block["main"].reverse()

        # Remake 'text' key.
        # Joins the lines and yields the block.
        block["text"] = "\n".join(block["initial"] + block["start"] + block["arc"] + block["main"] + block["end"])

        yield block


if __name__ == "__main__":
    cam_file = "archivo.cam"
    for block in block_generator(cam_file):
        print(block)
        print("-" * 80)
