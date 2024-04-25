'''

   This program calculates the arithmetic mean values of all prime numbers in the range from 3 to a given number.

'''
import matplotlib.pyplot as plt
import numpy as np


def create_primes(limit):
    primes_list = [2]
    for num in range(3, limit):
        is_prime = True
        for prime in primes_list:
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes_list.append(num)
    return primes_list


# Combine pairwise the last prime number in the list with all preceding ones.
def get_combinations(primes_list):
    last_prime = primes_list[-1]
    comb_list = []
    for i in range(len(primes_list) - 1):
        comb_list.append((primes_list[i], last_prime))
    return comb_list


primes = create_primes(20)[1:]
get_combinations(primes)


def get_mean_numbers(combinations_list):
    integer_list = []
    for pair in combinations_list:
        mean_num = int(np.mean((pair)))
        integer_list.append(mean_num)
    return sorted(set(integer_list))


# Returns the first number whose difference with the previous one is greater than 1.
def get_first_number(int_list):
    previous_num = None
    int_list = sorted(set(int_list))
    for index, num in enumerate(int_list):
        if index == 0:
            previous_num = num
        else:

            diff = num - previous_num
            if diff > 1:
                return int_list[index] - diff + 1
            previous_num = num
    return None


def create_first_numbers_list(limit):
    primes = create_primes(limit)[1:]
    integer_list = []
    first_numbers_list = []
    for index in range(2, len(primes)):

        part_primes = primes[:index]

        comb = get_combinations(part_primes)

        integer_list = sorted(set(integer_list + get_mean_numbers(comb)))

        last_number = get_first_number(integer_list)

        if last_number is not None:
            first_numbers_list.append(last_number)

    return first_numbers_list


first_numbers = create_first_numbers_list(4000)

plt.plot(first_numbers)
plt.show()
