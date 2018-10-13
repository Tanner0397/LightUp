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
Parameters: (seed) where seed is a floating point number that represent the seed used for the random number generator
Return: none
This function writes some information to the log file in the config file used. Output to log here depends on if the user used a
data file to read a map or of the program generated a map randomly.
"""
def write_log_intializer(seed):
    try:
        log_file_name = config.get('PATHS', 'log_path')
    except configparser.Error:
        print("Error: log_path field under [PATHS] is missing from config file. Exiting.")
        sys.exit()
    with open(log_file_name, 'w') as file:
        if config.get('GENERATOR', 'generate') == 'no': #we're using a datefile
            if(len(sys.argv) >= 3):
                file.write("Date File: " + sys.argv[2] + '\n')
            else:
                file.write("Date File: " + config.get('PATHS', 'file_path') + '\n')
            file.write("Seed: " + str(seed) + '\n')
        else: #This was generated
            file.write("Seed: " + str(seed) + '\n')
            file.write("Rows: " + config.get('GENERATOR', 'rows') + '\n')
            file.write("Cols: " + config.get('GENERATOR', 'cols') + '\n')
            file.write("Wall Percent: " + config.get('GENERATOR', 'wall_percent') + '\n')
        file.write("Enforcement of Wall Values: " + config.get('PARAMETERS', 'enforce_wall_value') + '\n')
        file.write("Forced Wall Validity: " + config.get("PARAMETERS", "forced_wall_validity") + '\n')
        file.write("Penalty Function: " + config.get("PARAMETERS", "penalty_function") + '\n')
        file.write("Penalty Coefficient: " + config.get("PARAMETERS", "penalty_coefficient") + '\n')
        file.write("Survival Stategy: " + config.get("EA_PARAMATERS" ,"survival_strategy") + '\n')
        file.write("Survival Selection: " + config.get("EA_PARAMATERS" ,"survival_selection") + '\n')
        file.write("Parent Selection: " + config.get("EA_PARAMATERS", "parent_selection") + '\n')
        file.write("Convergence Termination: " + config.get("EA_PARAMATERS", "convergence_termination") + '\n')
        file.write("n Point Crossover: " + config.get("EA_PARAMATERS", "n_point_crossover") + "\n")
        file.write("n Points: " + config.get("EA_PARAMATERS", "n_points") + "\n")
        file.write("mu: " + config.get("EA_PARAMATERS", "mu") + '\n')
        file.write("lambda: " + config.get("EA_PARAMATERS", "lambda") + '\n')
        file.write("Parent Tournament Size: " + config.get("EA_PARAMATERS", "tournament_size_parent") + '\n')
        file.write("Survival Tournament Size: " + config.get("EA_PARAMATERS", "tournament_size_survival") + '\n')
        file.write("Mutation Rate: " + config.get("EA_PARAMATERS", "mutation_rate") + '\n')
        file.write("Insert Mutation Rate: " + config.get("EA_PARAMATERS", "insert_mutation_rate") + '\n')
        file.write("Evaluations Until Termination: " + config.get("EA_PARAMATERS", "evals_until_term") + '\n')
        file.write("Termination Convergence Criterion: " + config.get("EA_PARAMATERS", "termination_convergence_criterion") + '\n')
        file.write("Repair Function: " + config.get("EA_PARAMATERS", "repair_function") + '\n')
        file.write('Results Log\n')

"""
Paramters: (run_id) where run_id is an integer
Return: None
This function simply writes to the log file a new block for puzzle solving runs
"""
def start_new_block(run_id):
    log_file_name = config.get('PATHS', 'log_path')
    with open(log_file_name, 'a') as file:
        file.write('\nRun ' + str(run_id) + '\n')

"""
Paramtes: (evals, fitness) where eval and fitness are both integers
Return: none
This function simply writes to the log the current evaluation in the run with the fitness value passes
"""
def new_entry(evals, average_fitness, best_fitness):
    log_file_name = config.get('PATHS', 'log_path')
    with open(log_file_name, 'a') as file:
        file.write(str(evals) + '\t' + str(average_fitness) + "\t" + str(best_fitness) + '\n')
