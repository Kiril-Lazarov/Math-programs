from collections import deque

primes = {2: deque([0, 1])}

boundary = 100
for n in range(3, boundary + 1):
    is_prime = True
    for number in primes:
        primes[number].append(primes[number].popleft())
        if primes[number][0] == 0:
            is_prime = False
    if is_prime:
        primes[n] = deque(list(range(0, n)))
        print(f'{len(primes)} - {n}')
