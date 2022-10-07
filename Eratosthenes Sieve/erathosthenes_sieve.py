from math import sqrt
import time
end_num = 2000000

numbers_list = list(range(2, end_num+1))
n = 0
start = time.time()
while True:
    n +=1
    divisor = numbers_list[0]
    if divisor > sqrt(end_num):
        break
    numbers_list = [num for num in numbers_list if num % divisor != 0]
    print(f'{n} - {divisor}')

for num in numbers_list:
    n += 1
    print(f'{n} - {num}')
end = time.time()
print(f'Time: {end - start} sec')