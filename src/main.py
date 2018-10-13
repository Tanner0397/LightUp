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
from datetime import datetime
from evolution import Evolution_Instance
from population_member import Population_Member

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
    #Storage for the best fitness level, throughout all runs. All puzzle have the same number of white panels
    best_fitness = -1

    for run_id in range(runs):
        print("Startin Run " + str(run_id+1))
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
        #---------START SOLVING PUZZLE FOR THIS RUN------------
        # best_member = solver.evolution_algorithm(puzzle)
        # current_fitness = best_member.verify_solution()
        # #Store the solution
        # if current_fitness > best_fitness:
        #     solution_writer.write_solution(best_member)
        #     best_fitness = current_fitness
        #---------END SOLVING-----------------------


        test_inst = evolution.Evolution_Instance(puzzle)
        print("Testing. Population Size {}".format(len(test_inst.population)))
        test_inst.dom_table.print_table_info()


        #-------TESTING-----------
        #-----------END TESTING--------


if __name__ == "__main__":
    main()
