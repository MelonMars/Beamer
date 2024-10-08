```
     ***** **
  ******  ***
 **   *  * **
*    *  *  **
    *  *   *                                                    ***  ****
   ** **  *        ***       ****    *** **** ****       ***     **** **** *
   ** ** *        * ***     * ***  *  *** **** ***  *   * ***     **   ****
   ** ***        *   ***   *   ****    **  **** ****   *   ***    **
   ** ** ***    **    *** **    **     **   **   **   **    ***   **
   ** **   ***  ********  **    **     **   **   **   ********    **
   *  **     ** *******   **    **     **   **   **   *******     **
      *      ** **        **    **     **   **   **   **          **
  ****     ***  ****    * **    **     **   **   **   ****    *   ***
 *  ********     *******   ***** **    ***  ***  ***   *******     ***
*     ****        *****     ***   **    ***  ***  ***   *****
*
 **
``` 

An esoteric programming language

Syntax:
```
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
D = Division flag, sets the division flag to true. If negative flag is enabled for a division, it becomes a square route.
M = Multiplication flag, sets the multiplication flag to true.
* = Square flag. If the multiplication flag is on, then the number is squared when a number is hit by the beam.
Q = Quantum splitter. Like S, but instead of going in 2 directions, there's straight, 90 degrees to the right, and 90 degrees to the left.
P = Power. Makes the beam move an extra time each tick until the next power is hit.
X = Set the swap flag to true. If the swap flag is true when a number is hit, then that number is treated as an index in the addReg, and is swapped with the current addReg index.
```
Addition/Subtraction:
    - Addition works by having the addition flag being on. There is a default addition register, addReg[0]. addReg can grow in size. addReg[0] is originally set to 0. When the beam hits a number, if the addition flag is on, then that number is added to the current index in addReg. The index is contained in addIndex. If the negative flag is set to true, then until it is turned off, all additions are treated as subtractions.
Multiplication/Division:
    - Same as addition, even uses the addReg, but with a multiplication flag. Division is set by division flag.
Flags for numerical ops take precedence in the following order:
    - Addition
    - Division
    - Multiplication
    - Square
    - Swap
 
(e.g. if you have a Swap flag and an Addition flag both set to True, only the addition will be executed, and the swap flag will remain True.)

## To run:
To run first install `requirements.txt` and then run make a program, with whatever path and name you want. Then run `beamer.py` with the argument `--program` set to the path of the program you made.
