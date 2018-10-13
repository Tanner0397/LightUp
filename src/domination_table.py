"""
Tanner Wendland
10/13/18
CS5401
Missouri University of Science and Technology
"""
from population_member import Population_Member

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

"""
Class that handles the domination table.
Members:
    Add_entry(): adds an entry to the domination table.
    generate_table(): creates the
"""
class domination_table:
    def __init__(self, members):
        self.pairs = []
        self.generate_table(members)

    def add_entry(self, member, dominates):
        self.pair.append([member, dominates])

    def generate_table(self, members):
        for current_member in members:
            doms = []
            for check_member in members:
                if dominates(current_member, check_member):
                    doms.append(check_member)
            self.pairs.append([current_member, doms])

    def update_table(self, members):
        #Clear pairs
        self.pairs.clear()
        self.generate_table(members)

    def print_table_info(self):
        i = 0
        for pair in self.pairs:
            print("Memebr {} dominates {} memebrs of the population".format(i, len(self.pairs[i][1])))
            i+=1
