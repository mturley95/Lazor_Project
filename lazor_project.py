'''
Lazor Project
Carter Gaulke, Shri Shivram, Mitch Turley

This project will take an input file that represents a level from Lazor.
Lazor is a mobile puzzle game where the goal is to use blocks to redirect
the lazor to hit the targets. This project therefore solves the puzzle and
outputs what the solution would be for each specific level.
'''

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

    while len(lazor_path) > 0:
        current_position = lazor_path.pop()
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
    return lazor_grid, targets_results

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

    test_grid = [
        [0 for i in range(7)]
        for j in range(7)
    ]

    test_grid[3][0] = 11
    test_grid[2][1] = 10
    test_grid[3][1] = 1
    test_grid[4][1] = 10
    test_grid[3][2] = 11
    test_grid[5][2] = 11
    test_grid[4][3] = 10
    test_grid[5][3] = 1
    test_grid[6][3] = 10
    test_grid[5][4] = 11

    # print(test_grid)

    test_start = (1,6)
    test_direction = (1,-1)
    test_targets = [(2,3),(1,4)]

    print(test_targets)
    lazor_grid_results, test_targets_results = lazor(test_grid, test_start,
                                                     test_direction, test_targets)
    print(test_targets_results)
