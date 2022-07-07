from collections import deque


def primes():
    primes_list = [2, 3]
    # num = int(input("Choose n>7 "))
    num = 100000
    if num <= 7:
        print('Invalid input')
        primes()

    for i in range(4, num):
        is_prime = True
        for j in primes_list:
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes_list.append(i)
    return primes_list, num


def patterns():
    data = primes()
    primes_list = data[0]
    n = data[1]
    combinations = deque([])
    for sixts in range(7, n + 1, 6):
        if sixts in primes_list:
            left = 'True'
        else:
            left = 'False'
        if (sixts - 2) in primes_list:
            right = 'True'
        else:
            right = 'False'
        combinations.append(right)
        combinations.append(left)
        # print(f'{right} {sixts - 2} --- {sixts - 1} --- {sixts} {left}', end='   ')
    combinations.popleft()
    combinations.pop()
    prime_boolean_tuples = []
    true_true = ('True', 'True')
    true_true_count = 0
    true_false = ('True', 'False')
    true_false_count = 0
    false_true = ('False', 'True')
    false_true_count = 0
    false_false = ('False', 'False')
    false_false_count = 0
    while combinations:
        boolean_pair = (combinations.popleft(), combinations.popleft())
        prime_boolean_tuples.append(boolean_pair)
        if boolean_pair == true_true:
            true_true_count += 1
        elif boolean_pair == true_false:
            true_false_count +=1
        elif boolean_pair == false_true:
            false_true_count += 1
        else:
            false_false_count +=1
    print()
    print(true_true_count)
    print(true_false_count)
    print(false_true_count)
    print(false_false_count)



patterns()