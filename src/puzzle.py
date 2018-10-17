"""
Tanner Wendland
8/21/18
CS5401
Missouri University of Science and Technology
"""

import configparser
import sys
import random
from panels import Puzzle_panel
from panels import DEFAULT_WALL
from shine_list import shine_list

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    config.read(sys.argv[1]) #Use another config file
else:
    config.read("configs/default.cfg")

class Light_puzzle:
    """
    Game object for the Light Bulb Puzzle.
    Parameters: (row, col) where row and col are both integers.


    This puzzle objects holds a 2d list of panel objects that act as a map for ths game, and all
    game informations such as if the panel is a wall or not is stored in the panel object. There are get functions inplace to obtain lists of
    panel objects such as obtaiing all unlit panels, obtaining all panels that have bulbs places at them, etc...
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.walls = 0 #no walls in the beginning
        self.white_panels = [] #List of white panels, that are not bulbs. Used for random search.
        self.bulb_panels = []
        self.unlit_panels = []
        self.map = [[Puzzle_panel(i, j) for j in range(self.cols)] for i in range(self.rows)]

    """
    Paramaters: (row, col) where row and col are both integers.
    Return: panel object from map
    Get panel function. This function simply returns the panel object at the indicies passed.
    """
    def get_panel(self, row, col):
        return self.map[row][col]

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    """
    Parameters: (panel, value) where panel is a panel object in the map, and value is an integer.
    Return: none
    This function turns the panel passed into the function that is located in the map into a wall, with the wall value set as the parameter value
    """
    def set_wall(self, panel, value):
        if(panel.is_wall() == False):
            self.walls += 1
        panel.set_wall() #Set this coordinate to a wall
        panel.set_wall_value(value) #Set that walls value

    """
    Parameters: (panel) where panel is a panel objects in the map
    Return: Boolean
    This fucntion simply returns True if the panel seltected is a wall, other wise it is not a wall
    """
    def is_wall(self, panel):
        if panel.is_wall() == True:
            return True
        else:
            return False

    """
    Parmeters: (panel) where panel is a panel object in map
    Return: integer
    This function simply returns the wall value of the panel
    """
    def get_wall_value(self, panel):
        return panel.wall_value()

    def get_num_walls(self):
        return self.walls

    """
    Parameters: (panel) where panel is a panel object that is in map.
    Return: Boolean
    This function sets a bulb in the panel passed and then lights up panels according that are in the same row and col, but not
    passing through wall panels.
    """
    def set_bulb(self, panel):
        self.bulb_panels.append(panel);
        row = panel.get_row()
        col = panel.get_col()
        if(self.map[row][col].is_bulb() == False):
            self.map[row][col].light() #The panels with bulbs are lit
            self.map[row][col].set_bulb() #This panel is now a bulb
            self.map[row][col].inc_lit_value()
            #If the length is zero, don't remove a white panel since the program is still
            #generating the puzzle map. This list has elements in it when the puzzle is done generating
            try:
                self.white_panels.remove(self.map[row][col]) #This panel is no longer able to be selected for a solution
            except ValueError:
                pass
            #Sometime due to crossover bulbs can now shine on each other, so now if this panel is already lit, place the bulb any way and don't remove from unlit_panels
            try:
                self.unlit_panels.remove(self.map[row][col])
            except ValueError:
                pass
            #self.map[row][col].lit_value += 1

            #light squares going to the right of the bulb first
            for i in range(col, self.cols):
                if(self.map[row][i].is_wall() == False):
                    if self.map[row][i] != panel:
                        self.map[row][i].light()
                        self.map[row][i].inc_lit_value()
                        if len(self.unlit_panels) != 0:
                            try:
                                self.unlit_panels.remove(self.map[row][i])
                            #This was already removed from the unlit_panel list because panels can be lit by different bulbs
                            except ValueError:
                                pass
                else:
                    break;

            #light panels to the left of the bulb, go backwards. range function is exclusive so to have 0 -1 needs to be the stoppping param
            for i in range(col, -1, -1):
                if(self.map[row][i].is_wall() == False):
                    if self.map[row][i] != panel:
                        self.map[row][i].light()
                        self.map[row][i].inc_lit_value()
                        if len(self.unlit_panels) != 0:
                            try:
                                self.unlit_panels.remove(self.map[row][i])
                            except ValueError:
                                pass
                else:
                    break;

            for j in range(row, self.rows): #lights above above the bulb
                if(self.map[j][col].is_wall() == False):
                    if self.map[j][col] != panel:
                        self.map[j][col].light()
                        self.map[j][col].inc_lit_value()
                        if len(self.unlit_panels) != 0:
                            try:
                                self.unlit_panels.remove(self.map[j][col])
                            except ValueError:
                                pass
                else:
                    break;

            for j in range(row, -1, -1): #lights below below the bulb
                if(self.map[j][col].is_wall() == False):
                    if self.map[j][col] != panel:
                        self.map[j][col].light()
                        self.map[j][col].inc_lit_value()
                        if len(self.unlit_panels) != 0:
                            try:
                                self.unlit_panels.remove(self.map[j][col])
                            except ValueError:
                                pass
                else:
                    break;


    """
    Paramaters: (panel) where panel is a panel object from the map.
    Return: Boolean
    This function simply retursn true of the panel passed is a bulb, otherwise return false.
    """
    def is_bulb(self, panel):
        if panel.is_bulb() == True:
            return True
        else:
            return False

    def remove_bulb(self, panel):
        row = panel.get_row()
        col = panel.get_col()
        panel.remove_bulb()
        panel.dec_lit_value()
        if panel.get_lit_value() <= 0:
            panel.unlight()
        #No longer a bulb
        try:
            self.bulb_panels.remove(panel);
        except:
            #Something when wrong...
            print("ERROR")
            sys.exit()


        #We need to remove the bulb. If the After removing the bulb and and recrementing the lit value, if the lit value is 0 (not lit by another bulb) then the bulb is no longer lit.
        #Goto the right first
        for i in range(col, self.cols):
            if(self.map[row][i].is_wall() == False):
                #Dont count this if it is the bulb that we removed
                    if self.map[row][i] != panel:
                        self.map[row][i].dec_lit_value()
                        #If the lit value is 0, we can say the panel is no longer lit
                        if self.map[row][i].get_lit_value() <= 0:
                            self.map[row][i].unlight()
                            self.unlit_panels.append(self.map[row][i])
            else:
                break;
        #check left
        for i in range(col, -1, -1):
            if(self.map[row][i].is_wall() == False):
                #Dont count this if it is the bulb that we removed
                if self.map[row][i] != panel:
                    self.map[row][i].dec_lit_value()
                    #If the lit value is 0, we can say the panel is no longer lit
                    if self.map[row][i].get_lit_value() <= 0:
                        self.map[row][i].unlight()
                        self.unlit_panels.append(self.map[row][i])
            else:
                break;
        #check up
        for j in range(row, -1, -1):
            if(self.map[j][col].is_wall() == False):
                #Dont count this if it is the bulb that we removed
                if self.map[j][col] != panel:
                    self.map[j][col].dec_lit_value()
                    #If the lit value is 0, we can say the panel is no longer lit
                    if self.map[j][col].get_lit_value() <= 0:
                        self.map[j][col].unlight()
                        self.unlit_panels.append(self.map[j][col])
            else:
                break;
        #finally check down
        for j in range(row, self.rows):
            if(self.map[j][col].is_wall() == False):
                #Dont count this if it is the bulb that we removed
                if self.map[j][col] != panel:
                    self.map[j][col].dec_lit_value()
                    #If the lit value is 0, we can say the panel is no longer lit
                    if self.map[j][col].get_lit_value() <= 0:
                        self.map[j][col].unlight()
                        self.unlit_panels.append(self.map[j][col])
            else:
                break;



    """
    Paremeters: None
    Return: None
    This function populates the list of white panels. This function is only called once and thats when the puzzle is done generating.
    This white_panels list of a list of all the white panels that are not bulbs. The panel is removed from the list when a bulb is placed.
    This is here so there is not an O(m*n) algorithm when searching for a random white panel when solving each time we want a new random panel.
    """
    def init_white_panel_list(self):
        for j in range(self.cols):
            for i in range(self.rows):
                #If the panel isn't a wall and isn't a bulb, it can be selected
                if self.map[i][j].is_bulb() == False and self.map[i][j].is_wall() == False:
                    self.white_panels.append(self.map[i][j]) #send in (row, col) format


    """
    Paremeters: None
    Return: None
    This function populates the list of unlit panels. This function is defined like init_white_panel_list because it was used in random search so that random search would find valid solutions faster
    But using this function for random search has some unintended consequences. If the user is not using the option to enforce wall values, then random search would find a global optimum
    almost immediately. This did not seem like a problem until the evotinary algorithm. Since crossover can create invalid solutions by making bulbs shine on each other,
    the first generation would almost always be worse than their parents. This compounded with k tournement styled survival could mean that you are killing off high fitness population members
    since it is unliekly that you select all the children in the survival tourament.
    """
    def init_unlit_panel_list(self):
        self.unlit_panels.clear()
        for j in range(self.cols):
            for i in range(self.rows):
                #If the panel isn't a wall and isn't a bulb, it can be selected
                if self.map[i][j].is_lit() == False and self.map[i][j].is_wall() == False:
                    self.unlit_panels.append(self.map[i][j])


    """
    Paramters: None
    Return: list of panels
    Thus function returns a list of all the white panels (excluding bulbs) in the map
    """
    def get_all_white_panels(self):
        return self.white_panels

    """
    Paramters: none
    Returns: list of panels
    This function finds all the panels that are unlit and returns a list of them
    """
    def get_all_unlit(self):
        return self.unlit_panels

    """
    Paramaters: none
    Returns: list of panels
    This function finds all the panels that are lit and returns a list of them
    """
    def get_all_lit(self):
        panel_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j].is_lit() == True:
                    panel_list.append(self.map[i][j])
        return panel_list

    """
    Paramaters: none
    Returns: list of panels
    This function finds all the panels that are bulbs and returns a list of them
    """
    def get_all_bulbs(self):
        return self.bulb_panels;
    """
    Paramters: none
    Returns: list of panels
    This function finds all the panels that are wall and returns a list of them
    """
    def get_all_walls(self):
        panel_list = []
        for j in range(self.cols):
            for i in range(self.rows):
                if self.map[i][j].is_wall() == True:
                    panel_list.append(self.map[i][j])
        return panel_list

    """
    Paramters: (panel) where panel is a panel object from the map
    Returns: list of panels
    This function finds all of the neighbors (directly adjacent panels) for the panel passes, and creates a list of these panels
    """
    def get_adjacent_panels(self, panel):
        row = panel.get_row()
        col = panel.get_col()
        panel_list = []
        if row != 0:
            panel_list.append(self.map[row-1][col])
        if row != self.rows-1:
            panel_list.append(self.map[row+1][col])
        if col != 0:
            panel_list.append(self.map[row][col-1])
        if col != self.cols-1:
            panel_list.append(self.map[row][col+1])
        return panel_list

    """
    Parameters: none
    Return: panel from map
    This function simply returns a random panel from the map
    """
    def get_random_panel(self):
        row = random.randint(0, self.rows-1)
        col = random.randint(0, self.cols-1)
        return self.map[row][col]


    """
    Parameters: (panel) where panel is a panel object from the map
    Return: boolean
    This function checks to see the wall panel passed has to currect number of bulbs in the neigbor panels. Returns True if the wall is valid, but false
    if the wall is invalid
    """
    def  check_wall(self, panel):
        adjacent_bulbs = 0
        row = panel.get_row()
        col = panel.get_col()
        #check to the left
        if row != 0 and self.map[row-1][col].is_bulb() == True:
            adjacent_bulbs+=1
        #check to the right
        if row != self.rows-1 and self.map[row+1][col].is_bulb() == True:
            adjacent_bulbs+=1
        #check below the wall
        if col != 0 and self.map[row][col-1].is_bulb() == True:
            adjacent_bulbs+=1
        #check above the wall
        if col != self.cols-1 and self.map[row][col+1].is_bulb() == True:
            adjacent_bulbs+=1
        #If the values are not the same, then return 0 because the solution fails
        if adjacent_bulbs != self.map[row][col].wall_value():
            return False
        return True

    """
    Paramters: (panel) where panel is a panel object from the map
    Return: boolean
    Thus function checks to see of the bulb set at the panel passes shines directly on to any other bulbs in the puzzle. Returns True if the bulb placement is valid
    and false if the bulb placement is invalid.
    """
    def check_bulb(self, panel):
        row = panel.get_row()
        col = panel.get_col()
        #light squares going to the right of the bulb first
        for i in range(col, self.cols):
            # If we run into a wall, we're done looking in this direction
            if self.map[row][i].is_wall() == True:
                break
            #If we run into a bulb, return false
            if self.map[row][i].is_bulb() == True and self.map[row][i] != panel:
                return False
        #light panels to the left of the bulb, go backwards. range function is exclusive so to have 0 -1 needs to be the stoppping param
        for i in range(col, -1, -1):
            if self.map[row][i].is_wall() == True:
                break
            if self.map[row][i].is_bulb() == True and self.map[row][i] != panel:
                return False
        #lights above above the bulb
        for j in range(row, -1, -1):
            if self.map[j][col].is_wall() == True:
                break
            if self.map[j][col].is_bulb() == True and self.map[j][col] != panel:
                return False
        #lights below below the bulb
        for j in range(row, self.rows):
            if self.map[j][col].is_wall() == True:
                break
            if self.map[j][col].is_bulb() == True and self.map[j][col] != panel:
                return False

        return True #This bulb does not shine on any other bulb

    """Shine List"""
    def repair_shine_list(self):
        current_shine_list = []
        for bulb in self.bulb_panels:
            #lets check to see if this bulb is shining on any other bulb
            row = bulb.get_row()
            col = bulb.get_col()
            #List of bulbs it shines on
            this_shines_on = []
            #First, lets look right
            for i in range(col, self.cols):
                if self.map[row][i].is_wall() == True:
                    break
                #If we run into a bulb, add it to the list
                if self.map[row][i].is_bulb() == True and self.map[row][i] != bulb:
                    this_shines_on.append(self.map[row][i])
            #lets look left
            for i in range(col, -1, -1):
                if self.map[row][i].is_wall() == True:
                    break
                #If we run into a bulb, add it to the list
                if self.map[row][i].is_bulb() == True and self.map[row][i] != bulb:
                    this_shines_on.append(self.map[row][i])
            #Look up
            for j in range(row, -1, -1):
                if self.map[j][col].is_wall() == True:
                    break
                #If we run into a bulb, add it to the list
                if self.map[j][col].is_bulb() == True and self.map[j][col] != bulb:
                    this_shines_on.append(self.map[j][col])
            #Look down
            for j in range(row, self.rows):
                if self.map[j][col].is_wall() == True:
                    break
                #If we run into a bulb, add it to the list
                if self.map[j][col].is_bulb() == True and self.map[j][col] != bulb:
                    this_shines_on.append(self.map[j][col])

            #Create a the shine_list object
            if len(this_shines_on) > 0:
                current_shine_list.append(shine_list(bulb, this_shines_on))
        return current_shine_list





    """
    Parameters: none
    Return: none
    This function simply clears the map of any panels that are not walls, setting their lit and bulb properties to false.
    """
    def clear_map(self):
        self.bulb_panels.clear() #clear the bulb list
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j].is_wall() == False:
                    self.map[i][j].remove_bulb()
                    self.map[i][j].unlight()
                    self.map[i][j].clear_lit_value()

    """
    Paramters: none
    Returns: integer

    Thius function simply acts as a wrapper that chooses the fitness fucntion to used based on the users config.
    """
    def verify_solution(self):
        try:
            if config.get("PARAMETERS", "penalty_function") == 'yes':
                return self.penalty_fitness_function()
            else:
                return self.orginal_fitness_function()
        except configparser.Error:
            print("Error: penalty_function option under [PARAMATERS] is missinf from config file. Exiting.")
            sys.exit()


    """
    Paramters: none
    Returns: integer
    This function checks to see if the current map setup is valid by checking 2 things. First if the panel is a wall, then is the neightbor bulb constraint fulfilled
    if the wall has a value that is not 5. Also if the panel is a bulb, does this bulb shine on any other bulb in the puzzle. If both of these requirements are
    met, then the returned integer is the fitness value where the fitness value is the number of white panels lit currently in the puzzle.

    The wall value requirement can be laxed if the users config file states that it is not to enforce the wall values.
    """
    def orginal_fitness_function(self):
        #Boolean option to determine if we enfore the wall contraint, used for random search
        enforce_wall_value = True
        try:
            if config.get('PARAMETERS', 'enforce_wall_value') == 'no':
                enforce_wall_value = False
        except configparser.Error:
            print("Error: enforce_wall_value field under [PARAMETERS] is missing from config file. Exiting")
            sys.exit()
        health_value = 0
        #iterate through the map
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                current_panel = self.map[i][j]
                if current_panel.is_wall() == False and current_panel.is_lit() == True:
                    health_value+=1
                #check if wall have the correct number of adjacent bulbs if the value isn't 5. Check the wall using check_wall()
                if enforce_wall_value == True and current_panel.is_wall() == True and current_panel.wall_value() != DEFAULT_WALL and self.check_wall(current_panel) == False:
                    return 0
                #Check of this bulb shines on another bulb
                if current_panel.is_bulb() == True and self.check_bulb(current_panel) == False:
                    return 0
        return health_value

    """
    Paramters: none
    Returns: integer
    Similar to the oprginal fitness function, but a penalty will be added based on the number of walls that their containts are not satisfied (if enforced) and the numebr of bulbs
    that shine on each other. The penalty will be be the sum of these two numbrs times a penalty coefficient.
    """
    def penalty_fitness_function(self):
        #Boolean option to determine if we enfore the wall contraint, used for random search
        enforce_wall_value = True
        try:
            if config.get('PARAMETERS', 'enforce_wall_value') == 'no':
                enforce_wall_value = False
        except configparser.Error:
            print("Error: enforce_wall_value field under [PARAMETERS] is missing from config file. Exiting.")
            sys.exit()
        #Obtain floating points penalty coefficient
        try:
            penalty_coefficient = float(config.get('PARAMETERS', 'penalty_coefficient'))
        except configparser.Error:
            print("Error: penalty_function field uinder [PARAMATERS] is msising from config file. Exiting.")
            sys.exit()
        health_value = 0
        penalty = 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                current_panel = self.map[i][j]
                if current_panel.is_wall() == False and current_panel.is_lit() == True:
                    health_value+=1
                #check if wall have the correct number of adjacent bulbs if the value isn't 5. Check the wall using check_wall().
                if enforce_wall_value == True and current_panel.is_wall() == True and current_panel.wall_value() != DEFAULT_WALL and self.check_wall(current_panel) == False:
                    penalty+=1
                #Check of this bulb shines on another bulb, if so increment panalty
                if current_panel.is_bulb() == True and self.check_bulb(current_panel) == False:
                    penalty+=1
        #This could maybe be below 0, so if it is then jsut make it zero
        if health_value-penalty*penalty_coefficient > 0:
            return int(health_value-penalty*penalty_coefficient)
        else:
            # If all solutions are invlaid, returns 0 to prevent fitness_prop from breaking.
            return 1


    """
    Parameters: None
    Return: Interger
    This function returns an interger of the number of bulbs that shine on each other. The function for getting the list of bulbs that shine on each other is
    already implmented because of the repair function.
    """
    def shine_fitness(self):
        shine_list = self.repair_shine_list()
        return len(shine_list)


    """
    Parmeters: None
    Return: Integer
    This function returns the number of wall violations.
    """
    def wall_fitness(self):
        wall_violations = 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                current_panel = self.map[i][j]
                if current_panel.is_wall() == True and current_panel.wall_value() != DEFAULT_WALL and self.check_wall(current_panel) == False:
                    wall_violations+=1
        return wall_violations


    """
    Paramters: none
    Return: String
    This function simply returns a string that repersents the current map status. This is for aid to tell if a solution file is correct or if the
    algorithm for verfiying a solution is correct. _
    Key:
    _: blank white panel
    +: lit white panel
    B: bulb
    W: wall with no value
    0-4: wall with the value of that integer
    """
    def map_image(self):
        string = ''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j].is_wall() == False and self.map[i][j].is_bulb() == False and self.map[i][j].is_lit() == False:
                    string += '_'
                elif self.map[i][j].is_wall() == False and self.map[i][j].is_bulb() == False and self.map[i][j].is_list() == True:
                    string += '+'
                elif self.map[i][j].is_bulb() == True:
                    string += 'B'
                elif self.map[i][j].is_wall() == True:
                    if(self.map[i][j].wall_value() < DEFAULT_WALL):
                        string += str(self.map[i][j].wall_value())
                    else:
                        string += 'W'
            string += '\n'
        return string
