string = ''''
You are participating in a Firearm course. It is a training day at the 
shooting range. You will be given a matrix with 5 rows and 5 columns. 
It is a shotgun range represented as some symbols separated by a single space:

'''
first_value = string[0]
list = []
new = ''
print(first_value)
for i in range(len(string) - 1):
    list.append(ord(string[i+1]) - ord(string[i]))

for i in range(len(list)):

    if i > 0:
        new = chr(ord(new) + list[i])
    else:
        new += chr(ord(first_value) + list[i])
    first_value += new
print(first_value)




