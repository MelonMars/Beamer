import numpy as np

"""
Syntax:
Code:
flags = [Negativity (false for positive, true for negative)]
Language:
F = Flashlight, start of program. Arrow next to it dictates position it is pointing in.
/ = Mirror, reflects the beam 90 degrees.
\ = Mirror, reflects the beam 270 degrees.
- = Mirror, reflects the beam 180 degrees.
N = flips the negative flag.
1 = Beam Path (Currently)
+ = Sets the addition flag to true. Addition flag is changed to false upon an addition.
; = Adds 1 to the addition index.
, = Subtracts 1 from the addition index.
0-9 = Adds the number to the addition register at additionIndex, if the addition flag is true.
? = Ask for input.
! = Output of the addition index at addition register, in ascii from the number.
# = Increase addition register size by 1.
S = Beam splitter, splits the beam into two beams. One beam goes 90 degrees to the right, the other goes 90 degrees to the left.
C = Camera, the first beam after a split that hits it is eliminated.
Addition/Subtraction:
    Addition works by having the addition flag being on. There is a default addition register, addReg[0]. addReg can grow in size. addReg[0] is originally set to 0. When the beam hits a number, if the addition flag is on, then that number is added to the current index in addReg. The index is contained in addIndex. If the negative flag is set to true, then until it is turned off, all additions are treated as subtractions.
"""

program = ""
with open("program.beam", "r") as f:
    program = f.read()

pLines = program.splitlines()
max_length = max(len(line) for line in pLines)
paddedLines = [line.ljust(max_length) for line in pLines]
programArray = np.array([list(line) for line in paddedLines])
flashLightMask = np.isin(programArray, "F")
if True not in flashLightMask:
    raise SyntaxError("No flashlight found in program")
indices = np.argwhere(flashLightMask)
arrow, arrowIndex = " ", []

arrow_found = False
for index in indices:
    x, y = index
    subarray = programArray[x - 1:x + 2, y - 1:y + 2]  # Adjusted to get the 3x3 subarray centered on (x, y)
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

arrow = programArray[arrowIndex[0], arrowIndex[1]]
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

rows, cols = programArray.shape
beams = []

class Beam:
    def __init__(self, dir, position, nFlag=False, addFlag=False, addReg=[0], addIndex=0):
        self.direction = dir
        self.position = position
        self.nFlag = nFlag
        self.addFlag = addFlag
        self.addReg = addReg
        self.addIndex = addIndex


    def move(self):
        self.position = [self.position[0] + self.direction[0], self.position[1] + self.direction[1]]
        x, y = self.position
        if 0 <= x < rows + 1 and 0 <= y < cols + 1:
            try:
                if programArray[x, y] == "/":
                    if self.direction == [-1, 0]:
                        self.direction = [0, 1]
                    elif self.direction == [1, 0]:
                        self.direction = [0, -1]
                    elif self.direction == [0, 1]:
                        self.direction = [-1, 0]
                    elif self.direction == [0, -1]:
                        self.direction = [1, 0]
                elif programArray[x, y] == "-":
                    if self.direction == [-1, 0]:
                        self.direction = [1, 0]
                    elif self.direction == [1, 0]:
                        self.direction = [-1, 0]
                    elif self.direction == [0, 1]:
                        self.direction = [0, -1]
                    elif self.direction == [0, -1]:
                        self.direction = [0, 1]
                if programArray[x, y] == "N":
                    self.nFlag = not self.nFlag
                elif programArray[x, y] == "+":
                    self.addFlag = True
                elif (programArray[x, y] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & (self.addFlag == True):
                    self.addReg[self.addIndex] += int(programArray[x, y])
                    self.addFlag = False
                elif programArray[x, y] == ";":
                    self.addIndex += 1
                elif programArray[x, y] == ",":
                    self.addIndex -= 1
                elif programArray[x, y] == "!":
                    print(chr(self.addReg[self.addIndex]), end="")
                elif programArray[x, y] == "?":
                    while True:
                        self.addReg[self.addIndex] = int(input("Enter a number: "))
                        try:
                            int(self.addReg[self.addIndex])
                            break
                        except ValueError:
                            print("Please enter a number.")
                elif programArray[x, y] == "#":
                    self.addReg.append(0)
                elif programArray[x, y] == "\\":
                    if self.direction == [-1, 0]:
                        self.direction = [0, -1]
                    elif self.direction == [1, 0]:
                        self.direction = [0, 1]
                    elif self.direction == [0, 1]:
                        self.direction = [1, 0]
                    elif self.direction == [0, -1]:
                        self.direction = [-1, 0]
                elif programArray[x, y] == "S":
                    beam1 = Beam([self.direction[1], -self.direction[0]], self.position, self.nFlag, self.addFlag, self.addReg, self.addIndex)
                    beam2 = Beam([-self.direction[1], self.direction[0]], self.position, self.nFlag, self.addFlag, self.addReg, self.addIndex)
                    beams.append(beam1)
                    beams.append(beam2)
                programArray[x, y] = "L"
                self.position = [x + self.direction[0], y + self.direction[1]]
            except IndexError as e:
                if len(beams) == 1:
                    print("You're program has ended. Your result is 42.")
                    multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])
                    print(multiline_string)
                    del self
                else:
                    beams.remove(self)
                    del self
        else:
            if len(beams) == 1:
                print("You're program has ended. Your result is 42.")
                multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])
                print(multiline_string)
                del self
            else:
                beams.remove(self)
                del self


beam = Beam(direction, arrowIndex)
beams.append(beam)

while len(beams) > 0:
    for beam in beams:
        print(len(beams))
        beam.move()

