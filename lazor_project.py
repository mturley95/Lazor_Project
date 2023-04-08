"""
Lazor Project
Carter Gaulke, Shri Shivram, Mitch Turley

This project will take an input file that represents a level from Lazor.
Lazor is a mobile puzzle game where the goal is to use blocks to redirect
the lazor to hit the targets. This project therefore solves the puzzle and
outputs what the solution would be for each specific level.
"""
# Imports
from tkinter import *

# Global Variable
X = 0
Y = 1

def openlazorfile(filename):
    '''
    This will open the bff file and output the components on the board.

    **Parameters**
        file: *str*
            Name of the file that needs to be opened

    **Returns**
        A series of lists containing the following:
            grid_list = list of numbers in the grid
            refl_block = list of number of reflect blocks
            opq_block = list of number of opaque blocks
            refr_block = list of number of refract blocks
            laz_start = list of lists with the starting position of the lazor
            target = list of lists with the targets that the lazor needs to hit
    '''

    grid_list = []
    refl_block = []
    opq_block = []
    refr_block = []
    num_refl_block = 0
    num_opq_block = 0
    num_refr_block = 0
    laz_data = []
    laz_count = 0
    laz_dict = {}
    target = []
    targets = []
    add_grid_to_list = False

    with open(filename, 'r') as file:

        for l in file:
            # print(l)
            if l.startswith("#"):
                continue

            if l.startswith(" "):
                continue

            elif l.startswith('GRID START'):
                for grid_line in file:
                    if grid_line.startswith('GRID STOP'):
                        break
                    grid_list.append(
                        [int(x) if x.isdigit() else x for x in grid_line.strip().split()])

            # print(grid_list)
            elif l.startswith("A"):
                refl_block = [int(x) for x in l.strip().split()[1:]]
                num_refl_block = int(refl_block[0])

            elif l.startswith("B"):
                opq_block = [int(x) for x in l.strip().split()[1:]]
                num_opq_block = int(opq_block[0])

            elif l.startswith("C"):
                refr_block = [int(x) for x in l.strip().split()[1:]]
                num_refr_block = int(refr_block[0])

            elif l.startswith("L"):
                laz_data = []
                laz_data.append(l.split()[1:])
                lazor_coor = (int(laz_data[0][0]), int(laz_data[0][1]))
                lazor_dir = (int(laz_data[0][2]), int(laz_data[0][3]))
                key = f"lazor{laz_count}"
                laz_dict[key] = [(lazor_coor[0], lazor_coor[1]),
                                 (lazor_dir[0], lazor_dir[1])]
                laz_count += 1

            elif l.startswith("P"):
                target.append(l.split()[1:])

    # converting the output from the loop into a int
    target = [[int(element) for element in inner_list]
              for inner_list in target]
    for i in target:
        targets.append(tuple(i))
    # print(grid_list)
    # print(grid_list[0][0])
    # print(type(grid_list[0][0]))
    # print(num_refl_block)
    # print(num_opq_block)
    # print(num_refr_block)
    # print(laz_dict)
    # # print(type(laz_start[0][0]))
    # print(targets)
    return grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets

## Block Creation
class Block:
    '''
    This class 
    '''

    # Initialize the Block class.
    def __init__(self, type='empty'):
        self.type = type
        self.grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        self.positions = []

    def get_type(self):
        return self.type

    def get_positions(self):
        return self.positions

    def set_position(self, new_position, new_grid):
        '''
        This function takes the desired position of the block and adds
        the values of this block into the grid

        **Parameters**
            new_position: *tuple*
                A tuple to hold the x and y coordinates of the new position
            new_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            new_grid: *list, list*
                The original grid with the updated values
        '''
        self.positions.append(new_position)
        grid_edit = self.grid
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit)):
                new_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] = \
                    grid_edit[y_index][x_index]
        return new_grid

    def remove_position(self, remove_position, new_grid):
        '''
        This function takes the desired position of the block and removes
        the values of this block into the grid

        **Parameters**
            old_position: *tuple*
                A tuple to hold the x and y coordinates of the old position
            new_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            new_grid: *list, list*
                The original grid with the updated values

        UPDATE:
        - Fix to make sure it doesn't overwrite values for a block next to it
        '''
        self.positions.remove(remove_position)
        grid_edit = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        grid_edit[1][1] = 100
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit)):
                new_grid[remove_position[Y]+y_index-1][remove_position[X]+x_index-1] = \
                    grid_edit[y_index][x_index]
        return new_grid
    
    def mirror_direction(self, lazor_direction, side_of_block):
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
            new_direction = (lazor_direction[0], lazor_direction[1] * -1)
        if side_of_block == 1 or side_of_block == 3:
            new_direction = (lazor_direction[0] * -1, lazor_direction[1])
        return new_direction

    def lazor(self, lazor_position, lazor_direction):
        new_direction = (lazor_direction[0], lazor_direction[1])
        new_position = (lazor_position[0] + new_direction[0],
                        lazor_position[1] + new_direction[1])
        return new_position, new_direction


