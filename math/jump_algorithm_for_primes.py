import time

end_num = 100

n = 2
last_index = 2

cumulative_list = ['*']
start = time.time()
while n <= end_num:
    for position in cumulative_list:
        if position == '*':
            cumulative_list += (2 * n - last_index) * ['*']
            last_index = 2 * n
            cumulative_list[-1] = [n]
            del cumulative_list[0]
            print(f'Prime number: {n} Length of list: {len(cumulative_list)}')
            # print(cumulative_list)
            break
        else:
            for num in position:
                if num <= len(cumulative_list) -1:
                    if cumulative_list[num] == '*':
                        cumulative_list[num] = [num]
                    else:
                        cumulative_list[num].append(num)
                else:
                    diff = num - (len(cumulative_list) -1)
                    last_index += diff
                    cumulative_list += diff * ['*']
                    cumulative_list[-1] = [num]
            del cumulative_list[0]
            # print(n)
            # print(cumulative_list)
            break
    n += 1
end = time.time()
print(f'Time: {end - start} sec')