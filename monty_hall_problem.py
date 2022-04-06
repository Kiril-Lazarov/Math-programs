import random
is_switched = 'No' 

wins = 0   #
count = 500
for i in range(count):
    behind_doors = ["goat", "car", "goat"]
    random.shuffle(behind_doors)
    rand_int = random.randint(0,2)
    choice = behind_doors[rand_int]
    behind_doors.pop(rand_int)
    if behind_doors.count('goat') == 2:
        delete = random.randint(0,1)
        behind_doors.pop(delete)
    else:
        behind_doors.remove('goat')
    behind_doors.append(choice)
    if is_switched == "Yes":
        choice = behind_doors[0]

    if choice == 'car':
        wins +=1
print(f'Wins ratio = {wins / count:.2f}%')