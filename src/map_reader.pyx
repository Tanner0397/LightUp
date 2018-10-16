"""
Tanner Wendland
8/21/18
CS5401
Missouri University of Science and Technology
"""

import sys
from puzzle import Light_puzzle

"""
Parameters: (filename) where filename is a string for the filename used for reading the data file
Return: Light_puzzle object
This function reads the map from a file that is given either by the config file or bythe users command line argument. The first input of the file
is the number of columns, then the number of rows. The input for the wall is <col> <row> <value> however the spesification states that
col and row are bother indexed at 1 and starts at the bottom lefthand corner, so the numbers bust be adjuested. So <col-1> <puzzle.rows - row> <value>
is what it is changed to so that everything obeys pyhtons indexing scheme.
"""
def read_map(filename):
    with open(filename) as file:
        try:
            cols = int(file.readline())
            rows = int(file.readline())
            puzzle = Light_puzzle(rows, cols)

            #read the reast of the data file to create walls
            for line in file:
                col = line.split()[0]
                row = line.split()[1]
                wall_value = line.split()[2]
                """
                The input is column, row, wallvalue so values[0] is the column
                values[1] is the row, and values[2] is the wall value

                Subtract cols by 1 because pyhton indexes starting at zero
                Take the number of all rows and subtract the row specified since the generations format
                starts at the bottome lefthand corner
                """

                #Adjust values to be 0 indexed and flip the rows to start from the top at 0
                wall_row = puzzle.rows - int(row)
                #Adjust to be 0 indexed
                wall_col = int(col)-1

                #Get the panel at the row and col
                panel = puzzle.get_panel(wall_row, wall_col)
                #place wall at the panel and give it that wall value
                puzzle.set_wall(panel, int(wall_value))

            #reading map is done, genreate list of white panels
            puzzle.init_white_panel_list()
            puzzle.init_unlit_panel_list()
            return puzzle
        except:
            #We have a problem reading the file.
            print("Invalid Data File. Exiting")
            sys.exit()
