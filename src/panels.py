"""
Tanner Wendland
8/21/18
CS5401
Missouri University of Science and Technology
"""

"""
Puzzle Panel object. Puzzle object will have a 2d list of this object. This panel is either a wall or not a wall. If this panel is sa wall it either has a value
or does not have a value. If this panel is not a wall it is known as a white panel. White panels can either be lit or unlit, and be a bulb or bot a bulb.
Panels that are bulbs are lit automatically and panels that are not bulbs but are lit have a bulb that is wither in the same row or col as them.

This object keeps track of its position in the map so that it is easier to obtain it location when traversing the map in the functions in puzzle that use the
indicies of the panel to check things such wen placing a bulb the panels sharing the same row and col are lit. This avoids an O(m*n) time search everytime
we need to look for a panel.
"""
DEFAULT_WALL = 5



class Puzzle_panel:
    #cdef bool_t lit, bulb, wall
    #cdef int wall_val, row, col, lit_value
    def __init__(self, rw, cl):
        self.lit = False #all panels are intinally not lit
        self.bulb = False; #Has no bulb inintally
        self.wall = False #all panels are not walls by default
        self.wall_val = -1 #-1 because the panel is initially not a walls
        self.row = rw #set row
        self.col = cl #set col
        self.lit_value = 0

    """
    Parameters: None
    Return: None
    Set wall function. This function simply turns this objects wall boolean value to true.
    """
    def set_wall(self):
        self.wall = True

    def set_bulb(self):
        self.bulb = True

    def remove_bulb(self):
        self.bulb = False

    def is_bulb(self):
        return self.bulb

    def light(self):
        self.lit = True

    def unlight(self):
        self.lit = False

    def is_wall(self):
        return self.wall

    def is_lit(self):
        return self.lit

    def wall_value(self):
        return self.wall_val

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_lit_value(self):
        return self.lit_value

    def inc_lit_value(self):
        self.lit_value += 1

    def dec_lit_value(self):
        self.lit_value -= 1

    def clear_lit_value(self):
        self.lit_value = 0

    """
    Parameters: (Value) where value is an integer
    Set wall value function. This function simply sets this panels wall value. The wall value of a wall determines how many adjacent bulbs need to be present
    when checkign a potential solution. The only excption is when the wall value is 5, which means that it is a wall that has no value of adjacent bulbs that need
    to be there, but may be there.
    """
    def set_wall_value(self, value):
        if value <= 5 and value >= 0:
            self.wall_val = value
        else:
            print("Invalid wall value number. Defaulting to 5 for blank wall panel")
            self.wall_val = 5

    def __str__(self):
        return ("(" + str(self.row) + ", " + str(self.col) + ")")

    # def __copy__(self):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     result.__dict__.update(self.__dict__)
    #     return result
    #
    # def __deepcopy__(self, memo):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     memo[id(self)] = result
    #     for k, v in self.__dict__items():
    #         setattr(result, k, copy.deepcopy(v, memo))
