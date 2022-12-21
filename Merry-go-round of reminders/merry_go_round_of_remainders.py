'''
    Description:

        This program derives prime numbers from 2 to N without executing any mathematical calculations - addition,
    subtraction, division or multiplication(only taking square roots but this is not necessary - taking square roots
    is used for reduce the complexity and time for execution. Deriving primes up to 20 000 without finding
    square roots takes approximately 10,5 seconds.Deriving with square roots - only 0.9 seconds.).
        The core idea is to cycling threw reminders of primes. For example every natural number can be divided by 2 with only two possible
    reminders - 0 and 1. For 3 the reminders are 0, 1 and 2, for 5 - 0, 1, 2, 3 and 4. If a reminder of some of the
    primes smaller than the square root of N is equal to 0 implicates that this number is not a prime. In the opposite
    case the number is a prime number and must be append to the primes-dictionary as key and its reminders as
    value (deque).
        This method has a limitation - it can't calculates over N = 48 000 because of MemoryError.
'''

from collections import deque
from math import sqrt
import time


class PrimesMarryGoRound:
    primes = {2: deque([0, 1])}

    def __init__(self, boundary):
        self.boundary = boundary

    def start_marry_go_round(self):
        square_root = sqrt(self.boundary)
        for n in range(3, self.boundary + 1):
            is_prime = True
            for number in self.primes:
                if number <= square_root:
                    self.primes[number].append(self.primes[number].popleft())
                    if self.primes[number][0] == 0:
                        is_prime = False
                else:
                    break

            if is_prime:
                self.primes[n] = deque(list(range(0, n)))
        return ', '.join(list(str(p) for p in self.primes.keys()))


primes_list = PrimesMarryGoRound(20000)
start = time.time()
result = primes_list.start_marry_go_round()
end = time.time()
print('Start program...')
print('Another start program')
print(result)
print(f'Time for execution: {end - start}s.')
