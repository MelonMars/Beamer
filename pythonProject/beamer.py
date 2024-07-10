import numpy as np

"""
Syntax:
Code:
flags = [Negativity (false for positive, true for negative)]
Language:
F = Flashlight, start of program. Arrow next to it dictates position it is pointing in.
/ = Mirror, reflects the beam 90 degrees.
- = Mirror, reflects the beam 180 degrees.
N = flips the negative flag.
"""
program = ""
with open("program.beam", "r") as f:
    program = f.read()

pLines = program.splitlines()
max_length = max(len(line) for line in pLines)
paddedLines = [line.rjust(max_length) for line in pLines]
programArray = np.array([list(line) for line in paddedLines])
flashLightMask = np.isin(programArray, "F")
if True not in flashLightMask:
    raise SyntaxError("No flashlight found in program")
indices = np.argwhere(flashLightMask)
arrow, arrowIndex = " ", []

arrow_found = False
for index in indices:
    x, y = index
    subarray = programArray[x-1:x+2, y-1:y+2]  # Adjusted to get the 3x3 subarray centered on (x, y)
    if np.any(subarray == "F"):  # Ensure the flashlight is in the subarray
        adjacent_positions = {
            "^": (-1, 0),
            "v": (1, 0),
            ">": (0, 1),
            "<": (0, -1)
        }
        for symbol, (dx, dy) in adjacent_positions.items():
            if (1 + dx >= 0 and 1 + dx < 3) and (1 + dy >= 0 and 1 + dy < 3) and subarray[1 + dx, 1 + dy] == symbol:
                arrow_found = True
                arrow = symbol
                arrowIndex = [x + dx, y + dy]
                break
    if arrow_found:
        break


arrow=programArray[arrowIndex[0], arrowIndex[1]]
if arrow == " ":
    print(programArray)
    raise SyntaxError("No arrow found in flashlight")
direction = []
if arrow == "^":
    direction = [-1, 0]
elif arrow == "v":
    direction = [1, 0]
elif arrow == ">":
    direction = [0, 1]
elif arrow == "<":
    direction = [0, -1]

print(direction)
currentIndex = arrowIndex
rows, cols = programArray.shape
flags = [False]
while 0 <= x < rows + 1 and 0 <= y < cols + 1:
    x, y = currentIndex
    try:
        if programArray[x, y] == "/":
            if direction == [-1, 0]:
                direction = [0, 1]
            elif direction == [1, 0]:
                direction = [0, -1]
            elif direction == [0, 1]:
                direction = [-1, 0]
            elif direction == [0, -1]:
                direction = [1, 0]
        elif programArray[x, y] == "-":
            if direction == [-1, 0]:
                direction = [1, 0]
            elif direction == [1, 0]:
                direction = [-1, 0]
            elif direction == [0, 1]:
                direction = [0, -1]
            elif direction == [0, -1]:
                direction = [0, 1]
        if programArray[x, y] == "N":
            flags[0] = not flags[0]

        programArray[x, y] = "1"
        currentIndex = [x+direction[0], y+direction[1]]
    except IndexError as e:
        break

print(flags)
print("You're program has ended. Your result is 42.")

multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])

print(multiline_string)
