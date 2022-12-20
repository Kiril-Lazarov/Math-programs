import time




def primes_factors(num, primes_list, choose):
    factors_dict = {}
    print(f"2 -> 1, 2")
    print(f"3 -> 1, 3")
    for i in range(4, num + 1):
        factorisation(num, primes_list, choose)
        factors = factorisation(i, primes_list, choose)
        if len(factors) == 0:
            factors_dict[i] = [1, i]
        else:
            factors_dict[i] = factors
    for key, value in factors_dict.items():
        count = 0
        for i in primes_list:
            if i <= key:
                count += 1
        print(f'{key} -> {", ".join(list(map(str, value)))} <::> {count} primes')


def factorisation(num, prime_list, choose):
    factors_list = []
    j = 0
    i = prime_list[j]
    while i <= int(num / 2):
        i = prime_list[j]
        current_num = num
        if num % i == 0:
            while current_num % i == 0:
                factors_list.append(i)
                current_num /= i
        j += 1
    if choose == "f":
        if len(factors_list) != 0:
            print(f"The prime factors of {num} are {', '.join(list(map(str, factors_list)))}")
        else:
            print(f"The prime factors of {num} are {1} and {num}")
    elif choose == "d":
        return factors_list


def primes():
    primes_list = [2, 3]
    num = int(input("Choose n>3 "))
    choose = input(
        "Which function do you want to choose? Primes(p), Primes factorisation(f) or Primes factors dictionary(d)? ")
    if num <= 3:
        print("Invalid number")
        primes()
    else:

        for i in range(4, num):
            is_prime = True
            for j in primes_list:
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime:
                primes_list.append(i)

    if choose == "p":
        print(', '.join(list(map(str, primes_list))))
        print(f"Count primes are {len(primes_list)}")
        if num in primes_list:
            print(f'{num} is a prime number')
        else:
            print(f'{num} is not a prime number')
        return primes_list



    elif choose == 'f':
        factorisation(num, primes_list, choose)
    elif choose == 'd':
        primes_factors(num, primes_list, choose)


prime_numbers = primes()
print(prime_numbers)
