'''
    Description:

    This program tests the Goldbach Conjecture https://en.wikipedia.org/wiki/Goldbach%27s_conjecture,
but in an alternative formulation. The equivalent statement is that for every natural number greater
than three, there is at least one pair of primes that are equidistant from it. In the output the natural
number is surrounded by '<< >>' and the primes are on the left side (for p<N) and right side (for N<p) from it.

'''

from collections import deque


class PrimePairs:
    @staticmethod
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
            primes_dict[number] = idx + 1

        return primes_dict

    # primes_dict = get_primes(1000)
    @staticmethod
    def calc_prime_pairs(prime_dict):

        for num in range(4, 500):
            pairs = deque()
            pairs.append(f'<<{num}>>')
            diff = 1 if num % 2 == 0 else 2
            right_number = num - diff

            while right_number > 2:
                if right_number in prime_dict:
                    left_number = num + diff
                    if left_number in prime_dict:
                        pairs.appendleft(right_number)
                        pairs.append(left_number)
                diff += 2
                right_number = num - diff
            print(' '.join(list(str(x) for x in pairs)))


prime_pairs = PrimePairs()
primes_dict = prime_pairs.get_primes(1000)
prime_pairs.calc_prime_pairs(primes_dict)
