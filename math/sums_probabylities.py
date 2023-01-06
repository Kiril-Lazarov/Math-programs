'''
    Description:
    This program calculates the number of occurrences of a number relative
to a given number of attempts. The number is obtained as a result by
summing all the digits contained in a given number. For example,
the sum of the number 235 is equal to 8.

'''

from random import randint


# Constructs random number with a given length among the natural digits in some range
def get_random_integer(length_of_num_sequence, range_of_used_integer):
    number = []
    for idx in range(length_of_num_sequence):
        number.append(randint(*range_of_used_integer))

    return ''.join(str(x) for x in number)


# Calculates the sum of the digits of the given number
def get_sum_of_number_integers(num):
    return sum(int(x) for x in num)


# Counts the occurrences
def calc_nums_appearances(attempts, length_of_num_sequence, range_of_used_integer):
    nums_occurrences = {}
    for _ in range(attempts):
        curr_num = get_random_integer(length_of_num_sequence, range_of_used_integer)
        integer_sum = get_sum_of_number_integers(curr_num)
        if integer_sum not in nums_occurrences:
            nums_occurrences[integer_sum] = 0
        nums_occurrences[integer_sum] += 1
    sorted_nums_occurrences = {k: v for k, v in sorted(nums_occurrences.items(), key=lambda x: (-x[1], x[0]))}
    return "\n".join(f'{key}:        {value}              {(value / attempts) * 100:.2f}%' for key, value in
                     sorted_nums_occurrences.items())


num_range = (0, 5)
number_of_digits = 5
attempts = 10000
print('Number     Occurrences       Percentage')
print(calc_nums_appearances(attempts, number_of_digits, num_range))
