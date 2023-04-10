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
        self.type = 'empty'
        self.grid = [
            [0 for i in range(3)]
            for j in range(3)
        ]
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

        for i in self.positions:
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

        # Modify the original grid by adding the block's unique grid of numbers to the position specified.
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
        grid_edit = [
            [0 for i in range(3)]
            for j in range(3)
        ]
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
                    adj_block = num_grid[remove_position[Y]+y_index-2][remove_position[X]+x_index-1]
                    adj_block_pos = (remove_position[X]+x_index-1, remove_position[Y]+y_index-2)

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
                    adj_block = num_grid[remove_position[Y]+y_index-1][remove_position[X]+x_index-2]
                    adj_block_pos = (remove_position[X]+x_index-2, remove_position[Y]+y_index-1)
                    
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
                    adj_block = num_grid[remove_position[Y]+y_index-1][remove_position[X]+x_index-0]
                    adj_block_pos = (remove_position[X]+x_index-0, remove_position[Y]+y_index-1)             
                    
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
                    adj_block = num_grid[remove_position[Y]+y_index-0][remove_position[X]+x_index-1]
                    adj_block_pos = (remove_position[X]+x_index-1, remove_position[Y]+y_index-0)

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
        new_direction = mirror_direction(lazor_direction, side_of_block)
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
        new_direction_reflect = mirror_direction(lazor_direction, side_of_block)
        new_position_reflect = (lazor_position[0] + new_direction_reflect[0],
                                lazor_position[1] + new_direction_reflect[1])

        # Return the lazor's two new positions and directions.
        return new_position_empty, new_direction_empty, new_position_reflect, new_direction_reflect


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

    # Iterate through the letter grid to identify block types for each position and place blocks 
    # of the correct type into the number grid as each position is determined.
    for line in grid_list:
        for block in line:
            # 'o' corresponds to empty blocks that can be replaced by others in the future.
            if block == 'o':
                empty_block.set_position((x_count, y_count), new_grid)

            # 'x' corresponds to empty blocks that cannot be replaced by others in the future.
            if block == 'x':
                closed_block.set_position((x_count, y_count), new_grid)

            # 'A' corresponds to reflect blocks that cannot be replaced by others in the future.
            if block == 'A':
                reflect_block.set_position((x_count, y_count), new_grid)

            # 'B' corresponds to opaque blocks that cannot be replaced by others in the future.
            if block == 'B':
                opaque_block.set_position((x_count, y_count), new_grid)

            # 'C' corresponds to refract blocks that cannot be replaced by others in the future.
            if block == 'C':
                refract_block.set_position((x_count, y_count), new_grid)

            # Update the x_count as one line is iterated through.
            x_count += 2
        # Reset the x_count to 1 as the next line is started.
        x_count = 1
        y_count += 2
    
    # Identify all of the empty block positions that can be replaced by others in the future.
    possible_pos = empty_block.get_positions()

    # Return the new grid of numbers that was generated and the list of positions that can be manipulated.
    return new_grid, possible_pos

def create_possible_solutions(num_grid, lazors, targets, num_reflect, num_refract, num_opaque):
    '''
    Try solutions to the puzzle until it is solved

    **Parameters**
        num_grid: *list, list*
            A matrix holding the starting position for the grid
        lazors: *dict*
            Dictionary holding the lazors position and direction
        targets: *list, tuple*
            List of x y coordinates for the targets
        num_reflect: *int*
            Number of reflect blocks we can add to the puzzle
        num_refract: *int*
            Number of reflect blocks we can add to the puzzle
        num_opaque: *int*
            Number of reflect blocks we can add to the puzzle

    **Returns**
        grid_solution: *list, list*
            The solution to the grid
    '''
    lazor0 = lazors['lazor0']
    lazor0_start = lazor0[0]
    lazor0_direction = lazor0[1]
    lazor(num_grid, lazor0_start, lazor0_direction, targets)

