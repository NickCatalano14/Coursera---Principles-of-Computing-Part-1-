"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # 1. Create a new list of equal dimensions for the resulting list.
    newlist = [0] * len(line)
    last_merged = False

    # 2. Look for non-zero values, and will copy over to the next available entry of the resulting list.
       
    if len(line) < 2:
        return line

    for entry_index in range(0, len(line)):
        if line[entry_index] != 0:
            for re_index in range(0, len(newlist)):
                if newlist[re_index] == 0:
                    newlist[re_index] = line[entry_index]
                    last_merged = False
                    break
                elif newlist[re_index + 1] == 0:
                    if newlist[re_index] == line[entry_index] and last_merged is False:
                        newlist[re_index] = newlist[re_index] + line[entry_index]
                        last_merged = True
                        break

    return newlist


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self.reset()
        self._borders = {UP: [(0,col)for col in range(self._width)] ,
                   DOWN: [(self._height-1,col)for col in range(self._width)],
                   LEFT: [(row,0)for row in range(self._height)],
                   RIGHT: [(row,self._width-1)for row in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for i in range(self._width)] for j in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        steps = self._height
        changed = False
        
        old = []
        new = []
        if direction == RIGHT or direction == LEFT:
            steps = self._width
        
               
        for index in self._borders[direction]:
            
            old=[]
            for step in range(steps):
                row = index[0] + step * OFFSETS[direction][0] 
                col = index[1] + step * OFFSETS[direction][1]
                old.append(self._grid[row][col])

            new = merge(old)
            
            if old != new :
                changed = True
 
            
            for step in range(steps):
                row = index[0] + step * OFFSETS[direction][0]
                col = index[1] + step * OFFSETS[direction][1]
                self._grid[row][col]=new[step]
      

        if changed:
            self.new_tile()
        
        
        
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        flag = True

        while flag :
            col = random.randrange(self._width)
            row = random.randrange(self._height)
            if self._grid[row][col] == 0 :
                flag = False
                if random.random() <= .1 :
                    self._grid[row][col] = 4
                else :
                    self._grid[row][col] = 2 


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col] 


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


