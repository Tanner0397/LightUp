"""
Tanner Wendland
9/7/18
CS5401
Missouri University of Science and Technology
"""

"""
Object for population member. Each member has their own chromozome that determines their solution. This chromozome represents a list of bulb placement.
A chromozome will be of variable length, this being the number of white panels in the puzzle. The first part of the
chromozome is a list of the bulbs placed on the board in form of (row, col) pairs using the indicies from the panel object.
"""

import configparser
import sys
import solver
from chromosome import chromosome

config = configparser.ConfigParser()

if(len(sys.argv) >= 2):
    config.read(sys.argv[1]) #Use another config file
else:
    config.read("configs/default.cfg")


class Population_Member:
    """
    Constructor
    Paramters: (puzzle, chromo) where pizzle is an unsolved puzzle and chromo is an optional paramater that  is a chromsomes object
    Return: None
    This function is the constructor for the population member object. If a chromosome is not passes, then this a member of the intial populaion so it will use random search
    and attempt to solve their puzzle. If a chromomes is passes, then the population emmebr uses that chromosome to generate their phenotype (the bulb placement on the board).

    Members:
        puzzle: Solution instance, used to calculate fitness of member
        chromosome: Chromsome the represetns this members
        chromosome_length: length of the members chromosome
        fitness: base fitness based on number of panels lit, maxizing
        shine_fitness: Number of bulbs that shine on each other, minimizing
        wall_fitness: numebr of walls that are not satisfied, minimizing

    """
    def __init__(self, puzzle, chromo=None):
        #initial fitness value
        self.fitness = 0
        self.shine_fitness = 0
        self.wall_fitness = 0
        self.puzzle = puzzle
        #We are an initial population member so we must solve the puzzle using Random search
        if chromo is None:
            self.chromosome = chromosome() #initial_chromosome list

            #Solve the puzzle using uniform random and/or forced validity
            try :
                if config.get("PARAMETERS", "forced_wall_validity") == 'yes':
                    solver.forced_wall_validity(puzzle)
            except configparser.Error as e:
                print("Error. forced_wall_validity option under PARAMETERS is missing from config file. Exiting.")
                sys.exit()
            solver.random_search(puzzle)

            #Find the max length of a chromozome
            bulb_panels = self.puzzle.get_all_bulbs()
            #Set the max chromozome length
            self.chromosome_length = len(bulb_panels)
            for i in range(self.chromosome_length):
                row = bulb_panels[i].row
                col = bulb_panels[i].col
                #index [0] is row, index [1] is col. Sent as a tuple since tuples are not mutable, and are hashable
                self.chromosome.append(tuple([row, col]))
            self.evaluate_fitness()
            #Remove dupliates if any, but there shouldn't be any since random search does not place more than 1 bulb per panel
            self.chromosome.remove_duplicates()
            #We are receiving a chromosome so we must place the bulbs, then evaluate the solution
        elif isinstance(chromo, chromosome):
            #Remove duplicates if any
            chromo.remove_duplicates()
            self.chromosome = chromo
            self.chromosome_length = self.chromosome.length()
            for i in range(self.chromosome_length):
                row = self.chromosome[i][0]
                col = self.chromosome[i][1]
                panel = self.puzzle.get_panel(row, col)
                self.puzzle.set_bulb(panel)
            self.evaluate_fitness()
        else:
            print("Error: Chromosome argument is not a chromosome. Exiting.")
            sys.exit()

    """
    Paramater: gene, where gene is a tuple with a row and a column entry
    Return: Boolean
    This funciton simply returns true of the new gene would be vaild to place inside of their chromosome
    This will not place bulbs where a tile is already lit, so this will not create invalid solutions from bulb on bulb interactions
    """
    def valid_gene(self, gene):
        row = gene[0]
        col = gene[1]
        panel = self.puzzle.get_panel(row, col)
        #Not a wall, bulb, or already lit panel
        if panel.bulb == True or panel.wall == True or panel.lit == True:
            return False;
        return True

    """
    Parmeters: None
    return: Chromsome
    This function will simply return the chromosome of the population member
    """
    def get_chromosome(self):
        return self.chromosome

    """
    Parameters: None
    Return: None
    This function will evaluate the fitness of this Population member.
    """
    def evaluate_fitness(self):
        self.fitness = self.puzzle.verify_solution()
        self.shine_fitness = self.puzzle.shine_fitness()
        self.wall_fitness = self.puzzle.wall_fitness()

    """
    Parameters: None
    Return: Interger Fitness
    This function will return the fitness of this Population member.
    """
    def get_fitness(self):
        return self.fitness

    def get_shine_fitness(self):
        return self.shine_fitness

    def get_wall_fitness(self):
        return self.wall_fitness

    """
    Parameters: gene
    Return: None
    This function will insert a new gene into the chromosomes of the population member.
    """
    def insert_new_gene(self, gene):
        #append gene
        row = gene[0]
        col = gene[1]
        panel = self.puzzle.get_panel(row, col)
        self.chromosome.append(gene)
        self.chromosome_length += 1
        self.puzzle.set_bulb(panel)
        #Reevaluate fitness
        self.evaluate_fitness()

    """
    Function for testing and visualizing chromsomes
    """
    def __str__(self):
        return str(self.chromosome)


    """Repair Function"""
    def repair(self):
        while True:
            current_shine_list = self.puzzle.repair_shine_list()
            #If the length of this list is zero, then we don't have any bulbs to remove, so break
            if len(current_shine_list) == 0:
                #We should reevaluate the fitness now
                self.evaluate_fitness()
                break
            else:
                entry_to_remove = current_shine_list[0]
                for i in range(len(current_shine_list)):
                    if len(entry_to_remove) < len(current_shine_list[i]):
                        entry_to_remove = current_shine_list[i]
                #We have the bulb with the largest list now, now lets get the panel
                bulb_to_remove = entry_to_remove.base_bulb
                #Now, we have to made an ammendent to the chromosome, and remove this bulb that we are removing.
                gene_to_remove = tuple([bulb_to_remove.row, bulb_to_remove.col])
                #Now let us sctually remove the bulb from the solution
                self.puzzle.remove_bulb(bulb_to_remove)
                #Remove the bulb from the chromosome and decrement the size of the chromosome
                self.chromosome.remove_gene(gene_to_remove)
                self.chromosome_length-=1
        return


    """

    """

    """
    Equality and Inequality operators defined based off of fitness of population member
    """
    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitnes
