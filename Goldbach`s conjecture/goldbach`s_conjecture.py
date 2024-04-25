from itertools import combinations
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


def get_mean_numbers(combinations_list):
    integer_list = []
    for pair in combinations_list:
        mean_num = int(np.mean((pair)))
        integer_list.append(mean_num)
    return sorted(set(integer_list))


def get_last_number(int_list):
    previous_num = None
    int_list = sorted(set(int_list))
    for index, num in enumerate(int_list):
        if index == 0:
            previous_num = num
        else:

            diff = num - previous_num
            if diff > 1:
                return int_list[index] - diff
            previous_num = num
    return None


def create_last_numbers_list(limit):
    last_numbers_list = []
    primes = create_primes(limit)[1:]
    for index in range(2, len(primes)):
        if limit > 7:
            part_primes = primes[:index]
            comb = combinations(part_primes, 2)
            integer_list = get_mean_numbers(comb)
            last_number = get_last_number(integer_list)
            if last_number is not None:
                last_numbers_list.append(last_number)

    return last_numbers_list


last_numbers_list = create_last_numbers_list(1200)

plt.plot(range(len(last_numbers_list)), last_numbers_list)
plt.show()
