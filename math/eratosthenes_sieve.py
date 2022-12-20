'''
This program implements the Eratosthenes's method for deriving
prime numbers. The idea is to delete all numbers which are multiples
of every prime number in the sequence of the natural numbers from 2 to N.
For example if we want to find all prime numbers to 20 we must start from 2 and
delete all multiples of 2 exclude 2 itself - 4, 6, 8 and so on. Than take 3 and
delete all multiples of 3 - 9 and  15 (6, 12 and 18 are already deleted as multiples
of 2). Next take 5, 7, 11 and so on.
'''

from math import sqrt


class EratosthenesSieve:
    INDEX = 0

    def __init__(self, end_num):
        self.end_num = end_num

    # prepares a list with the natural numbers from 2 to end_num
    def __create_list(self):
        return list(range(2, self.end_num + 1))

    def start_sieving(self):
        sieve = self.__create_list()
        prime_container = []
        while True:
            self.INDEX += 1
            divisor = sieve[0]
            if divisor > sqrt(self.end_num):
                sieve = prime_container + sieve
                return ', '.join([str(prime) for prime in sieve])
            prime_container.append(divisor)
            sieve = [num for num in sieve if num % divisor != 0]


a = EratosthenesSieve(1000)
print(a.start_sieving())
