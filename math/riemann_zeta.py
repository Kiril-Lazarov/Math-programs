from matplotlib import pyplot as plt


n = 100

r = []
i = []
result = 0 + 0j
for number in range(1, n+1):
    result += 1/(number**(1/2 + 21.022039639j))
    r.append(result.real)
    i.append(result.imag)

plt.title("Reimann Zeta partial sum S = 1/2 + 21.022039639i n = 100")
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True, color = "k")
plt.plot(r,i)
plt.show()

# CDC4VCJASc0ZBHe1ZrXGM6BFUbGqp7nUAe3cbIkFUKfbjitPsLKOocvbGWyM6i78
#
# oJkghtV3LZFCCeJ8Vj7TA9TCdVVQzY9ezcZpygCiQPMwY5pzv2gCIT2UwYOJDhEd