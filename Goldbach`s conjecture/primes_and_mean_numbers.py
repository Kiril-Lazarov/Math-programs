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


def count_missing_numbers(primes_list_vec):
    curr_mean_numbers = {}
    last_prime = primes_list_vec[-1][0]
    for ll in primes_list_vec:
        if len(ll) > 1:
            mean_nums = [ll[0] + ll[i] for i in range(1, len(ll[:]))]
            all_nums = list(range(mean_nums[0], last_prime + 1))
            missing_nums_count = len(set(mean_nums).symmetric_difference(all_nums))
            curr_mean_numbers[ll[0]] = missing_nums_count
    curr_mean_numbers[last_prime] = 0

    return curr_mean_numbers


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


primes = create_primes(30)[1:]

primes_vec = create_natural_numbers(6, 0, primes, [])

missing_numbers = count_missing_numbers(primes_vec)

for ll in primes_vec:
    print(f'{ll[0]} ({missing_numbers[ll[0]]})-> {[ll[0] + ll[i] for i in range(1, len(ll[:]))]}')
total_len_primes_vec = sum([len(x) - 1 for x in primes_vec])
numbers_count = primes_vec[-1][0] - primes_vec[0][0]
missing_numbers_count = sum(missing_numbers.values())
first_mean_number_without_prime_pair = missing_numbers_count - total_len_primes_vec - 1

print(f'Numbers count: {numbers_count}\n'
      f'Total mean numbers: {total_len_primes_vec}\n'
      f'Missing numbers count: {missing_numbers_count}\n'
      f'First number without prime pair: {first_mean_number_without_prime_pair}')
