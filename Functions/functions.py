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


# find an indexes of character in a string
def find_indexes(character, sequence):
    char_sequence = [char for char in range(len(sequence)) if sequence[char] == character]
    return char_sequence


# find a fibonacci sequence to given member
def fibonacci(number):
    test_list = [0, 1]
    fibonacci_list = [0, 1]
    for i in range(number):
        new_member = sum(test_list)
        fibonacci_list.append(new_member)
        test_list.append(new_member)
        del test_list[0]
    return ', '.join(map(str, fibonacci_list))
