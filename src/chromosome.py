"""
Tanner Wendland
9/7/18
CS5401
Missouri University of Science and Technology
"""

from orderedset import OrderedSet

"""
This is the class defintion of a chromosome. A chromosome has genetic code that ddetermines the phenotype of the population member (the placement of the bulbs).
The genetic code is a list of integer tuples, each tuple representing a bulb placement with the tupes being (row, col)
While each entry in the genetic code is independed (and unordered) from one another since no bulb placement directly determines the placement of an other bulb on the bulb,
I use an OrderedSet to remove duplicate entries to avoid have redundant genes, and to keep the list in order when remove duplicate genes.
"""
class chromosome:


    """
    Chromosme constructor. No Paramaters
    """
    def __init__(self):
        self.genetic_code = []

    """
    Paramaters: object, any object but for this class it will always be a tuple
    Return: None
    This function will append an object passed to it to the genetic code of the chromosome
    """
    def append(self, object):
        self.genetic_code.append(object)

    """
    Paramters: None
    Return: None
    This function simply removes any duplicate entires within the chromosome, since no two bulbs can occupy the same panel
    """
    def remove_duplicates(self):
        #still use a list, but set removes the duplicate entries. Keep in order of list
        self.genetic_code = list(OrderedSet(self.genetic_code))

    """functions defined for chromosome so that chromosomes acts similar to a list"""
    def __getitem__(self, key):
        return self.genetic_code[key]

    def __setitem__(self, key, value):
        self.genetic_code[key] = value

    def __str__(self):
        return str(self.genetic_code)

    def __len__(self):
        return len(self.genetic_code)

    def __contains__(self, value):
        return value in self.genetic_code

    def length(self):
        return len(self.genetic_code)

    def remove_gene(self, gene):
        #Since this fucntion is only used once when trying to remove dummy genes, if the gene is not present then ignore
        try:
            self.genetic_code.remove(gene)
        except:
            pass