## Output visualization
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

    UPDATE:
    - Add other colors and ability to place whatever block you want
    - Make drawing the blocks a function
        
    '''
    box_size = width / (matrix_size_x*2)
    gap_between = (2*width/(matrix_size_x+1)) - (1*width/(matrix_size_x+1) + box_size)
    block_size = box_size + gap_between
    offset = 200

    for key in blocks_dict:
        if key == 'space':
            count = 0
            for i in range(matrix_size_x):
                for j in range(matrix_size_y):
                    if count in blocks_dict[key]:
                        x_location = ((i+1)*width/(matrix_size_x+1)) - (box_size/2)
                        y_location = (j+1)*width/(matrix_size_x+1) - (box_size/2) + offset
                        canvas.create_rectangle(x_location,y_location,
                                                x_location+box_size,y_location+box_size,
                                                fill="black")
                    count += 1
        if key == 'reflect':
            count = 0
            for i in range(matrix_size_x):
                for j in range(matrix_size_y):
                    if count in blocks_dict[key]:
                        block_x_position = ((i+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (j+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        canvas.create_rectangle(block_x_position,block_y_position,
                                                block_x_position+block_size,block_y_position+block_size,
                                                fill="tan")
                    count += 1
        if key == 'refract':
            count = 0
            for i in range(matrix_size_x):
                for j in range(matrix_size_y):
                    if count in blocks_dict[key]:
                        block_x_position = ((i+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (j+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        canvas.create_rectangle(block_x_position,block_y_position,
                                                block_x_position+block_size,block_y_position+block_size,
                                                fill="#EDF7FB")
                    count += 1
        if key == 'opaque':
            count = 0
            for i in range(matrix_size_x):
                for j in range(matrix_size_y):
                    if count in blocks_dict[key]:
                        block_x_position = ((i+1)*width/(matrix_size_x+1))-(box_size/2)-(gap_between/2)
                        block_y_position = (j+1)*width/(matrix_size_x+1)-(box_size/2)-(gap_between/2)+offset
                        canvas.create_rectangle(block_x_position,block_y_position,
                                                block_x_position+block_size,block_y_position+block_size,
                                                fill="#A66408")
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
        # if coordinates[i+1][0] - coordinate[0] > 1 and coordinates[i+1][1] - coordinate[1] > 1:
        #     count = 0
        #     while coordinates[count][0] != coordinates[i+1][0] and coordinates[count][1] != coordinates[i+1][1]:
        #         if coordinates[i+1][0] - coordinates[count][0] == 1 and coordinates[i+1][1] - coordinates[count][1] == 1:
        #             value = (coordinates[count][0], coordinates[count][1])
        #         else:
        #             value = (0,0)
        #         count += 1

        #     coordinates[count] = value
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

def lazor(num_grid, laz_dict, targets):
    '''
    This function takes the grid of the current status of the blocks and tracks the lazor
    to see if it reaches the target.

    **Parameters**

        num_grid: *list, list, int*
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

    for key in laz_dict:
        lazor_start, lazor_start_direction = laz_dict[key]

        # Initialize the lazor starting point and direction.
        lazor_path = [lazor_start]
        lazor_direction = [lazor_start_direction]
        
        laz_grid_key = f"lazor_grid{laz_count}"
        lazor_grid_dict[laz_grid_key] = [
            [0 for x in range(size[0])]
            for y in range(size[1])
        ]
        lazor_positions_dict[laz_grid_key] = []

        # Indicate the starting point of the lazor has been seen by the lazor.
        lazor_grid[lazor_start[Y]][lazor_start[X]] = 1
        lazor_grid_dict[laz_grid_key][lazor_start[Y]][lazor_start[X]] = 1

        # Continue to track the lazor while options remain in its path.
        while len(lazor_path) > 0:
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
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
                # Determine the next position and direction from the open block class.
                next_position, next_direction = \
                    empty_block.interact_lazor(current_position, current_direction)
                # Append the next lazor position and direction to their lists.
                lazor_path.append(next_position)
                lazor_direction.append(next_direction)

            # Reflect block (top/bottom): How to move when the lazor is moving through a 
            # reflect block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 10:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
                # Determine the next position and direction from the reflect block class.
                next_position, next_direction = \
                    reflect_block.interact_lazor(current_position, current_direction, 0)
                # Append the next lazor position and direction to their lists.
                lazor_path.append(next_position)
                lazor_direction.append(next_direction)

            # Reflect block (side): How to move when the lazor is moving through a 
            # reflect block from the side.
            if num_grid[current_position[Y]][current_position[X]] == 11:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
                # Determine the next position and direction from the reflect block class.
                next_position, next_direction = \
                    reflect_block.interact_lazor(current_position, current_direction, 1)
                # Append the next lazor position and direction to their lists.
                lazor_path.append(next_position)
                lazor_direction.append(next_direction)

            # Opaque block: How to move when the lazor is moving through an opaque block.
            if num_grid[current_position[Y]][current_position[X]] == 20:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
            if num_grid[current_position[Y]][current_position[X]] == 21:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1

            # Refract Block (top/bottom): How to move when the lazor is moving through a 
            # refract block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 30:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
                # Check the next position to identify whether the lazor is inside a refract block or 
                # entering a refract block.
                # If inside a refract block, the next position will be a 0 and 
                # the lazor should not refract again.
                # If entering a refract block, the next position will not be a 0 and 
                # the lazor should refract.
                check_position_y = (current_position[X],current_position[Y]+current_direction[Y])
                if pos_chk((check_position_y[X], check_position_y[Y]), size) and \
                num_grid[check_position_y[Y]][check_position_y[X]] != 0:
                    # If the lazor is entering a new refract block,
                    # Determine the next position and direction from the refract block class.
                    next_position1, next_direction1, next_position2, next_direction2 = \
                        refract_block.interact_lazor(current_position, current_direction, 0)
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
                        empty_block.interact_lazor(current_position, current_direction)
                    lazor_path.append(next_position)
                    lazor_direction.append(next_direction)

            # Refract Block (top/bottom): How to move when the lazor is moving through a 
            # refract block from the top/bottom.
            if num_grid[current_position[Y]][current_position[X]] == 31:
                # Indicate the lazor has passed through the current position.
                lazor_grid[current_position[Y]][current_position[X]] = 1
                lazor_grid_dict[laz_grid_key][current_position[Y]][current_position[X]] = 1
                # Check the next position to identify whether the lazor is inside a refract block or 
                # entering a refract block.
                # If inside a refract block, the next position will be a 0 and 
                # the lazor should not refract again.
                # If entering a refract block, the next position will not be a 0 and 
                # the lazor should refract.
                check_position_x = (current_position[X]+current_direction[X],current_position[Y])
                if pos_chk((check_position_x[X], check_position_x[Y]), size) and \
                num_grid[check_position_x[Y]][check_position_x[X]] != 0:
                    # If the lazor is entering a new refract block,
                    # Determine the next position and direction from the refract block class.
                    next_position1, next_direction1, next_position2, next_direction2 = \
                        refract_block.interact_lazor(current_position, current_direction, 1)
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
                        empty_block.interact_lazor(current_position, current_direction)
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

