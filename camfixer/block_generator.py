"""This module contains the function to get the text that defines a block from a cam file.
"""


def block_generator(cam_file):
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
    }

    Args:
        cam_file (str): The path to the cam file.

    Yields:
        str: The text that defines a block from a cam file.
    """
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
            # Gets the previous two lines.
            block_start = lines[i - 2 : i + 1]
            # Gets the next two lines.
            block_arc = lines[i + 1 : i + 3]
            block_main_start = i + 3
        if line == "M03" and lines[i + 1] == "G40":
            # Gets the next two lines.
            block_end = lines[i : i + 2]
            # Inverts the order of the block_main list.
            block_main.reverse()
            # Joins the lines and yields the block.
            text = "\n".join(block_start + block_arc + block_main + block_end)
            result = {
                "start": block_start,
                "arc": block_arc,
                "main": block_main,
                "end": block_end,
                "text": text,
            }
            yield result
            # Resets the block variables.
            block_start = []
            block_arc = []
            block_main = []
            block_end = []
            block_main_start = 0
        elif block_main_start > 0 and i >= block_main_start:
            block_main.append(line)


if __name__ == "__main__":
    cam_file = "archivo.cam"
    for block in block_generator(cam_file):
        print(block)
        print("-" * 80)
