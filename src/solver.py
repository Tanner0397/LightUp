"""
Tanner Wendland
8/26/18
CS5401
Missouri University of Science and Technology
"""

import random
import sys
import configparser
import solution_logger
import copy
from evolution import Evolution_Instance
from evolution import insert_into_dom_level
from population_member import Population_Member
from chromosome import chromosome

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    config.read(sys.argv[1]) #Use another config file
else:
    config.read("configs/default.cfg")

"""
Parameters: (puzzle) where puzzle is a Light_puzzle object
Return: Light_puzzle object
This is a random search algorithm, this attempts to solve the puzzle completly randomly with no game knowledge except knowing that it can only
place a bulb in a panel once and that bulbs can only be placed in white panels.
"""
def random_search(puzzle):
    while True:
        #The base chance that the algorithm will place a light. The larger the number, the larger the change the algorithm will place a bulb
        place_chance = random.random()
        while True:
            unlit_list = puzzle.get_all_white_panels()
            try:
                #Get an unlit panel. Chooseing unlit panels avoid bulbs shining on each other.
                random_white_panel = random.choice(unlit_list)
            #If unlit list is empty, we can't place a bulb
            except IndexError:
                break
            #Set the light bulb and then stop the inner Loop, and then decide
            #If the place_change is greater than the number generated, place a new bulb.
            if random.random() < place_chance:
                puzzle.set_bulb(random_white_panel)
                break
        #10% chance to stop searching
        if random.randint(0, 10) == 0:
            return puzzle

"""
Parameters: (puzzle) where puzzle is a Light_puzzle object
Return: Light_puzzle object
This function attempts to solve the puzzle randomly, but can use game knowledge in order to solve. Mostly to determine that if bulbs can be placed uniqiely arond walls with values
bulbs can be placed uniquly around a wall if and only of there are the same number of bulbs as the wall value
"""
def forced_wall_validity(puzzle):
    rows = puzzle.get_rows()
    cols = puzzle.get_cols()

    #place bulbs where there are unique placements of bulbs beccause of wall values
    for i in range(rows):
        for j in range(cols):
            panel = puzzle.get_panel(i, j)
            if puzzle.is_wall(panel) == True:
                #get all he adjacent bulb_panels
                adjacent_panels = puzzle.get_adjacent_panels(panel)
                wall_val = panel.wall_value()
                #Remove all the neighbors that are walls
                adjacent_panels[:] = [x for x in adjacent_panels if x.is_wall() == False]

                #It can be placed uniquely
                if len(adjacent_panels) == wall_val:
                    for neighbor in adjacent_panels:
                        #We don't need to place a bulb if there is already a bulb there
                        if neighbor.bulb == False:
                            puzzle.set_bulb(neighbor)
