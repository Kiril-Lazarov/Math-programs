from math import *
'''
    Description:
    
    This program calculates the length of a function in a given interval by breaking the curve into small straight lines
and then summing them up. The accuracy of the result increases with the decrease in the size of the straight lines. 
'''

class FunctionLength:
    def __init__(self, func: str, down_limit, up_limit, number_of_divisions):
        self.func = func
        self.down_limit = down_limit
        self.up_limit = up_limit
        self.number_of_divisions = number_of_divisions

    def _replace_x_with_values(self, value):
        func = self.func.replace('x', str(value))
        return eval(func)

    def _calculate_y_values(self):
        length = 0
        x_interval = abs(self.down_limit - self.up_limit)
        delta_x = x_interval / self.number_of_divisions
        x_value = self.down_limit
        y_value = self._replace_x_with_values(x_value)
        previous_point = (x_value, y_value)
        for index in range(1, self.number_of_divisions + 1):
            x_value = self.down_limit + index * delta_x
            y_value = self._replace_x_with_values(x_value)
            next_point = (x_value, y_value)
            length += dist(previous_point, next_point)
            previous_point = next_point

        return length

    def __str__(self):
        return f'The length of "{self.func}" in range {self.down_limit}' \
               f' and {self.up_limit} is {self._calculate_y_values()}'


a = FunctionLength('sin(x)', 0, 2*pi, 1000)
print(a)
