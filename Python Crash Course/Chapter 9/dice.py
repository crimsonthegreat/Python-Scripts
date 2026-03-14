from random import randint

class Die:
    """"Model dice and rolling them"""

    def __init__(self, sides=6):
        """Initilize die rolls"""
        self.sides = sides
        self.number_rolls = 0

    def roll_die(self):
        """Roll the dice"""
        while self.number_rolls < 10:
            print(randint(1, self.sides))
            self.number_rolls += 1
        
    def reset_rolls(self):
        """resets the number for rolls to 0"""
        self.number_rolls = 0