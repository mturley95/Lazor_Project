# Lazor_Project
For collaborative work on the lazor project.
A Software Carpentry class group project that mimics the functionality
of the "Lazors" game found for IOS.

## Table of Contents
- [Lazor\_Project](#lazor_project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Technologies](#technologies)
    - [Libraries](#libraries)
  - [Launch](#launch)
  - [Features](#features)
  - [Status](#status)
    - [Future work:](#future-work)

## Introduction
This project mimics the "Lazors" game found on IOS.
It imports a text file formatted as a ".bff" file type and creates a starting grid composed of the starting positions of different blocks, lazors, and targets that the lazors need to hit in order for the puzzle to be solve. 

The code visualizes the starting grid and then solves the puzzle, visualizing the solved grid and saving it as a ".png" image file of the same name as the original file.

## Technologies
Project is created with:
* Python 3.10

### Libraries
Project used the following libraries:
* tkinter
* itertools
* copy
* os
* tkcap

## Launch
To run this project, open lazor_project.py and run the code using Python 3.10.

Once the code is running, a window will pop up. First, enter the name of the file of a ".bff" filetype that needs to be read that contains information for the puzzle. For example, "mad_1.bff". 

Then, click "Display Puzzle". This button will display the starting puzzle board on the left display panel with all pre-populated blocks in place; the starting lazor location, direction, and path; and the location of the targets that the puzzle needs to be hit in order to be solved.

Once the puzzle has been displayed, click "Solve Puzzle" in order to solve the puzzle. This will populated the available blocks that need to be placed onto the puzzle in a position that causes all lazor targets to be contacted by the lazor path. Once the solution has been calculated, it will be displayed on the right panel with the block positions and final lazor path. An image of the same name as the original file will be saved as a ".png" filetype displaying the window with the starting puzzle on the left and the puzzle solution on the right. For example, "mad_1.png" will be saved for the "mad_1.bff" initial file.

## Features
Supported block types:
* Empty blocks
  * These blocks allow the lazor to pass through undisturbed and also allow new blocks to be placed in their spaces.
* Closed blocks
  * These blocks allow the lazor to pass through undisturbed and prevent new blocks from being placed in their spaces.
* Reflect blocks
  * These blocks reflect the lazor path as if they were a mirror.
* Opaque blocks
  * These blocks do not allow the lazor to pass through and end its trajectory.
* Refract blocks
  * These blocks both reflect the lazor path as if they were a mirror and allow the lazor to pass through undisturbed, effectively creating two lazor paths from the inital lazor input.

## Status
This release allows the for lazor puzzle to be input and solved, calculating and displaying the solution to the puzzle and saving it as a PNG image.

### Future work:
* Add functionality to the Gui to allow the user to place and move available blocks to attempt to solve the puzzle themselves.
* Continue to optimize the solve_puzzle function to improve its efficiency with more complex puzzles.