class Open_Block(Block):

    empty_count = 0

    def __init__(self, type='open'):
        self.type = type
        self.positions = []
        open_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        open_grid[1][1] = 100
        self.grid = open_grid


class Reflect_Block(Block):

    reflect_count = 0

    def __init__(self, type='reflect'):
        self.type = type
        self.positions = []
        reflect_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        reflect_grid[0][1] = 10
        reflect_grid[1][0] = 11
        reflect_grid[2][1] = 10
        reflect_grid[1][2] = 11
        reflect_grid[1][1] = 1
        self.grid = reflect_grid

    def lazor(self, starting_grid, lazor_grid, lazor_position, lazor_direction):
        if starting_grid[lazor_position[0]][lazor_position[1]] == 10:
            lazor_grid[lazor_position[0]][lazor_position[1]] = 1
            new_direction = mirror_direction(lazor_direction, 1)
        if starting_grid[lazor_position[0]][lazor_position[1]] == 11:
            lazor_grid[lazor_position[0]][lazor_position[1]] = 1
            new_direction = mirror_direction(lazor_direction, 0)
        new_position = (lazor_position[0] + new_direction[0],
                        lazor_position[1] + new_direction[1])
        return new_position, new_direction


class Opaque_Block(Block):

    opaque_count = 0

    def __init__(self, type='opaque'):
        self.type = type
        self.positions = []
        reflect_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        reflect_grid[0][1] = 20
        reflect_grid[1][0] = 21
        reflect_grid[2][1] = 20
        reflect_grid[1][2] = 21
        reflect_grid[1][1] = 2
        self.grid = reflect_grid

    def lazor(self, lazor_position, lazor_direction):
        new_direction = (0, 0)
        new_position = lazor_position
        return new_position, new_direction


class Refract_Block(Block):
    '''
        A class that inherits the Block class
        Creates for the refract block

        **Parameters**
            None

        **Returns**
            None

        UPDATE:
        - Update set_position to not overwrite other blocks that are next to it
        '''
    def __init__(self, type='refract'):
        self.type = type
        self.positions = []
        reflect_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        reflect_grid[0][1] = 30
        reflect_grid[1][0] = 31
        reflect_grid[2][1] = 30
        reflect_grid[1][2] = 31
        reflect_grid[1][1] = 3
        self.grid = reflect_grid

    def lazor(self, starting_grid, lazor_grid, lazor_position, lazor_direction):
        new_direction_empty = (lazor_direction[0], lazor_direction[1])
        new_position_empty = (lazor_position[0] + new_direction[0],
                              lazor_position[1] + new_direction[1])

        if starting_grid[lazor_position[0]][lazor_position[1]] == 20:
            lazor_grid[lazor_position[0]][lazor_position[1]] = 1
            new_direction_reflect = mirror_direction(lazor_direction, 1)
        if starting_grid[lazor_position[0]][lazor_position[1]] == 21:
            lazor_grid[lazor_position[0]][lazor_position[1]] = 1
            new_direction_reflect = mirror_direction(lazor_direction, 0)
        new_position_reflect = (lazor_position[0] + new_direction_reflect[0],
                                lazor_position[1] + new_direction_reflect[1])

        return [new_position_empty, new_direction_empty, new_position_reflect, new_direction_reflect]

