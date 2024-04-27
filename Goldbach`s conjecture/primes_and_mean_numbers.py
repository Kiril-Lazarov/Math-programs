'''
    This script calculates the arithmetic mean of every
    possible pair of prime numbers up to a given number."
'''


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


def create_natural_numbers(count_iterations, current_iteration, primes_list, nums_list):
    if current_iteration > count_iterations:
        return nums_list
    first_prime = primes_list[0]
    primes_list = primes_list[1:]
    current_nums_list = [first_prime]
    for prime in primes_list:
        current_nums_list.append(int((prime - first_prime) / 2))

    nums_list.append(current_nums_list)
    current_iteration += 1
    return create_natural_numbers(count_iterations, current_iteration, primes_list, nums_list)


primes = create_primes(300)[1:]

primes_vec = create_natural_numbers(30, 0, primes, [])

for ll in primes_vec:
    print(ll[0], '->', [ll[0] + ll[i] for i in range(1, len(ll[:]))])
