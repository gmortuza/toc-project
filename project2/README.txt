# Project Name: Turing Machine Simulator and Busy Beaver finder
### Author: Golam Mortuza
### Course: CS 561
### Semester: Fall 2019

# Submitted file
tm.py --> Contains all the necessary code for this project

MainProj2.py --> A wrapper from tm.py. It calls the tm.py behind the seen.

README.txt --> This file. Contains the compiling instructions

BB1.txt --> Busy Beaver for State 1 symbol 3.

BB2.txt --> Busy Beaver for state 2 symbol 3.

BB3.txt --> Busy Beaver for state 3 symbol 3.

BB4.txt --> Busy Beaver for state 4 symbol 3.

# Compilation
The program is written in Python2.7

# Usage
```
python MainProj2.py [file_name]
```

# Input file format
The first line of the input file indicates the total number of states for the TM.
The second line of the input file indidcates the total number of symbols for the TM.
From the third line each line indicates a single transition. The transition will be in
the following format.

```next_state, write_symbol, move```

Where,

`next_state` --> The state that machine transits to.

`write_symbol` --> The symbol the machine will write to the cell.

`move` --> The direction either L or R to move the tape head to.