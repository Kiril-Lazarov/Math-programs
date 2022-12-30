'''
    Description:

      This program is based on 'marry_go_round_of_remainders' principle but the prime remainders
   are not store in deque. Instead, they are stored as just one digit in 'primes' dictionary. The
   digit increase by 1 and set back to 0 when it reaches the value of the prime itself. This correction
   preserves the memory from overloading and significantly increases the speed of the program. For example
   the calculation of primes when N = 20 000 takes approximately 0.2 seconds - four times faster than same
   calculation using 'marry_go_round_of_remainders'.
'''

from math import sqrt
import time


class PrimeRemainders:
    primes = {2: 0}
    final_primes_list = ['2']

    def __init__(self, boundary):
        self.boundary = boundary

    def start_marry_go_round(self):
        square_root = sqrt(self.boundary)
        for n in range(3, self.boundary + 1):
            is_prime = True
            for number in self.primes:
                if number <= square_root:
                    self.primes[number] += 1
                    if self.primes[number] == number:
                        self.primes[number] = 0
                        is_prime = False
                else:
                    break

            if is_prime:
                self.primes[n] = 0
                self.final_primes_list.append(str(n))
        return ', '.join(self.final_primes_list)


primes_list = PrimeRemainders(50000)
start = time.time()
result = primes_list.start_marry_go_round()
end = time.time()
print(result)
print(f'Time for execution: {end - start}s.')
