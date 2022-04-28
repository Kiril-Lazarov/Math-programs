from math import dist

n = 1000  # bigger n calculates more accurate the length of function
lower_lim = -1
upper_lim = 0
diff = abs(lower_lim - upper_lim) # defines range
x_distance = diff / n
result = 0
for i in range(1, n + 1):
    x1 = lower_lim + (i-1)*x_distance
    x2 = x1 + x_distance
    y1 = x1**2
    y2 = x2**2
    length = dist([x1,y1], [x2,y2])
    result += length
print(result)
