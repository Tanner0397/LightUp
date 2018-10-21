"""
Tanner Wendland
8/21/18
CS5401
Missouri University of Science and Technology
"""
import map_reader
import copy
import sys
import map_generator
import configparser
import random
import solver
import solution_logger
import solution_writer
import evolution
import timeit
from datetime import datetime
from evolution import Evolution_Instance
from population_member import Population_Member
from evolution import dominates

from distutils.core import setup
from Cython.Build import cythonize

#Set up config file
config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    #Use another config file
    config.read(sys.argv[1])
else:
    config.read("configs/default.cfg")

"""
Main Method.
"""
def test_fx():
  print("test")

def main():
    #intialize seed, used later for log when showing time based seed.
    seed = 0


    #Prodeed to seed the program if the confiog ask for it.
    try:
        if(config.get('GENERATOR', 'seed') != ''):
            seed = float(config.get('GENERATOR', 'seed'))
            random.seed(seed)
        else:
            #use time for random number
            random.seed(datetime.now())
            #Generate a new seed so that we can record the seed used
            seed = random.random()
            #Apply new seed
            random.seed(seed)
    except configparser.Error:
        print("Error: seed field under [GENERATOR] is missing in config file. Exiting")
        sys.exit()

    #------------------SEEDING END----------------------
    #-------------------DO RUNS---------------------

    solution_logger.write_log_intializer(seed)
    try:
        runs = int(config.get('STATISTICS','runs'))
    except configparser.Error:
        print("Error: runs field under [STATISTICS] is missing from config file. Exiting.")
        sys.exit()
    try:
        evals = int(config.get('STATISTICS','evals'))
    except configparser.Error:
        print("Error: evals field under [STATISTICS] is missing from config file. Exiting.")
        sys.exit()
    #Storage of patero front
    best_patero_front = []

    for run_id in range(runs):
        print("Starting Run " + str(run_id+1))
        solution_logger.start_new_block(run_id+1)
        #------------GENERATE/READ A PUZZLE----------------
        #Puzzles are generated for each run of the program
        try:
            if config.get('GENERATOR', 'generate') == 'no':
                try:
                    #We have a user passed datafile
                    if(len(sys.argv) >= 3):
                        #Use another config file
                        filename = sys.argv[2]
                    else:
                        filename = config.get('PATHS', 'file_path')
                except configparser.Error:
                    print("Error: file_path field under [PATHS] is missing in config file. Exiting")
                    sys.exit()
                    #read the map based off a file
                puzzle = map_reader.read_map(filename)
            #Generare a puzzle
            else:
                #generate a random map
                puzzle = map_generator.generate_map()
        except configparser.Error:
            print("Error: generate filed under [GENERATOR] is missing from config file. Exiting")
            sys.exit()

        #---------ENDING PUZZLE GENERATION/READING--------------
        """
         The solution file should consist of the best Pareto front found in any run, where we count Pareto front
         P1 as better than Pareto front P2 if the proportion of solutions in P1 which dominate at least one solution in P2 is larger than the proportion of solutions in
         P2 which dominate at least one solution in P1.
        """
        #---------START SOLVING PUZZLE FOR THIS RUN------------
        current_patero_front = solver.evolution_algorithm(puzzle)
        #Store the solution
        if len(best_patero_front) != 0:
            #The number of of solutions in current that dominate at least 1 solution in the best patero front
            num_current_dominates = 0
            #The number of solutions in the best found patero front that dominate at least 1 solution in the cuurrent patero front
            num_best_dominates = 0
            #compute num dominates for both
            for current_member in current_patero_front:
                for best_member in best_patero_front:
                    #If the member in the currente patero front is better than a solution found this far, increse counter
                    if dominates(current_member, best_member):
                        num_current_dominates+=1
                        break
            for best_member in best_patero_front:
                for current_member in current_patero_front:
                    #if the member in the best sounf thus far is better than a soltion in the current parero front, increse counter
                    if dominates(best_member, current_member):
                        num_best_dominates+=1
                        break
            current_proportion = num_current_dominates
            best_proportion = num_best_dominates
            if(current_proportion >= best_proportion):
                best_patero_front = copy.deepcopy(current_patero_front)
                solution_writer.write_solution(best_patero_front)

        else:
            best_patero_front = copy.deepcopy(current_patero_front)
            solution_writer.write_solution(best_patero_front)
        #---------END SOLVING-----------------------


        # test_inst = evolution.Evolution_Instance(puzzle)
        # print("Testing. Population Size {}".format(len(test_inst.get_population())))
        # #test_inst.dom_table.print_table_info()
        # #test_inst.print_dom_levels()
        # start_time = timeit.default_timer()
        # test_parent = test_inst.select_parent()
        # end_time = timeit.default_timer()
        # print(end_time - start_time)
        # print("Parent Info. Fitness = {}, Shine = {}, Wall = {}, Dom Rank = {}".format(test_parent.get_fitness(), test_parent.get_shine_fitness(), test_parent.get_wall_fitness(), test_parent.get_domination_rank()))

        #-------TESTING-----------
        #-----------END TESTING--------


if __name__ == "__main__":
    main()
