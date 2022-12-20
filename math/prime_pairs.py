from collections import deque


def get_primes(num):
    primes_list = [2, 3]
    for i in range(4, num):
        is_prime = True
        for j in primes_list:
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes_list.append(i)

    primes_dict = {}
    for idx, number in enumerate(primes_list):
        primes_dict[number] = idx+1
    print(primes_dict)
    return primes_dict
primes_dict = get_primes(1000)

def calc_prime_pairs(prime_dict):

    for num in range(4,500):
        pairs = deque()
        pairs.append(f'<<{num}>>')
        diff = 1 if num%2== 0 else 2
        right_number = num - diff
        left_number = 0
        while right_number >2:
            if right_number in prime_dict:
                left_number = num + diff
                if left_number in prime_dict:
                    pairs.appendleft(right_number)
                    pairs.append(left_number)
            diff +=2
            right_number = num - diff
        print(' '.join(list(str(x) for x in pairs)))



calc_prime_pairs(primes_dict)
