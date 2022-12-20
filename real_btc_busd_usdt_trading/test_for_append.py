# file = open('data.txt', 'a')
# number = 1299
# for _ in range(5):
#     number +=1
#     file.write(f', {number}')
# file = open('data.txt')
# print(file.read())

file = open('trade_numbers.txt')

f1, f2 = file.read().split(', ')
print(f1, f2)
file.close()