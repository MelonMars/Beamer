import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Run a program in the Beam language")
parser.add_argument("--program", help="The path to the program to run", type=str)
parser.add_argument("--programText", help="The text of the program to run", type=str)
parser.add_argument("--debug", help="Prints debug information", type=bool)
args = parser.parse_args()

if args.program is None and args.programText is None:
    raise ValueError("No program provided")

if args.program is not None and args.programText is not None:
    raise ValueError("Cannot provide both a program and program text")

program = ""

if args.program is not None:
    with open(args.program, "r") as f:
        program = f.read()
elif args.programText is not None:
    program = args.programText

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
    subarray = programArray[x - 1:x + 2, y - 1:y + 2]
    if np.any(subarray == "F"):
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
    if args.debug:
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
    def __init__(self, dir, position, nFlag=False, addFlag=False, addReg=[0], addIndex=0, divisionFlag=False,
                 multiplicationFlag=False, squareFlag=False, powerFlag=False, swapFlag=False):
        self.direction = dir
        self.position = position
        self.nFlag = nFlag
        self.addFlag = addFlag
        self.addReg = addReg
        self.addIndex = addIndex
        self.divisionFlag = divisionFlag
        self.multiplicationFlag = multiplicationFlag
        self.squareFlag = squareFlag
        self.powerFlag = powerFlag
        self.swapFlag = swapFlag

    def move(self, power=2):
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
                    if not self.nFlag:
                        self.addReg[self.addIndex] += int(programArray[x, y])
                        self.addFlag = False
                    else:
                        self.addReg[self.addIndex] -= int(programArray[x, y])
                        self.addFlag = False
                elif (programArray[x, y] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & (self.divisionFlag == True):
                    if not self.nFlag:
                        self.addReg[self.addIndex] /= int(programArray[x, y])
                        self.divisionFlag = False
                    else:
                        self.addReg[self.addIndex] //= int(programArray[x, y])
                        self.divisionFlag = False
                elif (programArray[x, y] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & (self.multiplicationFlag == True):
                    if not self.nFlag:
                        self.addReg[self.addIndex] *= int(programArray[x, y])
                        self.multiplicationFlag = False
                    else:
                        self.addReg[self.addIndex] *= -int(programArray[x, y])
                        self.multiplicationFlag = False
                elif (programArray[x, y] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & (self.squareFlag == True):
                    if not self.nFlag:
                        self.addReg[self.addIndex] **= int(programArray[x, y])
                        self.squareFlag = False
                    else:
                        self.addReg[self.addIndex] **= -int(programArray[x, y])
                        self.squareFlag = False
                elif (programArray[x, y] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) & (self.swapFlag == True):
                    self.addReg[self.addIndex], self.addReg[int(programArray[x, y])] = self.addReg[int(programArray[x, y])], self.addReg[self.addIndex]
                    self.swapFlag = False
                elif programArray[x, y] == ";":
                    self.addIndex += 1
                elif programArray[x, y] == ",":
                    self.addIndex -= 1
                elif programArray[x, y] == "!":
                    print(chr(self.addReg[self.addIndex]), end="")
                elif programArray[x, y] == "?":
                    while True:
                        self.addReg[self.addIndex] = int(input("Enter an integer number: "))
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
                    beam1 = Beam([self.direction[1], -self.direction[0]], self.position, self.nFlag, self.addFlag,
                                 self.addReg, self.addIndex, self.divisionFlag, self.multiplicationFlag, self.squareFlag, self.powerFlag, self.swapFlag)
                    beam2 = Beam([-self.direction[1], self.direction[0]], self.position, self.nFlag, self.addFlag,
                                 self.addReg, self.addIndex, self.divisionFlag, self.multiplicationFlag, self.squareFlag, self.powerFlag, self.swapFlag)
                    beams.append(beam1)
                    beams.append(beam2)
                elif programArray[x, y] == "C":
                    if len(beams) == 1:
                        print(f"You're program has ended. Your result is 42. Or possibly {self.addReg[self.addIndex]}")
                        multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])
                        if args.debug:
                            print(multiline_string)
                        beams.remove(self)
                    else:
                        beams.remove(self)
                elif programArray[x, y] == "D":
                    self.divisionFlag = True
                elif programArray[x, y] == "M":
                    self.multiplicationFlag = True
                elif programArray[x, y] == "*":
                    self.squareFlag = True
                elif programArray[x, y] == "Q":
                    beam1 = Beam([self.direction[1], -self.direction[0]], self.position, self.nFlag, self.addFlag,
                                 self.addReg, self.addIndex, self.divisionFlag, self.multiplicationFlag, self.squareFlag, self.powerFlag, self.swapFlag)
                    beam2 = Beam([-self.direction[1], self.direction[0]], self.position, self.nFlag, self.addFlag,
                                 self.addReg, self.addIndex, self.divisionFlag, self.multiplicationFlag, self.squareFlag, self.powerFlag, self.swapFlag)
                    beam3 = Beam(self.direction, self.position, self.nFlag, self.addFlag, self.addReg, self.addIndex, self.divisionFlag, self.multiplicationFlag, self.squareFlag, self.powerFlag, self.swapFlag)
                    beams.append(beam1)
                    beams.append(beam2)
                    beams.append(beam3)
                elif programArray[x, y] == "P":
                    self.powerFlag = True
                programArray[x, y] = "L"
                if self.powerFlag & power > 0:
                    if args.debug:
                        print("Power flag is on. Moving an extra time.")
                    self.move(power - 1)
            except IndexError as e:
                if len(beams) == 1:
                    print(f"You're program has ended. Your result is 42. Or possibly {self.addReg[self.addIndex]}")
                    multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])
                    if args.debug:
                        print(multiline_string)
                    del self
                else:
                    beams.remove(self)
                    del self
        else:
            if len(beams) == 1:
                print(f"You're program has ended. Your result is 42. Or possibly {self.addReg[self.addIndex]}")
                multiline_string = '\n'.join([' '.join(map(str, row)) for row in programArray])
                if args.debug:
                    print(multiline_string)
                beams.remove(self)
            else:
                beams.remove(self)


beam = Beam(direction, arrowIndex)
beams.append(beam)

while len(beams) > 0:
    np.random.shuffle(beams)
    for beam in beams:
        beam.move()
