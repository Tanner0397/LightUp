"""
Tanner Wendland
9/7/18
CS5401
Missouri University of Science and Technology
"""

import configparser
import sys
import random
import copy
import solver
from chromosome import chromosome
from population_member import Population_Member
from domination_table import domination_table
#rom domination_table import dominates

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    config.read(sys.argv[1]) #Use another config file
else:
    config.read("configs/default.cfg")

"""
Parmeters: Population_Member, list of population members
return: Boolean
This fucntion determines if member is dominated by anyone in the level passed
"""
def contains_dominate_member(member, list_of_level):
    #If the level is empty, this it is obviosuly not dominated
    if len(list_of_level) == 0:
        return False
    else:
        for members_in_level in list_of_level:
            #This member is dominated by somone in the level
            if dominates(members_in_level, member) == True:
                return True
        #Member was not dominated by anyone in this level, so lets return False
        return False

"""
Paramters: population member, population member
Return: Boolean
This function determines to see of member dominates over other
"""
def dominates(member, other):
    if member.get_fitness() >= other.get_fitness() and member.get_wall_fitness() <= other.get_wall_fitness() and member.get_shine_fitness() <= other.get_shine_fitness():
        if member.get_fitness() > other.get_fitness() or member.get_wall_fitness() < other.get_wall_fitness() or member.get_shine_fitness() < other.get_shine_fitness():
            return True
        return False
    return False


def insert_into_dom_level(member, levels):
    for i in range(len(levels)):
        #If the member is not dominated by anyone in the level, place it there.
        if contains_dominate_member(member, levels[i]) == False:
            member.set_domination_rank(i)
            levels[i].append(member)
            #Now that the member is in the level, there might be people in the level that are cdominated by the new member
            for check_members in levels[i][:]:
                #Check each one if it dominated by this new member
                if dominates(member, check_members):
                    #If this one is dominated, remove it from the dom_level and insert it somewhere else
                    levels[i].remove(check_members)
                    insert_into_dom_level(check_members, levels)
            return
    #If we're here then we were dominated by everyone thus far, so we create a new level with its only intry being the member
    levels.append([member])


def sort_by_domination(domination_levels):
        new_population = []
        for i in range(len(domination_levels)):
            for member in domination_levels[i]:
                new_population.append(member)
        return new_population

