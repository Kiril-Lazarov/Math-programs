'''
    Description:
    This program calculates the formula 'f(x) = x**2 + c' and checks whether, given values of x and c, by iterating
the initial value of the iteration can be obtained. For example if x = -7/4 the cycle is: -7/4, 5/4, -1/4, -7/4.
Calculations are done in the form of actions with fractions, not as actions with non-integers (floating point numbers)

'''

from math import floor

target_fraction = '-7/4'  # this is 'x' in the formula
constant = '-29/16'  # this is 'c' in the formula
result = ''
result_fractions = []
n = 10
start_fraction = target_fraction


def convert_to_numbers(fraction):
    return [int(x) for x in fraction.split('/')]


def get_divisor(number):
    for num in range(2, floor(abs(number / 2)) + 1):
        if number % num == 0:
            return num
    return None


def find_common_divisor(new_numerator, common_denominator):
    new_numerator_factor = get_divisor(new_numerator)
    common_denominator_factor = get_divisor(common_denominator)
    if new_numerator_factor == common_denominator_factor:
        return new_numerator_factor
    return None


def divide_fraction_by_common_divisor(common_factor, fraction):
    numerator, denominator = fraction
    while numerator % common_factor == 0 and denominator % common_factor == 0:
        numerator /= common_factor
        denominator /= common_factor
    return [int(numerator), int(denominator)]


def calculate_fraction_sum(squared_first_fraction, second_fraction):
    first_denominator, second_denominator = squared_first_fraction[1], second_fraction[1]
    first_numerator, second_numerator = squared_first_fraction[0], second_fraction[0]
    common_denominator = first_denominator * second_denominator
    new_numerator = second_denominator * first_numerator + first_denominator * second_numerator

    common_factor = find_common_divisor(new_numerator, common_denominator)
    if common_factor is not None:
        fraction = divide_fraction_by_common_divisor(common_factor, [new_numerator, common_denominator])
        return fraction
    return [int(new_numerator), int(common_denominator)]


# prepares the fraction for current iteration's calculations
def current_iteration(fraction_one, fraction_two):
    first_fraction = convert_to_numbers(fraction_one)
    second_fraction = convert_to_numbers(fraction_two)
    squared_first_fraction = [x ** 2 for x in first_fraction]
    return calculate_fraction_sum(squared_first_fraction, second_fraction)


# checks for a cycle up to n iterations
for _ in range(n):
    if result != target_fraction:
        new_value = current_iteration(start_fraction, constant)
        result = '/'.join(str(x) for x in new_value)
        result_fractions.append(result)
        start_fraction = result
    else:
        print(f'{target_fraction}, {", ".join(result_fractions)}')
        break
else:
    print(f'There is no cycles with target fraction {target_fraction} up to {n} iterations')
