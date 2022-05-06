import math
n = 20
result = 0 + 0j
for i in range(1, n+1):
    result += 1/ i**(1/2 + 2j)
    print(f'{result:.4f}', end= " ")

