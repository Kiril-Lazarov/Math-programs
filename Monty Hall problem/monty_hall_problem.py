'''
    Description:

    Link the famous Monty Hall Problem: https://www.youtube.com/watch?v=4Lb-6rxZxx0&ab_channel=Numberphile

        This program verifies that if the player always choose to switch the door the probability of win is
    equal to 2/3 (0.67%). And if he always choose not to switch the door the probability is fall down to 1/3.

'''

import random


class MontyHallProblem:
    wins = 0

    def __init__(self, count, is_switched = True):
        self.count = count
        self.is_switched = is_switched

    def calculate_probability(self):

        for i in range(self.count):
            behind_doors = ["goat", "car", "goat"]
            random.shuffle(behind_doors)
            rand_int = random.randint(0, 2)  # makes random choice of "door" by index
            choice = behind_doors[rand_int]
            behind_doors.pop(rand_int)  # removes "the choice" from the list
            if behind_doors.count('goat') == 2:
                delete = random.randint(0, 1)  # makes random choice which of "goat" member of the list to remove
                behind_doors.pop(delete)
            else:
                behind_doors.remove('goat')
            behind_doors.append(choice)
            if self.is_switched:
                choice = behind_doors[0]

            if choice == 'car':
                self.wins += 1
        return f'Wins ratio = {self.wins / self.count:.2f}%'

monty_hall = MontyHallProblem(10000)
print(monty_hall.calculate_probability())