"""
Tanner Wendland
8/24/18
CS5401
Missouri University of Science and Technology
"""


import configparser
import sys

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    config.read(sys.argv[1]) #Use another config file
else:
    config.read("configs/default.cfg")

"""
Paramters: (puzzle) where puzzle is a Light_puzzle object
Return: None
This function simply take a puzzle passes to it and generates the solution file as specified. The first entry is an integer that represents the number of columns
, and the second entry is an integer that represents the number of rows. The next rows tell locations of black cells (walls) and are in the format
 <col> <row> <value> where col and row and indexed at 1 and start from the bottom lefthand corner of the map. When the walls are done being listed
 the next entry is a single integer that is the fitness value of the the current puzzle passes. After the fitness value the rest of the
 file consist locations of bulbs in the map in <col> <row> formatting with and indexing scheme identical to how walls are represented
"""
def write_solution(puzzle):
    try:
        solution_file_name = config.get('PATHS', 'solution_path')
    except configparser.Error:
        print("Error: solution_path field under [PATHS] is missing from config file. Exiting.")
        sys.exit()
    try:
        solution_image_file_name = config.get('PATHS', 'solution_image')
    except configparser.Error:
        print("Error: solution_image field under [PATHS] is missing from config file. Exiting.")
        sys.exit()
    rows = puzzle.rows
    cols = puzzle.cols
    wall_panels = puzzle.get_all_walls() #Get all the walls to write down
    bulb_panels = puzzle.get_all_bulbs() #Get all the bulbs to write down
    health_value = puzzle.verify_solution() #obtain health value of the soln

    with open(solution_image_file_name, 'w') as file:
        map_image = puzzle.map_image()
        file.write(map_image)

    with open(solution_file_name, 'w') as file:
        file.write(str(cols) + '\n') #Format calls for cols first to be printed
        file.write(str(rows) + '\n')

        for wall in wall_panels: #For evyer wall in the walls list obtained, print it to the solution file
            row = wall.row
            col = wall.col
            wall_value = puzzle.get_wall_value(wall)
            file.write(str(col+1) + ' ' + str(puzzle.rows-row) + ' ' + str(wall_value) + '\n') #adjust col to be indexed at 1 and change rows to be flipped and index at 1

        file.write(str(health_value) + '\n')

        for bulb in bulb_panels: #For every bulb in the bulbs list, print it out in the soln file
            row = bulb.row
            col = bulb.col
            file.write(str(col+1) + ' ' + str(puzzle.rows-row) + '\n') #adjust col to be indexed at 1 and change rows to be flipped and index at 1
