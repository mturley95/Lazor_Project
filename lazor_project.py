'''
Lazor Project
Carter Gaulke, Shri Shivram, Mitch Turley

This project will take an input file that represents a level from Lazor.
Lazor is a mobile puzzle game where the goal is to use blocks to redirect
the lazor to hit the targets. This project therefore solves the puzzle and
outputs what the solution would be for each specific level.
'''
# Imports
from tkinter import *

def place_blocks(canvas, space_positions, block_positions, width, matrix_size_x, matrix_size_y):
    '''
    This function places the blocks in the grid. It places both the spaces for blocks
    and the blocks themselves.

    **Parameters**

        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        space_positions: *list, tuple*
            A list of x,y coordinates in the grid where the spaces are
        block_positions: *list, tuple*
            A list of x,y coordinates in the grid where the blocks are
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
        matrix_size_y: *int*
            A value for the number of rows of spaces

    **Returns**
        
    '''
    box_size = width / (matrix_size_x*2)
    gap_between = (2*width/(matrix_size_x+1)) - (1*width/(matrix_size_x+1) + box_size)
    block_size = box_size + gap_between
    offset = 200

    count = 0
    for i in range(matrix_size_x):
        for j in range(matrix_size_y):
            if count in space_positions:
                x_location = ((i+1)*width/(matrix_size_x+1)) - (box_size/2)
                y_location = (j+1)*width/(matrix_size_x+1) - (box_size/2) + offset
                canvas.create_rectangle(x_location,y_location,
                                            x_location+box_size,y_location+box_size,
                                            fill="black")
            if count in block_positions:
                block_x_position = ((i+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                block_y_position = (j+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                canvas.create_rectangle(block_x_position,block_y_position,
                                            block_x_position+block_size,block_y_position+block_size,
                                            fill="tan")
            count += 1

def place_start_point(canvas, start, width, matrix_size_x, diameter):
    '''
    This function places the start of the lazor in the grid.

    **Parameters**

        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        start: *tuple*
            x,y coordinate in the grid where the lazor starts
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
       diameter: *int*
            A value for the diameter of the start lazor

    **Returns**
        
    '''
    radius= diameter / 2
    box_size = width / (matrix_size_x*2)
    gap_between = (2*width/(matrix_size_x+1)) - (1*width/(matrix_size_x+1) + box_size)
    block_size = box_size + gap_between
    offset = 200
    x_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius
    y_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius + offset

    start_x_position = x_size + (start[0]*(block_size/2))
    start_y_position = y_size + (start[1]*(block_size/2))
    canvas.create_oval(start_x_position,start_y_position,
                             start_x_position+diameter,start_y_position+diameter,
                             fill='red')

def place_targets(canvas, coordinates, width, matrix_size_x, diameter):
    '''
    This function places the targets for the lazor in the grid.

    **Parameters**

        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        coordinates: *list, tuple*
            A list of x,y coordinates in the grid where the targets are
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
        diameter: *int*
            A value for the diameter of the targets

    **Returns**
        
    '''
    radius= diameter / 2
    box_size = width / (matrix_size_x*2)
    gap_between = (2*width/(matrix_size_x+1)) - (1*width/(matrix_size_x+1) + box_size)
    block_size = box_size + gap_between
    offset = 200
    x_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius
    y_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius + offset

    for coordinate in coordinates:
        try:
            start_x_position = x_size + (coordinate[0]*(block_size/2))
            start_y_position = y_size + (coordinate[1]*(block_size/2))
            canvas.create_oval(start_x_position,start_y_position,
                                    start_x_position+diameter,start_y_position+diameter,
                                    fill='grey')
        except:
            pass

def draw_lazor(canvas, coordinates, width, matrix_size_x, diameter):
    '''
    This function draws the lazor in the grid.

    **Parameters**

        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        coordinates: *list, tuple*
            A list of x,y coordinates in the grid where the lazor travels
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
        diameter: *int*
            A value for the diameter of the targets

    **Returns**
        
    '''
    radius = diameter / 2
    box_size = width / (matrix_size_x*2)
    gap_between = (2*width/(matrix_size_x+1)) - (1*width/(matrix_size_x+1) + box_size)
    block_size = box_size + gap_between
    offset = 200
    x_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius
    y_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius + offset

    for i, coordinate in enumerate(coordinates):
        try:
            start_x_position = x_size + (coordinate[0]*(block_size/2))
            start_y_position = y_size + (coordinate[1]*(block_size/2))
            end_x_position = x_size + (coordinates[i+1][0]*(block_size/2))
            end_y_position = y_size + (coordinates[i+1][1]*(block_size/2))
            canvas.create_line(start_x_position+radius,start_y_position+radius,
                                    end_x_position+radius,end_y_position+radius,
                                    fill='red',width=3)
        except:
            pass

def lazor(starting_grid, lazor_start, lazor_start_direction, targets):
    '''
    This function takes the grid of the current status of the blocks and tracks the lazor
    to see if it reaches the target.

    **Parameters**

        starting_grid: *list, list, int*
            A list of lists holding what blocks and targets are in the grid
            This grid will be tested as a solution.
        lazor_start: *tuple*
            An x,y coordinate in the grid where the lazor starts
        lazor_direction: *tuple*
            Two vectors showing which direction the lazor starts
        targets: *list, tuple*
            A list of tuples which includes the coordinates of the targets

    **Returns**
        lazor_grid: *list, list, int*
            A list of lists holding the values for the grid
            This grid holds the information where the lazor traveled
        targets_results: *list, str*
            A list showing if all the targets were hit by the lazor

    '''
    size = len(starting_grid)
    lazor_path = [lazor_start]
    lazor_direction = [lazor_start_direction]
    lazor_grid = [
        [0 for i in range(size)]
        for j in range(size)
    ]
    lazor_grid[lazor_start[0]][lazor_start[1]] = 1

    lazor_positions = []

    while len(lazor_path) > 0:
        current_position = lazor_path.pop()
        lazor_positions.append(current_position)
        current_direction = lazor_direction.pop()
        if not pos_chk(current_position[0],current_position[1], size):
            continue
        ## Nothing is there
        if starting_grid[current_position[0]][current_position[1]] == 0:
            lazor_grid[current_position[0]][current_position[1]] = 1
            next_position = (current_position[0]+current_direction[0],
                             current_position[1]+current_direction[1])
            lazor_path.append(next_position)
            lazor_direction.append(current_direction)
        ## Reflect Block
        if starting_grid[current_position[0]][current_position[1]] == 10:
            lazor_grid[current_position[0]][current_position[1]] = 1
            new_direction = mirror_direction(current_direction, 1)
            next_position = (current_position[0]+new_direction[0],
                             current_position[1]+new_direction[1])
            lazor_path.append(next_position)
            lazor_direction.append(new_direction)
        if starting_grid[current_position[0]][current_position[1]] == 11:
            lazor_grid[current_position[0]][current_position[1]] = 1
            new_direction = mirror_direction(current_direction, 0)
            next_position = (current_position[0]+new_direction[0],
                             current_position[1]+new_direction[1])
            lazor_path.append(next_position)
            lazor_direction.append(new_direction)
        ## Opaque Block
        if starting_grid[current_position[0]][current_position[1]] == 20:
            lazor_grid[current_position[0]][current_position[1]] = 1
        if starting_grid[current_position[0]][current_position[1]] == 21:
            lazor_grid[current_position[0]][current_position[1]] = 1
        ## Refract Block
        if starting_grid[current_position[0]][current_position[1]] == 30:
            pass
        if starting_grid[current_position[0]][current_position[1]] == 31:
            pass

    targets_results = []
    for i, target in enumerate(targets):
        if lazor_grid[target[0]][target[1]] == 1:
            targets_results.append(True)
        else:
            targets_results.append(False)
    return lazor_positions, targets_results

def mirror_direction(direction, side_of_block):
    '''
    This function takes the direction of the lazor and flips it depending
    on which side of the block it hits

    **Parameters**
        direction: *tuple*
            A tuple to hold the two vectors for the direction of the lazor
        side of block: *int*
            An integer denoting the side of the block
                0 = top/bottom
                1 = left/right

    **Returns**
        new_direction: *tuple*
            A tuple for the new direction of the lazor
    '''
    if side_of_block == 0 or side_of_block == 2:
        new_direction = (direction[0], direction[1] * -1)
    if side_of_block == 1 or side_of_block == 3:
        new_direction = (direction[0] * -1, direction[1])
    return new_direction

def pos_chk(x_position, y_position, size):
    '''
    Validate if the coordinates specified (x and y) are within the grid.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the maze.
        y: *int*
            A y coordinate to check if it resides within the maze.
        size: *int*
            How many blocks wide the grid is.  Should be equivalent to
            the length of the grid (ie. len(grid)).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''
    return x_position >= 0 and x_position < size and y_position >= 0 and y_position < size

def solve_puzzle(space_positions, block_positions, start_coordinate, target_coordinates, lazor_coordinates):
    '''
    Draws the lazor
    '''
    WIDTH_TEST = 300
    HEIGHT_TEST = WIDTH_TEST * 2

    MATRIX_SIZE_X_TEST = 3
    MATRIX_SIZE_Y_TEST = 3
    DIAMETER_TEST = 10

    image_solution = Canvas(win, width=WIDTH_TEST, height=HEIGHT_TEST, bg="grey")
    image_solution.grid(row=0,column=2)

    # space_positions = [0,1,3,5,7,8,10]
    # block_positions = [3,7]
    place_blocks(image_solution, space_positions, block_positions,
                 WIDTH_TEST, MATRIX_SIZE_X_TEST, MATRIX_SIZE_Y_TEST)

    #start_coordinates = [(1,6)]
    place_start_point(image_solution, start_coordinate,
                      WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # target_coordinates_test = [(2,3)]
    place_targets(image_solution, target_coordinates,
                  WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # lazor_coordinates = [(1,6), (2,5), (3,4), (4,3), (3,2), (2,3), (1,4), (0,5)]
    draw_lazor(image_solution, lazor_coordinates,
               WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

if __name__ == '__main__':
    # Reflect block = 1
    # Opaque block = 2
    # Left, Right = X0
    # Top, Bottom = X1
    # grid = 0 ,0 ,0 ,11,0 ,0 ,0
    #        0 ,0 ,10,1 ,10,0 ,0
    #        0 ,0 ,0 ,11,0 ,21,0
    #        0 ,0 ,0 ,0 ,20,2 ,20
    #        0 ,0 ,0 ,0 ,0 ,21,0
    #        0 ,0 ,0 ,0 ,0 ,0 ,0

    grid_test = [
        [0 for i in range(7)]
        for j in range(7)
    ]

    grid_test[3][0] = 11
    grid_test[2][1] = 10
    grid_test[3][1] = 1
    grid_test[4][1] = 10
    grid_test[3][2] = 11
    grid_test[5][2] = 11
    grid_test[4][3] = 10
    grid_test[5][3] = 1
    grid_test[6][3] = 10
    grid_test[5][4] = 11

    # print(test_grid)

    start_test = (1,6)
    direction_test = (1,-1)
    targets_test = [(2,3),(1,4)]

    ## The start of the level
    win = Tk()
    win.geometry("800x700")

    WIDTH_TEST = 300
    HEIGHT_TEST = WIDTH_TEST * 2

    MATRIX_SIZE_X_TEST = 3
    MATRIX_SIZE_Y_TEST = 3
    DIAMETER_TEST = 10

    image_start = Canvas(win, width=WIDTH_TEST, height=HEIGHT_TEST, bg="grey")
    image_start.grid(row=0,column=0)

    # Create start of game
    space_positions_test = [0,1,2,3,4,5,6,7,8]
    block_positions_test = []
    place_blocks(image_start, space_positions_test, block_positions_test,
                 WIDTH_TEST, MATRIX_SIZE_X_TEST, MATRIX_SIZE_Y_TEST)

    place_start_point(image_start, start_test,
                      WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    place_targets(image_start, targets_test,
                  WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    ## Solve puzzle
    # print(targets_test)
    lazor_grid_results, targets_test_results = lazor(grid_test, start_test,
                                                     direction_test, targets_test)
    # print(targets_test_results)
    print(lazor_grid_results)
    block_positions_test = [3,7]

    ## Solve Button
    image_button = Button(win, text="Solve Puzzle",
                          command=lambda: solve_puzzle(space_positions_test,block_positions_test,
                                                       start_test,targets_test,lazor_grid_results))
    image_button.grid(row=0, column=1, padx=50)

    win.mainloop()
