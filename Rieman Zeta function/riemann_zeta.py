from matplotlib import pyplot as plt

n = 2000

r = []
i = []
result = 0 + 0j
for number in range(1, n+1):
    result += 1/(number**(1/2 + 4j))
    r.append(result.real)
    i.append(result.imag)

plt.title("Reimann Zeta partial sum S = 1/2 + 4i n = 2000")
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True, color = "k")
plt.plot(r,i)
plt.show()