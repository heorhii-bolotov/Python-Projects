import numpy as np
import matplotlib.pyplot as plt

E = 21.2
R = [200, 300, 500]
U = [20.5, 20.8, 20.9]
I = [96, 65, 40]

c = 1
for u, i in zip(U, I):
    print(f'R{c} {round((E - u) / (i / 1000), 2)} Ом')
    c += 1

plt.plot(I, U, 'bo')
plt.plot(I, U, label='Реальне джерело', lw=3)
plt.plot(np.linspace(min(I), max(I), 3), [max(U)] * 3, label='Ідеальне', lw=2)
plt.title('ВАХ джерела напруги G1')
plt.xlabel('I, mA')
plt.ylabel('U, B')
plt.grid(True)
plt.legend()

# plt.show()
plt.savefig('/Users/macair/Desktop/temk1.png', bbox_inches='tight')