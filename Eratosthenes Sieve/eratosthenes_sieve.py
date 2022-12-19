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
