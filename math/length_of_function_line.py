import math

n = 10  # bigger n calculates more accurate the length of function
lower_lim = 0
upper_lim = 4
diff = abs(lower_lim - upper_lim)  # defines range
x_distance = diff / n
result = 0
area = 0
for i in range(1, n + 1):
    x1 = lower_lim + (i - 1) * x_distance
    x2 = x1 + x_distance
    y1 = math.sin(x1)
    y2 = math.sin(x2)
    area += abs(x1 - x2) * y1 + abs(x1 - x2) * abs(y1 - y2) / 2  # calculates tha area of the quadrilateral between four points
    length = math.dist([x1, y1], [x2, y2])
    result += length
print(result)
print(area)
