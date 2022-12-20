num = int(input())
binary = int(input())
final_num = []
count =0
while num != 0:
    deletion = num // 2
    remainder = num % 2
    final_num.append(str(remainder))
    num = deletion
final_num.reverse()
final_num = list(map(int, final_num))
count = final_num.count(binary)
print(count)

