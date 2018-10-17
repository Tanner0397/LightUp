"""
Tanner Wendland
9/28/18
CS5401
Missouri University of Science and Technology
"""
"""This class simply has 2 members, base_bulb shines on all the bulbs from the shine_bulbs list"""
class shine_list:
    def __init__(self, bulb, list_of_bulbs):
        self.base_bulb = bulb
        self.shine_bulbs = list_of_bulbs

    def __len__(self):
        return len(self.shine_bulbs)
