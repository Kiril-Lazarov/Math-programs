# calculates product of numbers
def product_nums(numbers):
    numbers = list(map(int, numbers.split()))
    multiplier = 1
    for i in numbers:
        multiplier *= int(i)
    return multiplier


# calculates sum of ascii values of sequence of characters
def ascii_sum(string):
    total = 0
    for i in range(len(string)):
        total += ord(string[i])
    return total



