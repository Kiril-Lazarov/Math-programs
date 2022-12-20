number = 0

ll = []
with open('file1.txt') as file:
    f = file.read()
with open('file2.txt') as file:
    g = file.read()
    # ll = exec(f)
for idx in range(10):
    exec(f)
    print(ll)
for idx in range(10):
    exec(g)
    print(ll)
# print(exec('a = 1+2'))