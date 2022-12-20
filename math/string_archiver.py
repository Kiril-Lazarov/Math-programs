string = 'TEXT TO CHANGE'
length_string = len(string)
print(length_string)
final_dict = {}
def smash(list):
    # new_list = []
    # final_dict = {}
    while len(list) > 2:
        new_list = []
        for i in range(len(list) - 1):
            if list[i] > list[i+1]:
                c = 100
            elif list[i]< list[i+1]:
                c = -100
            else:
                c = 0
            new_list.append(list[i + 1] - list[i] + c)
        print(f'Това е list: {len(new_list) +1} лист!')
        print(f'Той е дълъг: {len(new_list)}')
        print(new_list)
        final_dict[length_string - 2] = new_list
        return smash(new_list)

    return final_dict

first_value = string[0]
list = []
new = ''
print(first_value)
for i in range(length_string - 1):
    list.append(ord(string[i+1]) - ord(string[i]))


print(f'Това е първият лист! {list}')
print(f'Тoj e дълъг! {len((list))}')
dict = smash(list)
print(dict)
# dict = smash(list)


# for i in range(len(list)):
#
#     if i > 0:
#         new = chr(ord(new) + list[i])
#     else:
#         new += chr(ord(first_value) + list[i])
#     first_value += new
# print(first_value)
# def backward(smash):
#     def extention(lists, number):
#         new_lists = []
#         for i in range(number):
#             for j in range(len(lists) - 1):
#                 new_lists.append(lists[j] -100 + lists[j+1])
#     number = 0
#     lists = []
#     for i,j in  smash.items():
#         number = i
#         lists = j
#     extention(lists, number)
#
# backward(smash(list))








