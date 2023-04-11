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
import itertools
import copy
import pyautogui as pg
from PIL import Image

# Global Variables
X = 0
Y = 1

# Block Creation


class Block:
    '''
    This class is used to create block objects to populate the grid with. They will interact
    with the grid and the lazor in different ways as they are positioned on the grid.

    **Functions**
        __init__(self, type='empty'):
            Initializes the block object.
            Return: None
        get_type(self):
            Returns the type of block that exists at a specific position.
            Return self.type: *str*
        get_positions(self):
            Returns the different positions where the block object exists on the grid.
            Return self.positions: *list* of tuples
        set_position(self, new_position, new_grid):
            Takes the desired position of the block and adds the values of this block into the grid. 
            It ignores spaces where blocks are already present.
            It adds the position to the block's list of positions.
            Return new_grid: *list*
        remove_position(self, remove_position, new_grid):
            Takes the position of a block to be removed and resets the values of the block in the grid.
            It ensures all adjacent blocks have their values maintained.
            It removes the position from the block's list of positions.
            Return new_grid: *list*
        mirror_direction(self, lazor_direction, side_of_block):
            This function takes the direction of the lazor as it begins interacting with a block and 
            flips it depending on which side of the block it hits.
            Return new_direction: *tuple*
        interact_lazor(self, lazor_position, lazor_direction):
            This function calculates the new position and direction of the lazor based on how the block
            interacts with the lazor.
            Return new_position, new_direction: *tuple*, *tuple*

    **Sub-Classes**
        Open_Block:
            Creates blocks that are empty and open for other blocks to be placed in their positions.
        Reflect_Block:
            Creates blocks that reflect the lazor when it comes into contact.
        Opaque_Block:
            Creates blocks that absorb the lazor when it comes into contact.
        Refract_Block:
            Creates blocks that both reflect the lazor and allows it to pass through when it comes into contact.
    '''

    # Initialize the Block class.
    def __init__(self):
        '''
        This function initializes the Block class object. It performs the following functions:
            self.type: Assigns its type.
            self.grid: Creates its 3x3 grid of elements that determine how the lazor will interact with it.
            self.positions: Generates an empty position list.

        **Parameters**
            N/A

        **Returns**
            N/A
        '''
        # Initialize the type as empty
        self.type = 'empty'
        # Initialize the grid with 0's
        self.grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        # Initialize the positions list
        self.positions = []

    def get_type(self, position):
        '''
        This function returns the type of block that exists at a specific position.

        **Parameters**
            position: *tuple*
                A tuple to hold the x and y coordinates of the position that is being checked

        **Returns**
            self.type: *str*
                The type of block that exists at that position
        '''
        # Iterate through the positions
        for i in self.positions:
            # Returns the type at the positions
            if i == position:
                return self.type

    def get_positions(self):
        '''
        This function returns the the positions of the block object that have been assigned to the grid.

        **Parameters**
            N/A

        **Returns**
            self.positions: *list* of tuples
                The positions on the grid that the block object exists at
        '''
        # Return the positions
        return self.positions

    def set_position(self, new_position, num_grid):
        '''
        This function takes the desired position of the block and adds the values of this block into the grid. 
            It ignores spaces where block values are already present.
            It adds the position to the block's list of positions.

        **Parameters**
            new_position: *tuple*
                A tuple to hold the x and y coordinates of the new position
            num_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            num_grid: *list, list*
                The original grid with the updated values
        '''

        # Add the new position to the block's list of positions.
        self.positions.append(new_position)

        # Modify the original grid by adding the block's
        # unique grid of numbers to the position specified.
        grid_edit = self.grid
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit[y_index])):
                # Only overwrites the grid numbers for open spaces.
                if num_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] == 0 or \
                        num_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] == 100:
                    num_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] = \
                        grid_edit[y_index][x_index]

        # Return the new grid with the modified block values.
        return num_grid

    def remove_position(self, remove_position, num_grid):
        '''
        This function takes the position of a block to be removed and resets the values of the block in the grid.
            It ensures all adjacent blocks have their values maintained.
            It removes the position from the block's list of positions.

        **Parameters**
            remove_position: *tuple*
                A tuple to hold the x and y coordinates of the old position
            num_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            num_grid: *list, list*
                The original grid with the updated values
        '''

        # Add the specified position from the block's list of positions.
        self.positions.remove(remove_position)

        # Modify the original grid by removing the block's unique grid of numbers from the position specified.
        size = (len(num_grid[0]), len(num_grid))
        # Initialize the grid as 0's
        grid_edit = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        # Initialize the middle of the grid as 100
        grid_edit[1][1] = 100
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit[y_index])):
                num_grid[remove_position[Y]+y_index-1][remove_position[X]+x_index-1] = \
                    grid_edit[y_index][x_index]

                # Check neighboring blocks and ensure their values are replaced on the grid for positions
                # shared by the block that is being removed.

                # Check above the block being removed.
                if y_index-1 == -1 and x_index-1 == 0:

                    # Identify adjacent block type and position.
                    adj_block = num_grid[remove_position[Y] +
                                         y_index-2][remove_position[X]+x_index-1]
                    adj_block_pos = (
                        remove_position[X]+x_index-1, remove_position[Y]+y_index-2)

                    # Check to ensure adjacent block is on the grid.
                    if not pos_chk(adj_block_pos, size):
                        continue

                    # Check adjacent block type and replace value to removed space.
                    if adj_block == 100:
                        empty_block = Open_Block()
                        empty_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 0:
                        closed_block = Block()
                        closed_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 1:
                        reflect_block = Reflect_Block()
                        reflect_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 2:
                        opaque_block = Opaque_Block()
                        opaque_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 3:
                        refract_block = Refract_Block()
                        refract_block.set_position(adj_block_pos, num_grid)

                # Check to the left of the block being removed.
                if y_index-1 == 0 and x_index-1 == -1:

                    # Identify adjacent block type and position.
                    adj_block = num_grid[remove_position[Y] +
                                         y_index-1][remove_position[X]+x_index-2]
                    adj_block_pos = (
                        remove_position[X]+x_index-2, remove_position[Y]+y_index-1)

                    # Check to ensure adjacent block is on the grid.
                    if not pos_chk(adj_block_pos, size):
                        continue

                    # Check adjacent block type and replace value to removed space.
                    if adj_block == 100:
                        empty_block = Open_Block()
                        empty_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 0:
                        closed_block = Block()
                        closed_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 1:
                        reflect_block = Reflect_Block()
                        reflect_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 2:
                        opaque_block = Opaque_Block()
                        opaque_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 3:
                        refract_block = Refract_Block()
                        refract_block.set_position(adj_block_pos, num_grid)

                # Check to the right of the block being removed.
                if y_index-1 == 0 and x_index-1 == 1:

                    # Identify adjacent block type and position.
                    adj_block = num_grid[remove_position[Y] +
                                         y_index-1][remove_position[X]+x_index-0]
                    adj_block_pos = (
                        remove_position[X]+x_index-0, remove_position[Y]+y_index-1)

                    # Check to ensure adjacent block is on the grid.
                    if not pos_chk(adj_block_pos, size):
                        continue

                    # Check adjacent block type and replace value to removed space.
                    if adj_block == 100:
                        empty_block = Open_Block()
                        empty_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 0:
                        closed_block = Block()
                        closed_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 1:
                        reflect_block = Reflect_Block()
                        reflect_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 2:
                        opaque_block = Opaque_Block()
                        opaque_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 3:
                        refract_block = Refract_Block()
                        refract_block.set_position(adj_block_pos, num_grid)

                # Check below the block being removed.
                if y_index-1 == 1 and x_index-1 == 0:

                    # Identify adjacent block type and position.
                    adj_block = num_grid[remove_position[Y] +
                                         y_index-0][remove_position[X]+x_index-1]
                    adj_block_pos = (
                        remove_position[X]+x_index-1, remove_position[Y]+y_index-0)

                    # Check to ensure adjacent block is on the grid.
                    if not pos_chk(adj_block_pos, size):
                        continue

                    # Check adjacent block type and replace value to removed space.
                    if adj_block == 100:
                        empty_block = Open_Block()
                        empty_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 0:
                        closed_block = Block()
                        closed_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 1:
                        reflect_block = Reflect_Block()
                        reflect_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 2:
                        opaque_block = Opaque_Block()
                        opaque_block.set_position(adj_block_pos, num_grid)
                    if adj_block == 3:
                        refract_block = Refract_Block()
                        refract_block.set_position(adj_block_pos, num_grid)

        # Return the new grid with modified values.
        return num_grid

    def mirror_direction(self, lazor_direction, side_of_block):
        '''
        This function takes the direction of the lazor and flips it depending
        on which side of the block it hits.

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

        # Determine a new, reflected direction for the lazor dependent on which
        # side of the block it enters the reflect or refract block on.
        if side_of_block == 0 or side_of_block == 2:
            new_direction = (lazor_direction[0], lazor_direction[1] * -1)
        if side_of_block == 1 or side_of_block == 3:
            new_direction = (lazor_direction[0] * -1, lazor_direction[1])

        # Return the new direction of the lazor.
        return new_direction

    def interact_lazor(self, lazor_position, lazor_direction):
        '''
        This function calculates the new position and direcetion based on how the block
        interacts with the lazor.

        **Parameters**
            lazor_position: *tuple*
                A tuple to hold the x and y coordinates of the current position
            lazor_direction: *tuple*
                A tuple to hold the vector for the direction of the lazor
            side_of_block: *int*
                The value for if the lazor hits the top or side of a block
                    0 = top/bottom
                    1 = left/right

        **Returns**
            new_position: *tuple*
                The next position for the lazor to go
            new_direction: *tuple*
                The next vector for the direction of the lazor
        '''

        # Determine the new direction and position for the lazor.
        # There is no change in lazor direction for open blocks,
        # but the lazor poistion advances by one space.
        new_direction = (lazor_direction[0], lazor_direction[1])
        new_position = (lazor_position[0] + new_direction[0],
                        lazor_position[1] + new_direction[1])

        # Return the lazor's new position and direction.
        return new_position, new_direction


class Open_Block(Block):
    '''
    A class that inherits the Block class
    Creates the open block with its unique attributes.

    **Parameters**
        None

    **Returns**
        None
    '''

    def __init__(self):
        '''
        This function initializes the Open_Block class object. It performs the following functions:
            self.type: Assigns its type.
            self.grid: Creates its 3x3 grid of elements that determine how the lazor will interact with it.
            self.positions: Generates an empty position list.

        **Parameters**
            self:

        **Returns**
            N/A
        '''

        # Set the block type to 'open'.
        self.type = 'open'
        self.positions = []

        # Set the new grid to be all 0's with one 100 in the middle for an open block.
        # 0   0   0
        # 0  100  0
        # 0   0   0
        open_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        open_grid[1][1] = 100
        self.grid = open_grid


class Reflect_Block(Block):
    '''
    A class that inherits the Block class
    Creates the reflect block with its unique attributes.

    **Parameters**
        None

    **Returns**
        None
    '''

    def __init__(self):
        '''
        This function initializes the Reflect_Block class object. It performs the following functions:
            self.type: Assigns its type.
            self.grid: Creates its 3x3 grid of elements that determine how the lazor will interact with it.
            self.positions: Generates an empty position list.

        **Parameters**
            self:

        **Returns**
            N/A
        '''

        # Set the block type to 'reflect'.
        self.type = 'reflect'
        self.positions = []

        # Set the new grid to the values associated with a reflect block.
        # 0  10   0
        # 11  1  11
        # 0  10   0
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

    def set_position(self, new_position, num_grid):
        '''
        This function takes the desired position of the block and adds the values of this block into the grid. 
            It overwrites spaces where block values are already present.
            It adds the position to the block's list of positions.

        **Parameters**
            new_position: *tuple*
                A tuple to hold the x and y coordinates of the new position
            num_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            num_grid: *list, list*
                The original grid with the updated values
        '''

        # Add the new position to the block's list of positions.
        self.positions.append(new_position)

        # Modify the original grid by adding the block's unique grid of numbers to the position specified.
        grid_edit = self.grid
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit[y_index])):
                num_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] = \
                    grid_edit[y_index][x_index]

        # Return the new grid with the modified block values.
        return num_grid

    def interact_lazor(self, lazor_position, lazor_direction, side_of_block):
        '''
        This function calculates the new position and direcetion based on how the block
        interacts with the lazor

        **Parameters**
            lazor_position: *tuple*
                A tuple to hold the x and y coordinates of the current position
            lazor_direction: *tuple*
                A tuple to hold the vector for the direction of the lazor
            side_of_block: *int*
                The value for if the lazor hits the top or side of a block
                    0 = top/bottom
                    1 = left/right

        **Returns**
            new_position: *tuple*
                The next position for the lazor to go
            new_direction: *tuple*
                The next vector for the direction of the lazor
        '''

        # Determine the new direction and position for the lazor.
        # The lazor direction reflects either vertically or horizontally dependent on the direction that
        # it entered the block from and the lazor poistion advances by one space in the new direction.
        new_direction = self.mirror_direction(lazor_direction, side_of_block)
        new_position = (lazor_position[0] + new_direction[0],
                        lazor_position[1] + new_direction[1])

        # Return the lazor's new position and direction.
        return new_position, new_direction


class Opaque_Block(Block):
    '''
    A class that inherits the Block class
    Creates the opaque block with its unique attributes.

    **Parameters**
        None

    **Returns**
        None
    '''

    def __init__(self):
        '''
        This function initializes the Opaque_Block class object. It performs the following functions:
            self.type: Assigns its type.
            self.grid: Creates its 3x3 grid of elements that determine how the lazor will interact with it.
            self.positions: Generates an empty position list.

        **Parameters**
            self:

        **Returns**
            N/A
        '''

        # Set the block type to 'opaque'.
        self.type = 'opaque'
        self.positions = []

        # Set the new grid to the values associated with a opaque block.
        # 0  20   0
        # 21  2  21
        # 0  20   0
        opaque_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        opaque_grid[0][1] = 20
        opaque_grid[1][0] = 21
        opaque_grid[2][1] = 20
        opaque_grid[1][2] = 21
        opaque_grid[1][1] = 2
        self.grid = opaque_grid

    def set_position(self, new_position, num_grid):
        '''
        This function takes the desired position of the block and adds the values of this block into the grid. 
            It overwrites spaces where block values are already present.
            It adds the position to the block's list of positions.

        **Parameters**
            new_position: *tuple*
                A tuple to hold the x and y coordinates of the new position
            num_grid: *list, list*
                The grid that the values of the new block will be placed into

        **Returns**
            num_grid: *list, list*
                The original grid with the updated values
        '''

        # Add the new position to the block's list of positions.
        self.positions.append(new_position)

        # Modify the original grid by adding the block's unique grid of numbers to the position specified.
        grid_edit = self.grid
        for y_index in range(len(grid_edit)):
            for x_index in range(len(grid_edit[y_index])):
                num_grid[new_position[Y]+y_index-1][new_position[X]+x_index-1] = \
                    grid_edit[y_index][x_index]

        # Return the new grid with the modified block values.
        return num_grid

    def interact_lazor(self, lazor_position, lazor_direction):

        # Determine the new direction and position for the lazor.
        # The lazor direction stops and the lazor becomes stationary upon entering the new block.
        # The lazor position remains at the entry point to the block.
        new_direction = (0, 0)
        new_position = lazor_position

        # Return the lazor's new position and direction.
        return new_position, new_direction


class Refract_Block(Block):
    '''
    A class that inherits the Block class
    Creates the refract block with its unique attributes.

    **Parameters**
        None

    **Returns**
        None
    '''

    def __init__(self):
        '''
        This function initializes the Refract_Block class object. It performs the following functions:
            self.type: Assigns its type.
            self.grid: Creates its 3x3 grid of elements that determine how the lazor will interact with it.
            self.positions: Generates an empty position list.

        **Parameters**
            self:

        **Returns**
            N/A
        '''

        # Set the block type to 'refract'.
        self.type = 'refract'
        self.positions = []

        # Set the new grid to the values associated with a refract block.
        # 0  30   0
        # 31  3  31
        # 0  30   0
        refract_grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
        refract_grid[0][1] = 30
        refract_grid[1][0] = 31
        refract_grid[2][1] = 30
        refract_grid[1][2] = 31
        refract_grid[1][1] = 3
        self.grid = refract_grid

    def interact_lazor(self, lazor_position, lazor_direction, side_of_block):

        # Determine the new direction and position for the lazor. For the refract block,
        # two lazor pathway will be created: one that passes the lazor through and
        # one that reflects the lazor.

        # There is no change in lazor direction for empty block path,
        # but the lazor poistion advances by one space.
        new_direction_empty = (lazor_direction[0], lazor_direction[1])
        new_position_empty = (lazor_position[0] + lazor_direction[0],
                              lazor_position[1] + lazor_direction[1])

        # The lazor direction reflects either vertically or horizontally dependent on the direction that
        # it entered the block from and the lazor poistion advances by one space in the new direction.
        new_direction_reflect = self.mirror_direction(
            lazor_direction, side_of_block)
        new_position_reflect = (lazor_position[0] + new_direction_reflect[0],
                                lazor_position[1] + new_direction_reflect[1])

        # Return the lazor's two new positions and directions.
        return new_position_empty, new_direction_empty, new_position_reflect, new_direction_reflect

# Solving Functions


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
    # Initialize variables
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

    # Open the file
    with open(filename, 'r') as file:
        # Iterate through the lines of the file
        for l in file:
            # Skip lines that start with #
            if l.startswith("#"):
                continue
            # Skip lines that start with ' '
            if l.startswith(" "):
                continue
            # If line starts with "GRID START" read until line hits
            # "GRID STOP"
            elif l.startswith('GRID START'):
                for grid_line in file:
                    if grid_line.startswith('GRID STOP'):
                        break
                    # Append the line onto the grid
                    grid_list.append(
                        [int(x) if x.isdigit() else x for x in grid_line.strip().split()])

            # If the line starts with "A" the counter onto reflect block
            elif l.startswith("A"):
                refl_block = [int(x) for x in l.strip().split()[1:]]
                num_refl_block = int(refl_block[0])

            # If the line starts with "B" the counter onto opaque block
            elif l.startswith("B"):
                opq_block = [int(x) for x in l.strip().split()[1:]]
                num_opq_block = int(opq_block[0])

            # If the line starts with "C" the counter onto refract block
            elif l.startswith("C"):
                refr_block = [int(x) for x in l.strip().split()[1:]]
                num_refr_block = int(refr_block[0])

            # If the line starts with "L" read info about the lazor
            elif l.startswith("L"):
                # Initialize the variable
                laz_data = []
                # Add the line onto the list
                laz_data.append(l.split()[1:])
                # Save the lazor start coordinates
                lazor_coor = (int(laz_data[0][0]), int(laz_data[0][1]))
                # Save the lazor start direction
                lazor_dir = (int(laz_data[0][2]), int(laz_data[0][3]))
                # Save a dictionary with the lazor information
                key = f"lazor{laz_count}"
                laz_dict[key] = [(lazor_coor[0], lazor_coor[1]),
                                 (lazor_dir[0], lazor_dir[1])]
                laz_count += 1

            # If the line starts with "P" read info about the targets
            elif l.startswith("P"):
                target.append(l.split()[1:])

    # Converting the output from the targets into a int
    target = [[int(element) for element in inner_list]
              for inner_list in target]
    for i in target:
        targets.append(tuple(i))
    # Return variables
    return grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets


def create_grid(grid_list):
    '''
    This function takes in the grid list from the inital open file function that contains only letters
    and transforms it into a larger grid of numbers for the lazor to pass through and interact with.

    **Parameters**
        grid_list: *list, list*
            A matrix holding the letter coding for blocks in the starting grid.

    **Returns**
        new_grid: *list, list*
            A matrix holding the number coding for blocks in the starting grid.
        possible_pos: *list* of tuples
            A list containing all of the positions of open blocks that can be replaced with other block
            classes when attempting to solve the puzzle.
    '''

    # Start x_count, y_count at (1, 1) to ensure block positions are placed on odd numbers of the matrix.
    x_count = 1
    y_count = 1
    new_grid = []

    # Initialize all block objects for use in placing on the starting grid.
    empty_block = Open_Block()
    closed_block = Block()
    reflect_block = Reflect_Block()
    opaque_block = Opaque_Block()
    refract_block = Refract_Block()

    # Determine the new grid size based on the size of the letter grid from the open file function.
    # Initialize the new grid as completely open with all 0's.
    new_grid_width = len(grid_list[0]) * 2 + 1
    new_grid_height = len(grid_list) * 2 + 1
    new_grid = [[0 for i in range(new_grid_width)]
                for j in range(new_grid_height)]

    blocks_dict = {'space': [],
                   'reflect': [],
                   'refract': [],
                   'opaque': []}
    block_location_value = 0
    # Iterate through the letter grid to identify block types for each position and place blocks
    # of the correct type into the number grid as each position is determined.
    for line in grid_list:
        for block in line:
            # 'o' corresponds to empty blocks that can be replaced by others in the future.
            if block == 'o':
                empty_block.set_position((x_count, y_count), new_grid)
                # Adds the value for count in the space key
                blocks_dict['space'].append(block_location_value)

            # 'x' corresponds to empty blocks that cannot be replaced by others in the future.
            if block == 'x':
                closed_block.set_position((x_count, y_count), new_grid)

            # 'A' corresponds to reflect blocks that cannot be replaced by others in the future.
            if block == 'A':
                reflect_block.set_position((x_count, y_count), new_grid)
                # Adds the value for count in the reflect key
                blocks_dict['reflect'].append(block_location_value)

            # 'B' corresponds to opaque blocks that cannot be replaced by others in the future.
            if block == 'B':
                opaque_block.set_position((x_count, y_count), new_grid)
                # Adds the value for count in the opaque key
                blocks_dict['opaque'].append(block_location_value)

            # 'C' corresponds to refract blocks that cannot be replaced by others in the future.
            if block == 'C':
                refract_block.set_position((x_count, y_count), new_grid)
                # Adds the value for count in the refract key
                blocks_dict['refract'].append(block_location_value)

            # Update the x_count as one line is iterated through.
            x_count += 2
            # Update the block_location_value as each block is iterated through
            block_location_value += 1
        # Reset the x_count to 1 as the next line is started.
        x_count = 1
        y_count += 2

    # Identify all of the empty block positions that can be replaced by others in the future.
    possible_pos = empty_block.get_positions()
    # Return the new grid of numbers that was generated and the list of positions that can be manipulated.
    return new_grid, possible_pos, blocks_dict


def lazor(num_grid, laz_dict, targets):
    '''
    This function takes the grid of the current status of the blocks and tracks the lazor
    to see if it reaches the target.

    **Parameters**

        num_grid: *list, list, int*
            A list of lists holding what blocks and targets are in the grid
            This grid will be tested as a solution.
        laz_dict: *dict*
            A dictionary storing the information about the starting position and direction
            of the lazors in the level
        targets: *list, tuple*
            A list of tuples which includes the coordinates of the targets

    **Returns**
        lazor_grid: *list, list, int*
            A list of lists holding the values for the grid
            This grid holds the information where the lazor traveled
        lazor_positions: *list, tuple*
            A list of all of the positions the lazor traveled to
        lazor_positions_dict: *dict*
            A dictionary containing all of the positions the lazor traveled to
            separated by lazor
        targets_results: *list, str*
            A list showing if all the targets were hit by the lazor

            lazor_grid, lazor_positions, lazor_positions_dict, targets_results
    '''

    # Initialize all block objects for use in manipulating lazor.
    empty_block = Open_Block()
    reflect_block = Reflect_Block()
    opaque_block = Opaque_Block()
    refract_block = Refract_Block()

    # Identify size of the grid.
    size = (len(num_grid[0]), len(num_grid))

    # Initialize the lazor grid to be all 0's to start.
    lazor_grid = [
        [0 for x in range(size[0])]
        for y in range(size[1])
    ]
    lazor_positions = []

    # Initialize the lazor grid dictionary of lazor paths and
    # the counter for number of lazors.
    lazor_grid_dict = {}
    lazor_positions_dict = {}
    laz_count = 0

    # Loop through each lazor in the dictionary
    for key in laz_dict:
        # Save the start coordinates and the start direction from the lazor
        lazor_start, lazor_start_direction = laz_dict[key]

        # Initialize the lazor starting point and direction on the stacks.
        lazor_path = [lazor_start]
        lazor_direction = [lazor_start_direction]

        # Initialize the lazor grid dictionary
        laz_grid_key = f"lazor_grid{laz_count}"
        # Set lazor grid dictionary to 0's
        lazor_grid_dict[laz_grid_key] = [
            [0 for x in range(size[0])]
            for y in range(size[1])
        ]
        # Initialize the lazor positions dictionary
        lazor_positions_dict[laz_grid_key] = []

        # Indicate the starting point of the lazor has been seen by the lazor.
        lazor_grid[lazor_start[Y]][lazor_start[X]] = 1
        lazor_grid_dict[laz_grid_key][lazor_start[Y]][lazor_start[X]] = 1

        # Continue to track the lazor while options remain in its path.
        while len(lazor_path) > 0:
            # print(key)
            # print(lazor_path)
            # print(lazor_direction)
            current_position = lazor_path.pop()
            lazor_positions.append(current_position)
            lazor_positions_dict[laz_grid_key] += [current_position]
            current_direction = lazor_direction.pop()

            # Check to ensure the current position is still within the grid.
            if not pos_chk((current_position[X], current_position[Y]), size):
                continue

            # Open Block: How to move when the lazor is moving through an open block.
            if num_grid[current_position[Y]][current_position[X]] == 0:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]
                                              ][current_position[X]] = 1
                # Determine the next position and direction from the open block class.
                next_position, next_direction = \
                    empty_block.interact_lazor(
                        current_position, current_direction)
                # Append the next lazor position and direction to their lists.
                lazor_path.append(next_position)
                lazor_direction.append(next_direction)

            # Reflect block (top/bottom): How to move when the lazor is moving through a
            # reflect block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 10:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]
                                              ][current_position[X]] = 1

                check_position_y = (
                    current_position[X], current_position[Y]+current_direction[Y])
                if pos_chk((check_position_y[X], check_position_y[Y]), size) and \
                        num_grid[check_position_y[Y]][check_position_y[X]] != 0 and \
                        num_grid[check_position_y[Y]][check_position_y[X]] != 100:
                    # Determine the next position and direction from the reflect block class.
                    next_position, next_direction = \
                        reflect_block.interact_lazor(
                            current_position, current_direction, 0)
                    # Append the next lazor position and direction to their lists.
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)
                else:
                    # If the lazor is inside the reflect block,
                    # Treat the reflect block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            # Reflect block (side): How to move when the lazor is moving through a
            # reflect block from the side.
            if num_grid[current_position[Y]][current_position[X]] == 11:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]
                                              ][current_position[X]] = 1

                # Check the position in front of the lazors in the x direction for a block
                check_position_x = (
                    current_position[X]+current_direction[X], current_position[Y])
                if pos_chk((check_position_x[X], check_position_x[Y]), size) and \
                        num_grid[check_position_x[Y]][check_position_x[X]] != 0 and \
                        num_grid[check_position_x[Y]][check_position_x[X]] != 100:
                    # Determine the next position and direction from the reflect block class.
                    next_position, next_direction = \
                        reflect_block.interact_lazor(
                            current_position, current_direction, 1)
                    # Append the next lazor position and direction to their lists.
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)
                else:
                    # If the lazor is inside the reflect block,
                    # Treat the reflect block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            # Opaque block: How to move when the lazor is moving through an opaque block.
            if num_grid[current_position[Y]][current_position[X]] == 20:
                # Check the position in front of the lazors in the y direction for a block
                check_position_y = (
                    current_position[X], current_position[Y]+current_direction[Y])
                if pos_chk((check_position_y[X], check_position_y[Y]), size) and \
                        num_grid[check_position_y[Y]][check_position_y[X]] != 0 and \
                        num_grid[check_position_y[Y]][check_position_y[X]] != 100:
                    # Indicate the lazor has passed through the current position.
                    lazor_grid[current_position[Y]][current_position[X]] = 1
                    lazor_grid_dict[laz_grid_key][current_position[Y]
                                                  ][current_position[X]] = 1
                else:
                    # If the lazor is inside the refract block,
                    # Treat the refract block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            if num_grid[current_position[Y]][current_position[X]] == 21:
                # Check the position in front of the lazors in the x direction for a block
                check_position_x = (
                    current_position[X]+current_direction[X], current_position[Y])
                if pos_chk((check_position_x[X], check_position_x[Y]), size) and \
                        num_grid[check_position_x[Y]][check_position_x[X]] != 0 and \
                        num_grid[check_position_x[Y]][check_position_x[X]] != 100:
                    # Indicate the lazor has passed through the current position.
                    lazor_grid[current_position[Y]][current_position[X]] = 1
                    lazor_grid_dict[laz_grid_key][current_position[Y]
                                                  ][current_position[X]] = 1
                else:
                    # If the lazor is inside the refract block,
                    # Treat the refract block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            # Refract Block (top/bottom): How to move when the lazor is moving through a
            # refract block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 30:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]
                                              ][current_position[X]] = 1
                # Check the next position to identify whether the lazor is inside a refract block or
                # entering a refract block.
                # If inside a refract block, the next position will be a 0 and
                # the lazor should not refract again.
                # If entering a refract block, the next position will not be a 0 and
                # the lazor should refract.
                check_position_y = (
                    current_position[X], current_position[Y]+current_direction[Y])
                if pos_chk((check_position_y[X], check_position_y[Y]), size) and \
                    num_grid[check_position_y[Y]][check_position_y[X]] != 0 and \
                        num_grid[check_position_y[Y]][check_position_y[X]] != 100:
                    # If the lazor is entering a new refract block,
                    # Determine the next position and direction from the refract block class.
                    next_position1, next_direction1, next_position2, next_direction2 = \
                        refract_block.interact_lazor(
                            current_position, current_direction, 0)
                    # Append the next lazor positions and directions to their lists.
                    lazor_path.append(next_position1)
                    lazor_direction.append(next_direction1)
                    lazor_path.append(next_position2)
                    lazor_direction.append(next_direction2)
                else:
                    # If the lazor is inside the refract block,
                    # Treat the refract block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            # Refract Block (top/bottom): How to move when the lazor is moving through a
            # refract block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 31:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]
                                              ][current_position[X]] = 1
                # Check the next position to identify whether the lazor is inside a refract block or
                # entering a refract block.
                # If inside a refract block, the next position will be a 0 and
                # the lazor should not refract again.
                # If entering a refract block, the next position will not be a 0 and
                # the lazor should refract.
                check_position_x = (
                    current_position[X]+current_direction[X], current_position[Y])
                if pos_chk((check_position_x[X], check_position_x[Y]), size) and \
                    num_grid[check_position_x[Y]][check_position_x[X]] != 0 and \
                        num_grid[check_position_x[Y]][check_position_x[X]] != 100:
                    # If the lazor is entering a new refract block,
                    # Determine the next position and direction from the refract block class.
                    next_position1, next_direction1, next_position2, next_direction2 = \
                        refract_block.interact_lazor(
                            current_position, current_direction, 1)
                    # Append the next lazor positions and directions to their lists.
                    lazor_path.append(next_position1)
                    lazor_direction.append(next_direction1)
                    lazor_path.append(next_position2)
                    lazor_direction.append(next_direction2)
                else:
                    # If the lazor is inside the refract block,
                    # Treat the refract block as an open block and determine the next position and
                    # direction from the open block class.
                    next_position, next_direction = \
                        empty_block.interact_lazor(
                            current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)
        laz_count += 1

    # Check the target list to identify if the targets have been hit by the lazor path.
    targets_results = []
    for i, target in enumerate(targets):
        if lazor_grid[target[Y]][target[X]] == 1:
            targets_results.append(True)
        else:
            targets_results.append(False)

    # Return the lazor grid of 0's and 1's, the lazor positions, and the results of
    # if the targets were hit.
    return lazor_grid, lazor_positions, lazor_positions_dict, targets_results


def solve_puzzle(num_grid, possible_pos, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets):
    '''
    Iterates through all of the possible solution permutations until 
    one passes through all targets to solve the puzzle.

    **Parameters** 
        num_grid: *list, list*
            The starting grid for the lazor puzzle before any blocks are placed.
        possible_pos: *list* of tuples
            All of the possible positions that blocks can be placed.
        num_refl_block: *int*
            The number of reflect blocks that can be used to solve a puzzle.
        num_opq_block: *int*
            The number of opaque blocks that can be used to solve a puzzle.
        num_refr_block: *int*
            The number of refract blocks that can be used to solve a puzzle.
        laz_dict: *dict*
            A dictionary of all of the lazors in a puzzle with
            their starting positions and directions as values.
        targets: *list* of tuples
            A list of the coordinate positions of all of the targets that
            the lazor needs to pass through in order to solve the puzzle.

    **Returns**
        solution_grid: *list, list*
            A list of lists holding the values for the grid that successfully 
            solved the puzzle including the values for all of the blocks.
        lazor_grid: *list, list*
            A list of lists holding the values for the lazor grid that successfully
            solved the puzzle including 1s for locations the lazor passed through and
            0s for locations that it did not.
        lazor_positions: *list*
            A list of tuples containing the (x, y) coordinates of all of the positions
            that any lazor has passed through.
        blocks_results_dict: *dict, list*
            A dictionary containing the information for placement of the different
            types of blocks
        lazor_positions_dict: *dict*
            A dictionary listing all of the coordinates that each lazor individually
            passes through.
        targets_results: *list*
            A list displaying whether the targets were hit by the lazors.

    '''

    # Finding the total number of blocks that will define the lenght of set of combinations
    num_movable_blocks = num_refl_block + num_opq_block + num_refr_block
    # Converting the movable blocks into a list of values to be use in the for loop later
    movable_blocks = []
    for i in range(num_refl_block):
        movable_blocks.append(1)
    for i in range(num_opq_block):
        movable_blocks.append(2)
    for i in range(num_refr_block):
        movable_blocks.append(3)

    # Check to see if all blocks are the same for a given puzzle.
    if all(ele == movable_blocks[0] for ele in movable_blocks):
        # Create all of the possible combinations of positions where blocks can be placed.
        position_perm = itertools.combinations(
            possible_pos, num_movable_blocks)

    else:
        # Create all of the possible permutations of positions where blocks can be placed.
        position_perm = itertools.permutations(
            possible_pos, num_movable_blocks)

    # Create a list from the permutations
    perm_list = list(position_perm)

    # Run the lazor through the original grid to check if solved and
    # generate initial lazor path.
    lazor_grid, lazor_positions, lazor_positions_dict, \
        targets_results = lazor(num_grid, laz_dict, targets)

    # Identify any permutations that do not affect the lazor path at all and delete those.
    neighbor_positions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    lazor_neighbors = []

    # Update list of all block space the lazor passes next to.
    for i in lazor_positions:
        for j in neighbor_positions:
            lazor_neighbors.append((i[0]+j[0], i[1]+j[1]))

    # Reduce the list of neighbors to only unique neighbors.
    lazor_neighbor_set = set(lazor_neighbors)

    # For all identified neighbors, check to ensure they are in the grid.
    neighbor_set = copy.deepcopy(lazor_neighbor_set)
    size = (len(num_grid[0]), len(num_grid))
    for option in lazor_neighbor_set:
        # Check to ensure adjacent block is on the grid.
        if not pos_chk(option, size):
            neighbor_set.remove(option)

    # For all permutation options, identify if the lazor passes next to at
    # least one block within the permutation. If it does, keep it.
    # If it does not, remove it.
    lazor_perm_list = copy.deepcopy(perm_list)
    # Iterate through to check each permutation.
    for option in perm_list:
        unique = True
        # Identify if any positions in the permutation would be
        #   adjacent to any spaces that the lazor is passing through.
        for position in option:
            for neighbor in neighbor_set:
                if position == neighbor:
                    unique = False
        # Remove options that don't affect the lazor at all.
        if unique == True:
            lazor_perm_list.remove(option)

    # Iterate through all of the permutations until the lazor successfully solves the puzzle in one.
    solution_grid = []
    lazor_grid = []
    lazor_positions = []
    lazor_positions_dict = {}
    targets_results = []
    # Iterate through and check each option.
    for option in lazor_perm_list:  # lazor_perm_list:

        # Make a copy of the original grid that can be updated.
        new_grid = copy.deepcopy(num_grid)

        # Iterate through all positions in a permutation set and place the blocks.
        reflect_blk = Reflect_Block()
        opaque_blk = Opaque_Block()
        refract_blk = Refract_Block()

        # Iterate through each position in each option to place blocks.
        for pos in range(len(option)):
            # Place block depending on the type
            if movable_blocks[pos] == 1:
                reflect_blk.set_position(option[pos], new_grid)
            if movable_blocks[pos] == 2:
                opaque_blk.set_position(option[pos], new_grid)
            if movable_blocks[pos] == 3:
                refract_blk.set_position(option[pos], new_grid)

        # Run the lazor through the solutions attempt.
        lazor_grid, lazor_positions, lazor_positions_dict, \
            targets_results = lazor(new_grid, laz_dict, targets)
        # If all targets are hit, save the solution and break the code.
        if all(targets_results):
            solution_grid = new_grid
            break

    # Output if no possible solutions can be found.
    if solution_grid == []:
        print("No Solution Found")

    # Initialize dictionary for the block positions of the solution
    blocks_results_dict = {'space': [],
                           'reflect': [],
                           'refract': [],
                           'opaque': []}
    block_location_value = 0

    # Iterate through the letter grid to identify block types for each position and place blocks
    # of the correct type into the number grid as each position is determined.
    for i in range(len(solution_grid)):
        for j in range(len(solution_grid[i])):
            if i % 2 != 0 and j % 2 != 0:
                # 100 corresponds to empty blocks.
                if solution_grid[i][j] == 100:
                    # Adds the value for count in the space key
                    blocks_results_dict['space'].append(block_location_value)

                # 1 corresponds to reflect blocks.
                if solution_grid[i][j] == 1:
                    # Adds the value for count in the reflect key
                    blocks_results_dict['reflect'].append(block_location_value)

                # 2 corresponds to opaque blocks.
                if solution_grid[i][j] == 2:
                    # Adds the value for count in the opaque key
                    blocks_results_dict['opaque'].append(block_location_value)

                # 3 corresponds to refract blocks.
                if solution_grid[i][j] == 3:
                    # Adds the value for count in the refract key
                    blocks_results_dict['refract'].append(block_location_value)
                # Update the block_location_value as each block is iterated through
                block_location_value += 1

    # Return the solution grid, the grid of lazor values
    #   for the solution, the lazor positions dictionary
    # with the values for all lasers individually, and
    #   the results of the targets and whether they were hit.
    return solution_grid, lazor_grid, lazor_positions, \
        blocks_results_dict, lazor_positions_dict, targets_results

# Ancillary Functions


def pos_chk(position, size):
    '''
    Validate if the coordinates specified (x and y) are within the grid.

    **Parameters**

        position: *tuple* (int, int)
            A tuple of x, y coordinates for a position.
        size: *tuple* (int, int)
            How many blocks wide and how many blocks in height the grid is.
            Should be equivalent to the length of the grid and its row-lists. 
            (ie. (len(grid[0]), len(grid))).

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (False).
    '''

    # Return true if the position is within the grid. Return False if it is not.
    return position[0] >= 0 and position[0] < size[0] and position[1] >= 0 and position[1] < size[1]


def print_matrix(input_list):
    '''
    This function prints a matrix on row at a time. Makes it easier to read.

    **Parameters**

        input_list: *list, list*
            A a list of lists to be printed

    **Returns**

    '''
    # Print rows separately
    for rows in input_list:
        print(rows)

# Output Visualization Functions


def place_blocks(canvas, blocks_dict, width, matrix_size_x, matrix_size_y):
    '''
    This function places the blocks in the grid. It places both the spaces for blocks
    and the blocks themselves.

    **Parameters**

        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        blocks_dict: *dict*
            A dictionary holding the positions of each type of block
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
        matrix_size_y: *int*
            A value for the number of rows of spaces

    **Returns**
        None
    '''

    # Calculate the size of the box based on the width of the screen as well as how many columns
    # of blocks there are
    box_size = width / (matrix_size_x*2)
    # Calculate the size of the gap between the blocks
    gap_between = (2*width/(matrix_size_x+1)) - \
        (1*width/(matrix_size_x+1) + box_size)
    # Calculate the size of the block based on the box size and the gap between the boxes
    block_size = box_size + gap_between
    # Initialize the offset for the y axis
    offset = 100

    # Loop through a dictionary that contains the information where each block is
    for key in blocks_dict:
        # If the block is an open space
        if key == 'space':
            # Initialilize count
            count = 0
            # Loop through the available spaces in the game
            for i in range(matrix_size_y):
                for j in range(matrix_size_x):
                    # If the amount of times it has looped through the available spaces
                    # is the same as where a block is insert it
                    if count in blocks_dict[key]:
                        # Initialize the x and y location of the top left corner of the block
                        x_location = (
                            (j+1)*width/(matrix_size_x+1)) - (box_size/2)
                        y_location = (i+1)*width/(matrix_size_x +
                                                  1) - (box_size/2) + offset
                        # Draw the block
                        canvas.create_rectangle(x_location, y_location,
                                                x_location+box_size, y_location+box_size,
                                                fill="black")
                    # Iterate count
                    count += 1
        # If the block is a reflect block
        if key == 'reflect':
            # Initialilize count
            count = 0
            # Loop through the available spaces in the game
            for i in range(matrix_size_y):
                for j in range(matrix_size_x):
                    # If the amount of times it has looped through the available spaces
                    # is the same as where a block is insert it
                    if count in blocks_dict[key]:
                        # Initialize the x and y location of the top left corner of the block
                        block_x_position = (
                            (j+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (
                            i+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        # Draw the block
                        canvas.create_rectangle(block_x_position, block_y_position,
                                                block_x_position+block_size, block_y_position+block_size,
                                                fill="tan")
                    # Iterate count
                    count += 1
        # If the block is a refract block
        if key == 'refract':
            # Initialilize count
            count = 0
            # Loop through the available spaces in the game
            for i in range(matrix_size_y):
                for j in range(matrix_size_x):
                    # If the amount of times it has looped through the available spaces
                    # is the same as where a block is insert it
                    if count in blocks_dict[key]:
                        # Initialize the x and y location of the top left corner of the block
                        block_x_position = (
                            (j+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (
                            i+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        # Draw the block
                        canvas.create_rectangle(block_x_position, block_y_position,
                                                block_x_position+block_size, block_y_position+block_size,
                                                fill="#EDF7FB")
                    # Iterate the count
                    count += 1
        # If the block is an opaque block
        if key == 'opaque':
            # Initialize the count
            count = 0
            # Loop through the available spaces in the game
            for i in range(matrix_size_y):
                for j in range(matrix_size_x):
                    # If the amount of times it has looped through the available spaces
                    # is the same as where a block is insert it
                    if count in blocks_dict[key]:
                        # Initialize the x and y location of the top left corner of the block
                        block_x_position = (
                            (j+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (
                            i+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        # Draw the block
                        canvas.create_rectangle(block_x_position, block_y_position,
                                                block_x_position+block_size, block_y_position+block_size,
                                                fill="#A66408")
                    # Iterate the count
                    count += 1


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
    # Calculate the radius of the circle based on the diameter
    radius = diameter / 2
    # Calculate the box size based on the width of the game and the availible number
    # of boxes
    box_size = width / (matrix_size_x*2)
    # Calculate the gap between the boxes
    gap_between = (2*width/(matrix_size_x+1)) - \
        (1*width/(matrix_size_x+1) + box_size)
    # Calculate the block sized based on box size and the gap between
    block_size = box_size + gap_between
    # Initialize the offset in the y
    offset = 100
    # Initialize the size of both x and y where the target would be
    x_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius
    y_size = (width/(matrix_size_x+1))-(box_size/2) - \
        (gap_between/2) - radius + offset

    # Iterate through each location of the targets
    for coordinate in coordinates:
        try:
            # Initialize the starting position for the x and y
            start_x_position = x_size + (coordinate[0]*(block_size/2))
            start_y_position = y_size + (coordinate[1]*(block_size/2))
            # Draw the circle
            canvas.create_oval(start_x_position, start_y_position,
                               start_x_position+diameter, start_y_position+diameter,
                               fill='grey')
        except:
            pass


def draw_lazor(canvas, laz_dict, lazor_position_dict, width, matrix_size_x, diameter):
    '''
    This function draws the lazor in the grid.

    **Parameters**
        UPDATE
        canvas: *tkinter object*
            A canvas object that the blocks will be drawn on
        laz_dict: *dict*
            A dictionary containing the intialize position and direction
            of the lazors
        laz_position_dict: *dict*
            A dictionary containing the positions of where the 
            lazor traveled for all the lazors through the level
        width: *int*
            A value for the width of the canvas object
        matrix_size_x: *int*
            A value for the number of columns of spaces
        diameter: *int*
            A value for the diameter of the targets

    **Returns**
        None
    '''
    # Calculate the radius based on the diameter
    radius = diameter / 2
    # Calculate the box size based on the width and how many blocks in the x
    # there are
    box_size = width / (matrix_size_x*2)
    # Calculate the gap between each box
    gap_between = (2*width/(matrix_size_x+1)) - \
        (1*width/(matrix_size_x+1) + box_size)
    # Calculate the block size based on the box size and the gap between
    block_size = box_size + gap_between
    # Initialize the offset in the y
    offset = 100
    # Calculate the x and y size for the starting position of the lazor
    x_size = (width/(matrix_size_x+1))-(box_size/2)-(gap_between/2) - radius
    y_size = (width/(matrix_size_x+1))-(box_size/2) - \
        (gap_between/2) - radius + offset

    # Loop through each lazor in the dictionary
    for key in laz_dict:
        # Draw the starting point for each lazor
        # Calculate the start position for the lazor
        start_x_position = x_size + (laz_dict[key][0][0]*(block_size/2))
        start_y_position = y_size + (laz_dict[key][0][1]*(block_size/2))
        # Add circle to the canvas
        canvas.create_oval(start_x_position, start_y_position,
                           start_x_position+diameter, start_y_position+diameter,
                           fill='red')

    # Iterate through each lazor in the dictionary
    for key in lazor_position_dict:
        print(lazor_position_dict[key])
        # Loop through each coordinate the lazor traveled to
        for i, coordinate in enumerate(lazor_position_dict[key]):
            try:
                # Check if the position before the block is more than one block away
                if lazor_position_dict[key][i+1][0] - coordinate[0] > 1 or lazor_position_dict[key][i+1][0] - coordinate[0] < -1:
                    if lazor_position_dict[key][i+1][1] - coordinate[1] > 1 or lazor_position_dict[key][i+1][1] - coordinate[1] < -1:
                        print(coordinate)
                        # Initialize the count
                        count = 0
                        # Loop through to find the closest block to this position
                        while lazor_position_dict[key][count][0] != lazor_position_dict[key][i+1][0] or lazor_position_dict[key][count][1] != lazor_position_dict[key][i+1][1]:
                            if (lazor_position_dict[key][i+1][0] - lazor_position_dict[key][count][0] == -1 and lazor_position_dict[key][i+1][1] - lazor_position_dict[key][count][1] == -1)\
                                    or (lazor_position_dict[key][i+1][0] - lazor_position_dict[key][count][0] == 1 and lazor_position_dict[key][i+1][1] - lazor_position_dict[key][count][1] == 1)\
                                    or (lazor_position_dict[key][i+1][0] - lazor_position_dict[key][count][0] == -1 and lazor_position_dict[key][i+1][1] - lazor_position_dict[key][count][1] == 1)\
                                    or (lazor_position_dict[key][i+1][0] - lazor_position_dict[key][count][0] == 1 and lazor_position_dict[key][i+1][1] - lazor_position_dict[key][count][1] == -1):
                                # Save the value of the block 1 away that is the closest in the list
                                value = (
                                    lazor_position_dict[key][count][0], lazor_position_dict[key][count][1])
                            # Iterate the count
                            count += 1
                        # Replace the value of the position before with this value
                        lazor_position_dict[key][count-1] = value
                        print(lazor_position_dict[key])
            except:
                pass
        # Loop through all the coordinates in the position list
        # for i, coordinate in enumerate(lazor_position_dict[key]):
            try:
                # Make sure doesn't index backwards
                if i-1 < 0:
                    continue
                else:
                    # Create the start and end positions of the lazor
                    start_x_position = x_size + \
                        (lazor_position_dict[key][i-1][0]*(block_size/2))
                    start_y_position = y_size + \
                        (lazor_position_dict[key][i-1][1]*(block_size/2))
                    # lazor_position_dict[key][i][0]
                    end_x_position = x_size + (coordinate[0]*(block_size/2))
                    end_y_position = y_size + (coordinate[1]*(block_size/2))
                    # Draw the lazor between the two points
                    canvas.create_line(start_x_position+radius, start_y_position+radius,
                                       end_x_position+radius, end_y_position+radius,
                                       fill='red', width=3)
            except:
                pass


def display_level(level_title):
    '''
    Reads in a file and displays the inital state of the level

    **Parameters** 
        level_title: *str*
            The name of the level you want to play.

    **Returns**
        None
    '''
    # Open the file using the title of the level
    grid_list, num_refl_block, num_opq_block, num_refr_block, \
        laz_dict, targets = openlazorfile(level_title)
    # Create initial grid of the level
    num_grid, possible_pos, blocks_dict = create_grid(grid_list)
    # Track lazor through initial level
    lazor_grid, lazor_positions, lazor_positions_dict, \
        targets_results = lazor(num_grid, laz_dict, targets)

    WIDTH = 300
    HEIGHT = WIDTH * 2

    MATRIX_SIZE_X = len(grid_list[0])
    MATRIX_SIZE_Y = len(grid_list)
    DIAMETER = 10

    # Initialize the left side for the initial level
    image_start = Canvas(win, width=WIDTH, height=HEIGHT, bg="grey")
    image_start.grid(row=1, column=0)

    # Place the initial blocks from the level
    place_blocks(image_start, blocks_dict,
                 WIDTH, MATRIX_SIZE_X, MATRIX_SIZE_Y)

    # Place the targets from the level
    place_targets(image_start, targets,
                  WIDTH, MATRIX_SIZE_X, DIAMETER)

    # Draw the lazor for the level
    draw_lazor(image_start, laz_dict, lazor_positions_dict,
               WIDTH, MATRIX_SIZE_X, DIAMETER)


def display_solution(level_title):
    '''
    Reads in a file and displays the solved state of the level

    **Parameters** 
        level_title: *str*
            The name of the level you want to play.

    **Returns**
        None
    '''
    # Set width and height of the game
    WIDTH = 300
    HEIGHT = WIDTH * 2

    # Initialize the image on the right for the solution
    image_solution = Canvas(win, width=WIDTH, height=HEIGHT, bg="grey")
    # Place the image on the screen
    image_solution.grid(row=1, column=2)

    # Read in the file
    grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets = openlazorfile(
        level_title)
    # Create intiial grid
    num_grid, possible_pos, blocks_dict = create_grid(grid_list)
    # Solve the puzzle
    solution_grid, lazor_grid, lazor_positions,\
        blocks_results_dict, lazor_positions_dict, targets_results = \
        solve_puzzle(num_grid, possible_pos, num_refl_block, num_opq_block,
                     num_refr_block, laz_dict, targets)

    # Initialize the size of the grid for the image
    MATRIX_SIZE_X = len(grid_list[0])
    MATRIX_SIZE_Y = len(grid_list)
    DIAMETER = 10

    # Place the blocks on the image
    place_blocks(image_solution, blocks_results_dict,
                 WIDTH, MATRIX_SIZE_X, MATRIX_SIZE_Y)

    # Place the targets on the image
    place_targets(image_solution, targets,
                  WIDTH, MATRIX_SIZE_X, DIAMETER)

    # Draw the path of the lazor
    draw_lazor(image_solution, laz_dict, lazor_positions_dict,
               WIDTH, MATRIX_SIZE_X, DIAMETER)


def screenshot_window(level_title):
    level_title = level_title - ".bff"
    print(level_title)
    # filename = "https://github.com/mturley95/Lazor_Project.git/" + level_title + ".png"
    screenshot = pg.screenshot()
    screenshot.save("level_title", format="PNG")
    # win.deiconify()


if __name__ == '__main__':
    # The start of the level
    # Initialize window
    win = Tk()
    win.geometry("800x700")
    # Set width and height of the game
    WIDTH = 300
    HEIGHT = WIDTH * 2

    # Level Selection Text Field
    # Initialize the entry field
    level_selection_text = Entry(
        win, width=25, text="Pleaese Enter Level", borderwidth=5)
    # Place entry field in the window
    level_selection_text.grid(row=0, column=1)
    # Add default text into entry field
    level_selection_text.insert(0, ".bff")

    # Initialize image on the left for the level
    image_start = Canvas(win, width=WIDTH, height=HEIGHT, bg="grey")
    image_start.grid(row=1, column=0)

    # Initialize image on the right for the solution
    image_solution = Canvas(win, width=WIDTH, height=HEIGHT, bg="grey")
    image_solution.grid(row=1, column=2)

    # Showw Level Button
    # Initialize button to display level
    display_level_button = Button(win, text="Display Level",
                                  command=lambda: display_level(level_selection_text.get()))
    # Place button on the window
    display_level_button.grid(row=0, column=2, padx=10)

    # Solve Button
    # Initialize button to solve the level
    solve_puzzle_button = Button(win, text="Solve Puzzle",
                                 command=lambda: display_solution(level_selection_text.get()))
    # Place button on the window
    solve_puzzle_button.grid(row=1, column=1, padx=50)

    # Screenshot the window
    screenshot_window(level_selection_text.get())

    # Show the window
    win.mainloop()