"""
Object for E.A.
"""
class Evolution_Instance:

    def __init__(self, puzzle):

        self.puzzle = puzzle
        self.puzzle_instance_rows = self.puzzle.get_rows()
        self.puzzle_instance_cols = self.puzzle.get_cols()
        self.population = [] #list of population
        try:
            self.population_size = int(config.get("EA_PARAMATERS", "mu"))
        except configparser.Error:
            print("Error: mu option under EA_PARAMATERS is missing from config file. Exiting")
            sys.exit()

        #Create the first members of the population. Use random search to solve the puzzle puzzle_copy
        #Then apply it to the popualtion member.
        for i in range(self.population_size):
            puzzle_copy = copy.deepcopy(self.puzzle)
            #Give that population member a puzzle to solve
            self.population.append(Population_Member(puzzle_copy))

        #Create domination table after the inital population is already created
        #self.dom_table = domination_table(self.population)
        self.dom_levels = []
        self.num_levels = 0
        self.update_dom_levels()

    """
    Paramters: (tuple, chromosome) where tuple is a mutated gene in chromosome
    Return: Boolean
    This function is to verify if a new gene is valid by seeing if it is within the bounds of the puzzle, if the new gene is not a wall check, and if the gene is not a duplicate
    """
    def verify_gene(self, gene, chromo):
        row = gene[0]
        col = gene[1]
        if row < 0 or col < 0:
            return False
         #We are within bounds and this is not a duplicate
        if row < self.puzzle_instance_rows and col < self.puzzle_instance_cols and gene not in chromo:
            panel = self.puzzle.get_panel(row, col)
            #This is not a wall, we are valid
            if self.puzzle.is_wall(panel) == False:
                return True
        return False

    #Function for testing, and visualize population by chromsomes
    def __str__(self):
        string = ""
        for i in range(len(self.population)):
            string += str(self.population[i])
            string += "\n"
        return string

    """
    Paramaters: None
    Return: Integer
    This function simply returns the average fitness of the populaiton
    """
    def average_population_fitness(self):
        value = sum(member.get_fitness() for member in self.population)
        average = value/len(self.population)
        return average

    def average_populaion_shine_fitness(self):
        value = sum(member.get_shine_fitness() for member in self.population)
        average = value/len(self.population)
        return average

    def average_populaion_wall_fitness(self):
        value = sum(member.get_wall_fitness() for member in self.population)
        average = value/len(self.population)
        return average

    """
    Paramaters: None
    Return: Integer
    This function simply returns the best fitness  of the populaiton
    """
    def best_fitness_in_population(self):
        return max(member.get_fitness() for member in self.population)

    def best_shine_fitness_in_population(self):
        return min(member.get_shine_fitness() for member in self.population)

    def best_wall_fitness_in_populaiton(self):
        return min(member.get_wall_fitness() for member in self.population)

    """
    Paramaters: None
    Return: Population_Member
    This function will return the best level of the front
    """
    def get_best_population_members(self):
        best_members = self.dom_levels[0]
        return best_members

    def get_population(self):
        return self.population

    """
    Paramters: None
    return: Population_Member
    This function returns a parent, and winner is chosed in a k tournament style. Uses domination rank.
    """
    def parent_tournament(self):
        try:
            k = int(config.get("EA_PARAMATERS", "tournament_size_parent"))
        except configparser.Error:
            print("Error: tournament_size_parent option under EA_PARAMATERS is missing from config file. Exiting")
        if k > len(self.population):
            print("Error: k is larger then the current population. EA is killing more population members than producing. \nPlease Adjust the tournemnt size for survival in the config so the population is stable. Exiting")
            sys.exit()
        tourny_list = random.sample(self.population, k)
        best_entry = tourny_list[0]
        #Having a lower domination is the best, so this is a minimization problem
        #But wer know how many leves we have so taking the number of levels and subtracting it by
        #The domination rank makes this a maximzing problem and less has to change.
        best_entry_non_domination_rank = self.num_levels - best_entry.get_domination_rank()
        for i in range(k):
            current_non_domination_rank = self.num_levels - tourny_list[i].get_domination_rank()
            if current_non_domination_rank > best_entry_non_domination_rank:
                best_entry = tourny_list[i]
                best_entry_non_domination_rank = current_non_domination_rank
        return best_entry

    """
    Paramters: None
    return: Population_Member
    This function returns a parent, and winner is chosed by a weighted choice based off of fitness
    """
    def parent_fitness_proportional_selection(self):
        #Use num_levels - domination rank for this
        max = sum([self.num_levels - member.get_domination_rank() for member in self.population])
        #fixed point on "roulette wheel"
        choose_point = random.uniform(0, max)
        current = 0
        #Scramble population listing so that the first member of the population isn't chosen everytime, this is an issue when all the fitness scores are 0 (the very beginning)
        self.population = sorted(self.population, key = lambda x: random.random())
        for member in self.population:
            current += self.num_levels - member.get_domination_rank()
            if current >= choose_point:
                return member

    """
    Paramters: none
    Returns: population member
    This function will simply return a random member for the populatiion
    """
    def uniform_random_parent(self):
        return random.choice(self.population)

    """
    Paramaters: None
    Return: Population_Member
    This function returns the chosed parent by either fitness proportional or k tourament
    """
    def select_parent(self):
        try:
            if config.get("EA_PARAMATERS", "parent_selection") == 'random':
                return self.uniform_random_parent()
            elif config.get("EA_PARAMATERS", "parent_selection") == 'fitness_prop':
                return self.parent_fitness_proportional_selection()
            elif config.get("EA_PARAMATERS", "parent_selection") == 'k_tourn':
                return self.parent_tournament()
            else:
                print("Error: Invalid option for parent selection in config file. Exiting.")
                sys.exit()
        except configparser.Error:
            print("Error. parent_selection option under EA_PARAMATERS is missing from config file. Exiting")
            sys.exit()

    """
    Paramters: None
    Return:  None
    This function performs a k-tournament but kills population members that do not win
    """
    def survival_tournament(self):
        try:
            k = int(config.get("EA_PARAMATERS", "tournament_size_survival"))
        except configparser.Error:
            print("Error: tournament_size_survival option under EA_PARAMATERS is missing from config file. Exiting")
        if k > len(self.population):
            print("Error: k is larger then the current population. EA is killing more population members than producing. \nPlease Adjust the tournemnt size for survival in the config so the population is stable. Exiting")
            sys.exit()
        tourny_participants = random.sample(self.population, k)
        #Create local domination table and use that
        local_domination_table = []
        for member in tourny_participants:
            insert_into_dom_level(member, local_domination_table)
        #Sort in ascending order of non domination, reverse the list
        potential_winners = local_domination_table[0];
        random_winner = random.choice(potential_winners)
        for member in tourny_participants:
            if member != random_winner:
              self.population.remove(member)

    def survival_tournament_choose_to_die(self):
        while(len(self.population) != self.population_size):
            try:
                k = int(config.get("EA_PARAMATERS", "tournament_size_survival"))
            except configparser.Error:
              print("Error: tournament_size_survival option under EA_PARAMATERS is missing from config file. Exiting")
            if k > len(self.population):
                print("Error: k is larger then the current population. EA is killing more population members than producing. \nPlease Adjust the tournemnt size for survival in the config so the population is stable. Exiting")
                sys.exit()
            tourny_participants = random.sample(self.population, k)

            #Create local domination table and use that
            local_domination_table = []
            for member in tourny_participants:
                insert_into_dom_level(member, local_domination_table)
            #List if the most dominated solutions
            potential_losers = local_domination_table[-1];
            random_loser = random.choice(potential_losers)
            #print(random_loser.get_fitness())
            #self.population.remove(random_loser)
            for i in range(len(self.population)):
              if self.population[i] == random_loser:
                del self.population[i]
                break



    """
    Paramates: None
    Return: None
    This function simply eliminates the least fit member of the population and brings the population size back to mu
    """
    def truncate_population(self):
        #Try and not give positional bias in the population by keeping order
        members_to_remove = len(self.population)-self.population_size
         #Sorted in ascending order
        sorted_population = sort_by_domination(self.dom_levels)[::-1]
        #These are the members to remove
        unfit_members = sorted_population[0:members_to_remove]
         #kill of all the unfit members
        for i in range(len(unfit_members)):
            for j in range(len(self.population)):
                if unfit_members[i] == self.population[j]:
                    del self.population[j]
                    break

    """
    Parameters: None
    Return: none
    This function will randomly choose len(population) - mu memebrs to remove from population
    """
    def uniform_random_survival_selection(self):
        number_to_remove = len(self.population) - self.population_size
        for i in range(number_to_remove):
            self.population.remove(random.choice(self.population))


    """
    Paramters: None
    Return: None
    This function will choose mu number of members to keep using a iterative fitness propertional selctionself.
    """
    def survival_fitness_proportional_selection(self):

        surviving_members = []
        population_copy = copy.deepcopy(self.population)
        #move this out here for speedup, removes linear search from a linear search
        for i in range(self.population_size):
            #fixed point on "roulette wheel"
            #Same as parent, use domination rank
            max = sum([self.num_levels - member.get_domination_rank() for member in population_copy])
            choose_point = random.uniform(0, max)
            current = 0
            #Scramble population listing so that the first member of the population isn't chosen everytime, this is an issue when all the fitness scores are 0 (the very beginning)
            population_copy = sorted(population_copy, key = lambda x: random.random())
            for member in population_copy:
                current += self.num_levels - member.get_domination_rank()
                if current >= choose_point:
                    surviving_members.append(copy.deepcopy(member))
                    population_copy.remove(member)
                    #Stop the loop here
                    break
        self.population = surviving_members
        return

    """
    Paramaters: None
    Return: None
    This function simply decides how the population will survive, either by trunctaion or k tournament
    """
    def population_survival(self):
        try:
            if config.get("EA_PARAMATERS", "survival_selection") == 'trun':
                self.truncate_population()
            elif config.get("EA_PARAMATERS", "survival_selection") == "k_tourn":
                self.survival_tournament_choose_to_die()
            elif config.get("EA_PARAMATERS", "survival_selection") == "fitness_prop":
                self.survival_fitness_proportional_selection()
            elif config.get("EA_PARAMATERS", "survival_selection") == "random":
                self.uniform_random_survival_selection()
            else:
                print("Error: Ivalid option for survival_selection in config. Exiting")
                sys.exit()
        except configparser.Error:
            print("Error. truncation option under EA_PARAMATERS is missing from config file. Exiting")
            sys.exit()


    """
    Paramaters: Population_Member, Population_Member
    Return: Chromosome Object
    This function takes the chromosomes from parents 1 and 2, and does a single point crossover of the genes
    This creates 2 chromosomes and chooses one of them randomly based off of a coin flip.
    """
    def single_point_crossover(self, parent_1, parent_2):
        chromosome_1 = parent_1.get_chromosome()
        chromosome_2 = parent_2.get_chromosome()
        min_chromosome_length = min(len(chromosome_1), len(chromosome_2))
        max_chromosome_length = max(len(chromosome_1), len(chromosome_2))
        #Try and not clone chromsomes. This will only clone chromsomes of length 1
        random_crossover_index = random.randint(0, min_chromosome_length)
        new_chromosome_1 = chromosome()
        new_chromosome_2 = chromosome()

        for i in range(random_crossover_index):
            new_chromosome_1.append(chromosome_1[i])
            new_chromosome_2.append(chromosome_2[i])

        for i in range(random_crossover_index, min_chromosome_length):
            new_chromosome_1.append(chromosome_2[i])
            new_chromosome_2.append(chromosome_1[i])

        for i in range(min_chromosome_length, max_chromosome_length):
            if len(chromosome_1) > len(chromosome_2):
                new_chromosome_2.append(chromosome_1[i])
            else:
                new_chromosome_1.append(chromosome_2[i])

        #There is a possibility for the chromosome to have duplicate values. There values are redundant and can be removed. This ensures that the program will not
        #try and place 2 bulbs in one panel.
        new_chromosome_1.remove_duplicates()
        new_chromosome_2.remove_duplicates()

        #which chromosome do I return? - 50-50 chance for now
        if random.random() >= .50:
            return new_chromosome_1
        return new_chromosome_2

    def n_point_crossover(self, parent_1, parent_2):
        #Make chromsomes, create copes if parents to orginal values dont change
        chromosome_1 = copy.deepcopy(parent_1.get_chromosome())
        chromosome_2 = copy.deepcopy(parent_2.get_chromosome())
        min_chromosome_length = min(len(chromosome_1), len(chromosome_2))
        max_chromosome_length = max(len(chromosome_1), len(chromosome_2))
        #new chromosomes
        new_chromosome_1 = chromosome()
        new_chromosome_2 = chromosome()

        #Change in length
        length_delta = abs(len(chromosome_1) - len(chromosome_2))

        #Since chromosomes are ov variable length, in 0order to simply our crossover algorithm we must fill our smalled chromomes withj dummy values that will be removed
        dummy_gene = tuple([-1, -1])

        #fill the second chromosomes if it is shorter
        if len(chromosome_1) > len(chromosome_2):
            for i in range(length_delta):
                chromosome_2.append(dummy_gene)
        #Fill the first chromosome if it is shorter
        elif len(chromosome_1) < len(chromosome_2):
                for i in range(length_delta):
                    chromosome_1.append(dummy_gene)

        #Choose crossover points.
        try:
            n_points = int(config.get("EA_PARAMATERS", "n_points"))
        except configparser.Error:
            print("Error. n_points option under EA_PARAMATERS is missing from config file. Exiting.")
            sys.exit()

        #The value of points is larger that the elements avaliable to both chromomes. default to single point since this works for all cases
        if n_points > max_chromosome_length:
            return self.single_point_crossover(parent_1, parent_2)

        points = sorted(random.sample(range(0, max_chromosome_length), n_points))

        for i in range(0, n_points-1, 2):
            #This for will always happen
            for k in range(0, points[i]):
                new_chromosome_1.append(chromosome_1[k])
                new_chromosome_2.append(chromosome_2[k])
            #If i is less than the length of n_points -1 we can sill append
            if i < n_points-1:
                for k in range(points[i], points[i+1]):
                    new_chromosome_2.append(chromosome_1[k])
                    new_chromosome_1.append(chromosome_2[k])

        if points[-1] != max_chromosome_length:
            for i in range(points[-1], max_chromosome_length):
                #IF this is even, we end witht he same chromsomes as we started with
                if n_points % 2 == 0:
                    new_chromosome_1.append(chromosome_1[i])
                    new_chromosome_2.append(chromosome_2[i])
                else:
                    new_chromosome_2.append(chromosome_1[i])
                    new_chromosome_1.append(chromosome_2[i])

        #we're now done crossing over. Lets remove the dummy gene.
        #First lets remove all duplicates
        new_chromosome_1.remove_duplicates()
        new_chromosome_2.remove_duplicates()
        new_chromosome_1.remove_gene(dummy_gene)
        new_chromosome_2.remove_gene(dummy_gene)

        if random.random() >= .50:
            return new_chromosome_1
        return new_chromosome_2


    def crossover(self, parent_1, parent_2):
        try:
            if config.get("EA_PARAMATERS", "n_point_crossover") == 'no':
                return self.single_point_crossover(parent_1, parent_2)
            else:
                return self.n_point_crossover(parent_1  ,parent_2)
        except configparser.Error:
            print("Error. n_point_crossover option under EA_PARAMATERS is missing from config file. Exiting.")
            sys.exit()


    """
    Paramaters: Chromosome
    Return: None
    This function will mutate a chromosome given to it based off of the mutation_rate parameter in the config file. This will go through each entry in the chromosome
    and determine if that gene should be mutated. However since the chromosome is a tuple of integers, after mutating the gene based off of a random number generator
    we must determine to see of the mutated gene is actually valid. We must check to see if the new genes phenotype is a wall or is outside the bounds of the puzzle, or is the gene is a repeat.
    In all of the cases, we will stop the mutation of the gene selcted and move on.
    """
    def mutate(self, chromo):
        try:
            mutation_rate = float(config.get("EA_PARAMATERS", "mutation_rate"))
        except configparser.Error:
            print("Error: mutation_rate option under EA_PARAMATERS is missing from config file. Exiting")
            sys.exit()
            #For each entry in the genetic code of the chromosome
        for i in range(len(chromo)):
            chance = random.random()
            #if the chance of mutation is less or equal than the mutation rate, we mutate this gene
            if chance <= mutation_rate:
                mutated_gene = list(chromo[i])
                row = mutated_gene[0]
                col = mutated_gene[1]
                row_delta = random.randint(-2, 2)
                col_delta = random.randint(-2, 2)
                row += row_delta
                col += col_delta
                # row = random.randint(0, self.puzzle.rows)
                # col = random.randint(0, self.puzzle.cols)
                # We must first check if this gene is valid. We must see of this would be either out of bounds, a wall, or already in the chromosomes genetic code
                new_gene = tuple([row, col])
                valid = self.verify_gene(new_gene, chromo)
                #If the new gene is valid, if it is not valid, do not change it
                if valid == True:
                    chromo[i] = new_gene

    """
    Paramaters: Population_Member
    Return: none
    This function is a second type of mutation that will insert a new gene into the chromosome of a member
    This is added because if throughout the entire population no solution has the right number of bulbs to reach the global optimal
    The there is a zero percent probability that the global optimim will be reached. So this will add a gene to a chromomes,
    provided he gene generated is a valid placement
    """
    def insert_mutation(self, member):
        try:
            mutation_rate = float(config.get("EA_PARAMATERS", "insert_mutation_rate"))
        except configparser.Error:
            print("Error: insert_mutation_rate option under EA_PARAMATERS is missing from config file. Exiting")
            sys.exit()
        chance = random.random()
        if chance <= mutation_rate:
            #randint is inclusive
            random_row_gene = random.randint(0, self.puzzle_instance_rows-1)
            random_col_gene = random.randint(0, self.puzzle_instance_cols-1)
            new_gene = tuple([random_row_gene, random_col_gene])
            if member.valid_gene(new_gene) == True:
                member.insert_new_gene(new_gene)


    def create_new_member(self, chromo):
        #Create copy of blank puzzle for new member
        puzzle_copy = copy.deepcopy(self.puzzle)
        new_member = Population_Member(puzzle_copy, chromo)
        return new_member

    def add_new_member(self, member):
        self.population.append(member)
        insert_into_dom_level(member, self.dom_levels)

    """
    Parameters: none
    Return: none
    This function will simply just clear out the entire population. This function is only to be used in a comma survival strategy
    """
    def clear_population(self):
        self.population.clear()

    """
    Parameters: none
    Return: none
    This function will simply just set the passed object pop as the new popualtion. This function is only to be used in a comma survival strategy
    """
    def set_population(self, pop):
        self.population = pop

    def update_dom_levels(self):
        #clear out the sdom levels
        self.dom_levels.clear()
        for member in self.population:
            insert_into_dom_level(member, self.dom_levels)
        self.num_levels = len(self.dom_levels)

    #used for testing to see domination levels are generated correctly
    def print_dom_levels(self):
        for i in range(len(self.dom_levels)):
            for member in self.dom_levels[i]:
                print("Level {} - Fitness: {}, Shine: {}, Wall: {}".format(i, member.fitness, member.shine_fitness, member.wall_fitness))
