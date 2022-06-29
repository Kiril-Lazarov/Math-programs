def primes():
    primes_list = [2, 3]
    num = int(input("Choose n>3 "))

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
    for sixts in range(1, n + 1, 6):
        if sixts in primes_list:
            left = 'True'
        else:
            left = 'False'
        if (sixts - 2) in primes_list:
            right = 'True'
        else:
            right = 'False'
        print(f'{right} {sixts - 2} --- {sixts - 1} --- {sixts} {left}')

patterns()