## Create initial grid from file
def create_grid(grid_list):
    x_count = 1
    y_count = 1
    new_grid = []
    grid_edit = []

    new_grid_width = len(grid_list[0]) * 2 + 1
    new_grid_height = len(grid_list) * 2 + 1
    new_grid = [['0' for i in range(new_grid_width)]
                for j in range(new_grid_height)]

    # Then, add the empty and open blocks
    for line in grid_list:
        for block in line:
            if block == 'o':
                empty_block = Open_Block((x_count, y_count))
                # grid_edit = empty_block.grid
                empty_block.set_position((x_count, y_count), new_grid)
                # for row in range(len(grid_edit)):
                #     for col in range(len(grid_edit[0])):
                #         new_grid[x_count+col-1][y_count+row-1] \
                #             = grid_edit[col][row]

            if block == 'x':
                closed_block = Block((x_count, y_count))
                closed_block.set_position((x_count, y_count), new_grid)
                # grid_edit = closed_block.grid
                # for row in range(len(grid_edit)):
                #     for col in range(len(grid_edit[0])):
                #         new_grid[x_count+col-1][y_count+row-1] \
                #             = grid_edit[col][row]
            x_count += 2
        x_count = 1
        y_count += 2

    # Then, add the refract blocks
    x_count = 1
    y_count = 1
    grid_edit = []

    for line in grid_list:
        for block in line:
            if block == 'C':
                refract_block = Refract_Block((x_count, y_count))
                refract_block.set_position((x_count, y_count), new_grid)
                # grid_edit = refract_block.grid
                # for row in range(len(grid_edit)):
                #     for col in range(len(grid_edit[0])):
                #         new_grid[x_count+col-1][y_count+row-1] \
                #             = grid_edit[col][row]
            x_count += 2
        x_count = 1
        y_count += 2

    # Then, add the reflect and opaque blocks
    x_count = 1
    y_count = 1
    # grid_edit = []

    for line in grid_list:
        for block in line:
            if block == 'A':
                reflect_block = Reflect_Block((x_count, y_count))
                reflect_block.set_position((x_count, y_count), new_grid)
                # grid_edit = reflect_block.grid
                # for row in range(len(grid_edit)):
                #     for col in range(len(grid_edit[0])):
                #         new_grid[x_count+col-1][y_count+row-1] \
                #             = grid_edit[col][row]
            if block == 'B':
                opaque_block = Opaque_Block((x_count, y_count))
                opaque_block.set_position((x_count, y_count), new_grid)
                # grid_edit = opaque_block.grid
                # for row in range(len(grid_edit)):
                #     for col in range(len(grid_edit[0])):
                #         new_grid[x_count+col-1][y_count+row-1] \
                #             = grid_edit[col][row]
            x_count += 2
        x_count = 1
        y_count += 2

    return new_grid