def mirror_direction(lazor_direction, side_of_block):
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


def solve_puzzle(permutations_grids, laz_dict, targets):
    '''
   Iterates through all of the possible solution permutations until 
   one passes through all targets to solve the puzzle.

    **Parameters**

        permutations_grids: *list, list, list*
            A list of all of the possible solution permutations
            (which themselves are lists of lists)
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
        lazor_positions_dict: *dict*
            A dictionary listing all of the coordinates that each lazor individually
            passes through.
        targets_results: *list*
            A list displaying whether the targets were hit by the lazors.
    '''

    # Iterate through all of the permutations until the lazor successfully solves the puzzle in one.
    solution_grid = []
    lazor_grid = []
    lazor_positions = []
    lazor_positions_dict = {}
    targets_results = []
    for i in permutations_grids:
        lazor_grid, lazor_positions, lazor_positions_dict, targets_results = lazor(i, laz_dict, targets)
        # If all targets are hit, save the solution and break the code.
        if all(targets_results):
            solution_grid = i
            break
    # Return the solution grid, the grid of lazor values for the solution, the lazor positions dictionary
    # with the values for all lasers individually, and the results of the targets and whether they were hit.
    return solution_grid, lazor_grid, lazor_positions, lazor_positions_dict, targets_results


def display_solution(space_positions, block_positions, start_coordinate,
                 target_coordinates, lazor_coordinates):
    '''
    Draws the lazor pathway that solves the lazor puzzle.
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

def permutations_blocks(num_grid, possible_pos, num_refl_block, num_opq_block, num_refr_block):
    '''
    returns a permutations where the blocks can be placed in a list

    **Parameters**

        filename: *str*
            The file name of that from where we get the combinations
         

    **Returns**
        combinations: *list*
            List of permutations where the blocks can be placed
    '''
    
    #finding the total number of blocks that will define the lenght of set of combinations
    num_movable_blocks = num_refl_block+num_opq_block+num_refr_block
    # converting the movable blocks into a list of values to be use in the for loop later
    movable_blocks = []
    for i in range(num_refl_block):
        movable_blocks.append(1)
    for i in range(num_opq_block):
        movable_blocks.append(2)
    for i in range(num_refr_block):
        movable_blocks.append(3)
    
    #print(movable_blocks)
    #Creating the permutations of postiitons where blocks can be placed
    position_perm = itertools.permutations(possible_pos,num_movable_blocks)
    perm_list = list(position_perm)
    #print(perm_list) 
    #print(len(perm_list))
    #print(perm_list[0])
    #print(perm_list[0][0])
    permutations_grids = []
    #print(num_grid)
    #new_Grid = num_grid[:]
    for set in perm_list:
        #print(set)
        #print(range(len(set)))
        new_Grid = copy.deepcopy(num_grid)
        #print(new_Grid)
        for pos in range(len(set)):
            #print(pos)
            #print(set[pos])
            #print(new_Grid)
            if movable_blocks[pos] == 1:
                reflect_blk = Reflect_Block()
                reflect_blk.set_position(set[pos], new_Grid)
            if movable_blocks[pos] == 2:
                opaque_blk = Opaque_Block()
                opaque_blk.set_position(set[pos], new_Grid)
            if movable_blocks[pos] == 3:
                refract_blk = Refract_Block()
                refract_blk.set_position(set[pos], new_Grid)
            #print(range(len(pos)))

        
        permutations_grids.append(new_Grid)
        #new_Grid = copy.deepcopy(num_grid)  
        # print_matrix(new_Grid)
        # print("\n")
        # print_matrix(num_grid)
        # print("\n")
        
        
    # print(permutations_grids[0])
    # print_matrix(permutations_grids[0])
    # print("\n")
    # print_matrix(permutations_grids[51])
    # # print(grid_list)
    # print(num_refl_block)
    # print(num_opq_block)
    # print(num_refr_block)
    # print(num_grid)
    return permutations_grids

if __name__ == '__main__':
    # Reflect block = 1
    # Opaque block = 2
    # Left, Right = X0
    # Top, Bottom = X1
    # grid = 0 ,0   ,0   ,10  ,0   ,0  ,0
    #        0 ,100 ,11  ,1   ,11  ,100,0
    #        0 ,0   ,0   ,10  ,0   ,10 ,0
    #        0 ,100 ,0   ,100 ,11  ,1  ,11
    #        0 ,0   ,0   ,0   ,0   ,10 ,0
    #        0 ,100 ,0   ,100 ,0   ,100,0
    #        0 ,0   ,0   ,0   ,0   ,0  ,0
    
    grid_test = [
        [0 for i in range(7)]
        for j in range(7)
    ]

    grid_test[1][1] = 100
    grid_test[1][5] = 100
    grid_test[3][1] = 100
    grid_test[3][3] = 100
    grid_test[5][1] = 100
    grid_test[5][3] = 100
    grid_test[5][5] = 100
    
    grid_test[0][3] = 30
    grid_test[1][2] = 31
    grid_test[1][3] = 3
    grid_test[1][4] = 31
    grid_test[2][3] = 30
    
    grid_test[2][5] = 30
    grid_test[3][4] = 31
    grid_test[3][5] = 3
    grid_test[3][6] = 31
    grid_test[4][5] = 30

    #print_matrix(grid_test)

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

    # # Create start of game
    # space_positions_test = [0,1,2,3,4,5,6,7,8]
    # block_positions_test = []

    blocks_dict_test = {'space': [0,1,2,3,4,5,6,7,8],
                        'reflect': [],
                        'refract': [3,7],
                        'opaque': []}

    place_blocks(image_start, blocks_dict_test,
                 WIDTH_TEST, MATRIX_SIZE_X_TEST, MATRIX_SIZE_Y_TEST)

    # win.mainloop()

    # place_start_point(image_start, start_test,
    #                   WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # place_targets(image_start, targets_test,
    #               WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)

    # ## Solve puzzle
    print(targets_test)
    test_laz_dict = {}
    test_laz_dict['lazor1'] = [start_test, direction_test]
    lazor_grid_results, lazor_positions_test, lazor_positions_test_dict, targets_test_results = \
        lazor(grid_test, test_laz_dict, targets_test)
    print(targets_test_results)
    print(lazor_positions_test)
    print_matrix(lazor_grid_results)

    draw_lazor(image_start, lazor_positions_test,
               WIDTH_TEST, MATRIX_SIZE_X_TEST, DIAMETER_TEST)
    
    win.mainloop()
    # block_positions_test = [3,7]

    # ## Solve Button
    # image_button = Button(win, text="Solve Puzzle",
    #                       command=lambda: display_solution(space_positions_test,block_positions_test,
    #                                                    start_test,targets_test,lazor_grid_results))
    # image_button.grid(row=0, column=1, padx=50)
    
    
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

    grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets = openlazorfile('test.bff')
    num_grid, possible_pos = create_grid(grid_list)
    permutations_grids = permutations_blocks(num_grid, possible_pos, num_refl_block, num_opq_block, num_refr_block)
    print(len(permutations_grids))
    solution_grid, lazor_grid, lazor_positions, lazor_positions_dict, targets_results = solve_puzzle(permutations_grids, laz_dict, targets)
    print("\n")
    print("Start of Mitch testing")
    print(targets)
    print(laz_dict)
    print_matrix(solution_grid)
    print("\n")
    print_matrix(lazor_grid)
    print(targets_results)
    print(lazor_positions)
    print(lazor_positions_dict)

    # print_matrix(grid_list)
    # print(num_refl_block)
    # print(num_opq_block)
    # print(num_refr_block)
    # print(laz_dict)
    # print(targets)

    # tiny_5 = openlazorfile('tiny_5.bff')[0]
    # print(tiny_5)
    # tiny_5_num_grid = create_grid(tiny_5)
    # print(tiny_5_num_grid)

    # print(tiny_5_num_grid)

    # lazor1 = laz_dict['lazor0']
    # print(lazor1)

    # grid, positions, results = lazor(tiny_5_num_grid, lazor1[0], lazor1[1], targets)
    # print_matrix(grid)
    # print(positions)
    # print(results)

    # tiny_5_num_grid = create_grid(grid_list)
    # # print(tiny_5_num_grid)
    # print_matrix(tiny_5_num_grid)

    # block = Refract_Block()
    # print("\n")
    # print_matrix(block.set_position((1,1), tiny_5_num_grid))
    # print("\n")
    # print_matrix(block.remove_position((1,1), tiny_5_num_grid))

#####
    # # grid_list, num_refl_block, num_opq_block, num_refr_block, laz_dict, targets = openlazorfile('test.bff')
    # # # print_matrix(grid_list)
    # # # print("\n")
    # # test_num_grid = create_grid(grid_list)
    # # print_matrix(test_num_grid)



    # # reflect_block = Reflect_Block()
    # # # #refract_block = Refract_Block()
    # # print("\n")
    # # print_matrix(reflect_block.set_position((3,3), test_num_grid))
    # # print("\n")
    # #print_matrix(reflect_block.remove_position((3,3), test_num_grid))
    # #print("\n")
    # #print_matrix(refract_block.set_position((3,3), test_num_grid))
    # #print("\n")
    # #print_matrix(refract_block.remove_position((3,3), test_num_grid))