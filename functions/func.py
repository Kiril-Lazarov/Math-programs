number = 0
def print_glupost():
    global  number
    try:
        while True:
            n = int(input('Въведи число'))
            number = 0
            print(f'GLupost')
    except:
        number += 1
        if number < 3:
            print(f'Това е от except')
            print_glupost()
        raise ValueError
print_glupost()