"""
Tanner Wendland
8/23/18
CS5401
Missouri University of Science and Technology
"""
import configparser
import random
import sys
import math
from puzzle import Light_puzzle

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    #Use another config file
    config.read(sys.argv[1])
else:
    config.read("configs/default.cfg")

"""
Parameters: None
Return: None
Update map function. The purpose of this function is create a list of all the tiles that are bulbs, remove the bulbs
and then place the bulbs back to their original spot. This is so that when generating the puzzle and a wall is placed, the bulb
will not shine through the wall
"""
def update_map(puzzle):
    #get where we put the bulbs
    bulb_panels = puzzle.get_all_bulbs()
    #clear all the bulbs
    puzzle.clear_map()
    #for each of the bulbs that were placed, put thel back.
    for panel in bulb_panels:
        #update the panels. panel[0]is the row and panel[1] is the col
        puzzle.set_bulb(panel)

"""
Parameters: None
Return: Light_puzzle Object
Generate map function. This function will generate a map that is guarteed to be solvable since the function exist when the map has no white cells left,
bulbs are only placed on cells that are unlit so no bulbs shine on each other. The wall values are only placed once the map is full, and the value is placed
depending on the bumber of bulbs adjacent to it after the map is filled.

Note: Due to how this program generates puzzles, all puzzle generated within a partiular experiment will have the same number of wall panels
since the config file used a percentage of what cells should walls.
"""
def generate_map():
    try:
        rows = int(config.get('GENERATOR', 'rows'))
    except configparser.Error:
        print("Error: rows field under [GENERATOR] is missing from config file. Exiting.")
        sys.exit()
    try:
        cols = int(config.get('GENERATOR', 'cols'))
    except configparser.Error:
        print("Error: cols field under [GENERATOR] is missing from config file. Exiting.")
        sys.exit()
    try:
        wall_percent = float(config.get('GENERATOR', 'wall_percent'))
    except configparser.Error:
        print("Error: base_wall_persent field under [GENERATOR] is missing from config file. Exiting.")
        sys.exit()
    number_of_walls = math.floor(rows*cols*wall_percent / 100)
    puzzle = Light_puzzle(rows, cols)

    #This map cannot have any bulbs placed in it at all.
    if wall_percent >= 100 or number_of_walls == rows*cols:
        print("Error: No Light bulbs can be placed since the puzzle is made up of only walls. \nPlease reduce the wall percent value in your config file. Exiting.")
        sys.exit()

    #place a light so that the map is guarteed to have aat least 1 bulb placed
    random_light_panel = puzzle.get_random_panel()
    puzzle.set_bulb(random_light_panel)


    #now we have to randomly place walls
    while True:
        random_panel = puzzle.get_random_panel()
        #Reobtain rows and cols if they're a wall already or if they're the bulb we placed
        while puzzle.is_wall(random_panel) == True or puzzle.is_bulb(random_panel) == True:
            #Make another random panel
            random_panel = puzzle.get_random_panel()
        puzzle.set_wall(random_panel, 5)
        # If we have reached our baseline number of walls, stop making more walls.
        if puzzle.walls >= number_of_walls:
            break

    #update the map so that lights don't shine past walls now
    update_map(puzzle)

    #Place bulbs and walls randomly again until there are no unlit panels. Then numbers for the walls will be placed.
    while True:
        #Redo the list
        puzzle.init_unlit_panel_list()
        #gets all panels that are not lit and that are not walls. (no bulbs implied through lit property)
        unlit_panels = puzzle.get_all_unlit()
        #No more unlit panels means that we're done
        if not len(unlit_panels):
            break
        random_panel = random.choice(unlit_panels)
        new_obj_chance = random.random()
        #This is a pretty small change to add a new bulb to the game
        if new_obj_chance < 0.03:
            puzzle.set_bulb(random_panel)


    #Next I am going place the numbers of the walls based on their surroundings
    wall_panels = puzzle.get_all_walls()
    for wall in wall_panels:
        #start at zero
        wall_value = 0
        adjacent_panels = puzzle.get_adjacent_panels(wall)
        for neightbor in adjacent_panels:
            #If there is a bulb next to the wall, then its value can be increded by one
            if puzzle.is_bulb(neightbor) == True:
                wall_value += 1
        #50% chance to change this into a valued wall
        if random.random() >= 0.5:
            puzzle.set_wall(wall, wall_value)


    #finally done generating. Clear the board.
    puzzle.clear_map()
    #Done generating, so greate the list of white panels
    puzzle.init_white_panel_list()
    #Update the unlit list for the final time. 
    puzzle.init_unlit_panel_list()
    return puzzle
