def for_f():
    type_for_cicle = input("What type of for cycle - by index(i) or by member(m)? ")
    if type_for_cicle == "i":
        iterator = input("Iterator ")
        variable = input("Variable ")

        if input("Do you want to assign if_elif statements y\\n? ") == "y":
            el_if(iterator, variable)
        else:
            print(f"for {iterator} in range({variable}):\n    pass")
    elif type_for_cicle == "m":
        pass
    else:
        print("Invalid type for cycle")
        for_f()


def el_if(x,y):
    values_list = list()
    if_elif_var = input("Variable name ")
    value = input("Value ")
    while value != "end":
        values_list.append(value)
        value = input("Elif Value ")
    if x != 0:
        print(f"for {x} in range({y}):")
    for i in range(len(values_list)):
        if i == 0:
            print(f"if {if_elif_var} == '{values_list[i]}':\n    pass")
        else:
            print(f"elif {if_elif_var} == '{values_list[i]}':\n    pass")


def choose_func():
    choose_function = input("Choose function - el_if, for_f:")
    if choose_function == "el_if":
        x = 0
        y = 0
        el_if(x,y)
    elif choose_function == "for_f":
        for_f()
    else:
        print('Invalid function')
        choose_func()


choose_func()