"""
Paramters: (puzzle) whre puzzle is a Light_puzzle object
Return: Light_puzzle, but this Light_puzzle being the best Light_puzzle at the end of the EA run
This function will handle all of the proccessing with the EA. With fucntion is walled once per run, so
this function will have to do all the evals for the run
"""
def evolution_algorithm(puzzle):
    #Start with instance of the EA, give it the puzzle to make copies of
    EA_instance = Evolution_Instance(puzzle)
    #Get lambda and mu from the config file, so we know were to start in the loop
    try:
        population_size = int(config.get("EA_PARAMATERS", "mu"))
    except configparser.Error:
        print("Error: mu option under EA_PARAMATERS is missing from config file. Exiting")
        sys.exit()

    try:
        new_children = int(config.get("EA_PARAMATERS", "lambda"))
    except configparser.Error:
        print("Error: mu option under EA_PARAMATERS is missing from config file. Exiting")
        sys.exit()

    try:
        evals = int(config.get("STATISTICS", "evals"))
    except configparser.Error:
        print("Error: evals option under STATISTICS is missing from config file. Exiting")
        sys.exit()

    try:
        convergence = int(config.get("EA_PARAMATERS", "termination_convergence_criterion"))
    except configparser.Error:
        print("Error. termination_convergence_criterion option under EA_PARAMATERS is missing from config file. Exiting.")
        sys.exit()

    try:
        termination_evals = int(config.get("EA_PARAMATERS", "evals_until_term"))
    except configparser.Error:
        print("Error. evals_until_term option under EA_PARAMATERS is missingg from config file. Exiting.")
        sys.exit()

    try:
        if config.get("EA_PARAMATERS", "survival_strategy") == "plus":
            plus_survival = True
        elif config.get("EA_PARAMATERS", "survival_strategy") == "comma":
            plus_survival = False
        else:
            print("Error. Invalid option for survival_strategy in config file. Exiting")
            sys.exit()
    except configparser.Error:
        print("Error. survival_strategy option under EA_PARAMATERS is missing from config file. Exiting.")
        sys.exit()

    #This loop will create new generations, thus needing to skip lambda generations
    #Since creating children count an evaluation.
    #Number for convergence criterion
    evals_without_change = 0
    #last_average_fitness = EA_instance.average_population_fitness() #Starting best fitness
    #use a copy of it because this will change
    best_patero_front = copy.deepcopy(EA_instance.get_best_population_members())

    if plus_survival == False and population_size > new_children:
        print("Error. The size of the population is greater than the number of children produced while comma survival is selected.")
        print("Population size can never return to mu!. Please increse lambda in the config file. Exiting.")
        sys.exit()

    #intital logging
    average_fitness = EA_instance.average_population_fitness()
    average_shine_fitness = EA_instance.average_populaion_shine_fitness()
    average_wall_fitness = EA_instance.average_populaion_wall_fitness()

    best_fitness = EA_instance.best_fitness_in_population()
    best_shine_fitness = EA_instance.best_shine_fitness_in_population()
    best_wall_fitness = EA_instance.best_wall_fitness_in_populaiton()
    solution_logger.new_entry(population_size, average_fitness, average_shine_fitness, average_wall_fitness, best_fitness, best_shine_fitness, best_wall_fitness)

    #offset by lambda
    for current_eval in range(population_size+new_children, evals+new_children, new_children):


        #Now prepare the next generation
        #First prepate the next set of children, so we must choose parents
        #We will do the selction process twice for each child, to keep genetic diverisy
        if plus_survival == True:
            for i in range(new_children):
                #fparent selection type handled in select_parent function
                first_parent = EA_instance.select_parent()
                second_parent = EA_instance.select_parent()
                #Perform the crossover the the genes of the parents
                child_chromosome = EA_instance.crossover(first_parent, second_parent)

                #mutate child and create new population member
                new_child = EA_instance.create_new_member(EA_instance.mutate(child_chromosome))
                #Apply second mutation that can add genes to chromosome
                EA_instance.insert_mutation(new_child)
                #Do repair if defined
                try:
                    if config.get("EA_PARAMATERS", "repair_function") == 'yes':
                        new_child.repair()
                except configparser.Error:
                    print("Error: repair_function option under EA_PARAMATERS is missing from the config file. Exiting.")
                    sys.exit()

                #Finally add them to the population
                EA_instance.add_new_member(new_child)
                #We don't need to update the whole dom levels list because only 1 child is being added and no parents are being removed.
                insert_into_dom_level(new_child, EA_instance.dom_levels)
                #EA_instance.update_dom_levels()
        #Comma survival, all the population will be terminated and replaced by all the children. Then populaiton will be weeded out to mu members again. (When doing the normal survival)
        else:
            new_population = []
            #Here we create all the children, and then set every child created as the new population set.
            for i in range(new_children):
                first_parent = EA_instance.select_parent()
                second_parent = EA_instance.select_parent()
                #Perform the crossover the the genes of the parents
                child_chromosome = EA_instance.crossover(first_parent, second_parent)
                #mutate child and create new population member
                new_child = EA_instance.create_new_member(EA_instance.mutate(child_chromosome))
                #Apply second mutation that can add genes to chromosome
                EA_instance.insert_mutation(new_child)
                #Do repair function if specified
                try:
                    if config.get("EA_PARAMATERS", "repair_function") == 'yes':
                        new_child.repair()
                except configparser.Error:
                    print("Error: repair_function option under EA_PARAMATERS is missing from the config file. Exiting.")
                    sys.exit()
                #finally insert child into new member
                new_population.append(new_child)
            #clear old population
            EA_instance.clear_population()
            EA_instance.set_population(new_population)
            #Update dom levels in order to do survival
            EA_instance.update_dom_levels()

        #Now that a new generation has been made, we must now dtermine which solutions get to survive
        #Note: The dom table will be updated after every generation for comma, and for plus ius updated after every child is created and inserted
        #However, it will have to be updated after survival
        EA_instance.population_survival()
        EA_instance.update_dom_levels() #Update after

        #Stop the loop, we have over stepped. This is only a problem when the number of generations doe snot fit well with the number of total evaluations
        if current_eval > evals:
            break
        average_fitness = EA_instance.average_population_fitness()
        average_shine_fitness = EA_instance.average_populaion_shine_fitness()
        average_wall_fitness = EA_instance.average_populaion_wall_fitness()

        best_fitness = EA_instance.best_fitness_in_population()
        best_shine_fitness = EA_instance.best_shine_fitness_in_population()
        best_wall_fitness = EA_instance.best_wall_fitness_in_populaiton()

        solution_logger.new_entry(current_eval, average_fitness, average_shine_fitness, average_wall_fitness, best_fitness, best_shine_fitness, best_wall_fitness)


        current_best_patero_front = EA_instance.get_best_population_members()
        #Check termination conditions
        #Attempt to use convergence termination
        try:
            if config.get("EA_PARAMATERS", "convergence_termination") == 'yes':
                #If the lengths are the same, then we need to check if members have been changed.
                if len(current_best_patero_front) == len(best_patero_front):
                    #Boolean to indicate if we have an equal front
                    found_all = True
                    #They might not be in the same order, so we need to do an n*m search n = len(current) and m = len(best)
                    for best in best_patero_front:
                        #Boolean to indicate we have found the member 'best' in current_best_patero_front
                        found = False
                        for current in current_best_patero_front:
                            if best == current:
                                found = True
                        #This particular member 'best' was not in teh current. Thus the fronts are not equal
                        if found == False:
                            found_all = False
                    #This is the same patero front, thus we add a counter to the convergence.
                    if found_all:
                        evals_without_change += new_children
                    else:
                        evals_without_change = 0
                else:
                    #Change in fitness, so restart counter
                    evals_without_change = 0
                #We have converged, so stop the loop
                if evals_without_change >= convergence:
                    break
            else:
                #if the current evaluation is greater than the max evauluations from the config, terminate
                if termination_evals <= current_eval:
                    break
        except configparser.Error:
            print("Error. convergence_termination option uder EA_PARAMATERS is missing from the config file. Exiting.")
            sys.exit()

        #reassign - use copy because it will change
        best_patero_front = copy.deepcopy(current_best_patero_front)

    best_solutions = EA_instance.get_best_population_members()
    return best_solutions