## Output visualization
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
        None

    UPDATE:
    - Add other colors and ability to place whatever block you want
    - Make drawing the blocks a function
        
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

    UPDATE:
    - Add the class functionality for interacting with the lazor

    '''
    size = len(starting_grid)
    lazor_path = [lazor_start]
    lazor_direction = [lazor_start_direction]
    lazor_grid = [
        [0 for i in range(size)]
        for j in range(size)
    ]
    lazor_grid[lazor_start[Y]][lazor_start[X]] = 1

    lazor_positions = []

    while len(lazor_path) > 0:
        current_position = lazor_path.pop()
        lazor_positions.append(current_position)
        current_direction = lazor_direction.pop()
        if not pos_chk(current_position[X], current_position[Y], size):
            continue
        ## Nothing is there
        if starting_grid[current_position[Y]][current_position[X]] == 0:
            lazor_grid[current_position[Y]][current_position[X]] = 1
            ## Update with class
            next_position = (current_position[X]+current_direction[X],
                             current_position[Y]+current_direction[Y])
            ##
            lazor_path.append(next_position)
            lazor_direction.append(current_direction)
        # Reflect Block
        if starting_grid[current_position[Y]][current_position[X]] == 10:
            lazor_grid[current_position[Y]][current_position[X]] = 1
            ## Update with class
            new_direction = mirror_direction(current_direction, 1)
            next_position = (current_position[X]+new_direction[X],
                             current_position[Y]+new_direction[Y])
            ##
            lazor_path.append(next_position)
            lazor_direction.append(new_direction)
        if starting_grid[current_position[Y]][current_position[X]] == 11:
            lazor_grid[current_position[Y]][current_position[X]] = 1
            ## Update with class
            new_direction = mirror_direction(current_direction, 0)
            next_position = (current_position[X]+new_direction[X],
                             current_position[Y]+new_direction[Y])
            ##
            lazor_path.append(next_position)
            lazor_direction.append(new_direction)
        # Opaque Block
        if starting_grid[current_position[Y]][current_position[X]] == 20:
            lazor_grid[current_position[Y]][current_position[X]] = 1
        if starting_grid[current_position[Y]][current_position[X]] == 21:
            lazor_grid[current_position[Y]][current_position[X]] = 1
        # Refract Block
        if starting_grid[current_position[Y]][current_position[X]] == 30:
            pass
        if starting_grid[current_position[Y]][current_position[X]] == 31:
            pass

    targets_results = []
    for i, target in enumerate(targets):
        if lazor_grid[target[Y]][target[X]] == 1:
            targets_results.append(True)
        else:
            targets_results.append(False)
    return lazor_grid, lazor_positions, targets_results

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

def solve_puzzle(space_positions, block_positions, start_coordinate,
                 target_coordinates, lazor_coordinates):
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

def print_matrix(input_list):
    '''
    This function prints a matrix on row at a time. Makes it easier to read.

    **Parameters**

        input_list: *list, list*
            A a list of lists to be printed

    **Returns**

    '''
    for rows in input_list:
        print(rows)

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

    # grid_test = [
    #     [0 for i in range(7)]
    #     for j in range(7)
    # ]

    # grid_test[3][0] = 11
    # grid_test[2][1] = 10
    # grid_test[3][1] = 1
    # grid_test[4][1] = 10
    # grid_test[3][2] = 11
    # grid_test[5][2] = 11
    # grid_test[4][3] = 10
    # grid_test[5][3] = 1
    # grid_test[6][3] = 10
    # grid_test[5][4] = 11

    # print(grid_test)

    # start_test = (1,6)
    # direction_test = (1,-1)
    # targets_test = [(2,3),(1,4)]

    ## The start of the level
    # win = Tk()
    # win.geometry("800x700")

    WIDTH_TEST = 300
    HEIGHT_TEST = WIDTH_TEST * 2

    MATRIX_SIZE_X_TEST = 3
    MATRIX_SIZE_Y_TEST = 3
    DIAMETER_TEST = 10

    # image_start = Canvas(win, width=WIDTH_TEST, height=HEIGHT_TEST, bg="grey")
    # image_start.grid(row=0,column=0)

    # # Create start of game
    # space_positions_test = [0,1,2,3,4,5,6,7,8]
    # block_positions_test = []
    # place_blocks(image_start, space_positions_test, block_positions_test,
    #              WIDTH_TEST, MATRIX_SIZE_X_TEST, MATRIX_SIZE_Y_TEST)

    # place_start_point(image_start, start_test,
    #                   WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # place_targets(image_start, targets_test,
    #               WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # ## Solve puzzle
    # # print(targets_test)
    # lazor_grid_results, targets_test_results = lazor(grid_test, start_test,
    #                                                  direction_test, targets_test)
    # # print(targets_test_results)
    # print(lazor_grid_results)
    # block_positions_test = [3,7]

    # ## Solve Button
    # image_button = Button(win, text="Solve Puzzle",
    #                       command=lambda: solve_puzzle(space_positions_test,block_positions_test,
    #                                                    start_test,targets_test,lazor_grid_results))
    # image_button.grid(row=0, column=1, padx=50)
    
    # win.mainloop()
    # test_start = (1, 6)
    # test_direction = (1, -1)
    # test_targets = [(2, 3), (1, 4)]

    # print(test_targets)
    # lazor_grid_results, test_targets_results = lazor(grid_test, test_start,
    #                                                  test_direction, test_targets)
    # print(test_targets_results)

    # mad_1 = openlazorfile('mad_1.bff')
    # mad_1_num_grid = create_grid(mad_1)
    # print(mad_1_num_grid)

    # mad_7 = openlazorfile('mad_7.bff')
    # mad_7_num_grid = create_grid(mad_7)
    # print(mad_7_num_grid)

    grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets = openlazorfile('tiny_5.bff')

    # print_matrix(grid_list)
    # print(num_refl_block)
    # print(num_opq_block)
    # print(num_refr_block)
    # print(laz_dict)
    # print(targets)

    # tiny_5 = openlazorfile('tiny_5.bff')[0]
    tiny_5_num_grid = create_grid(grid_list)
    # print(tiny_5_num_grid)
    print_matrix(tiny_5_num_grid)

    # lazor1 = laz_dict['lazor0']
    # print(lazor1)

    # grid, positions, results = lazor(tiny_5_num_grid, lazor1[0], lazor1[1], targets)
    # print_matrix(grid)
    # print(positions)
    # print(results)

    block = Refract_Block()
    print("\n")
    print_matrix(block.set_position((1,1), tiny_5_num_grid))
    print("\n")
    print_matrix(block.remove_position((1,1), tiny_5_num_grid))
