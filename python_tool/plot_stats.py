## -*- coding: utf-8 -*-

import numpy as np  
import matplotlib
import matplotlib.pyplot as plt

plt.figure()

items = ['rmse', 'mean', 'max', 'min', 'std']

num_1 = [0.011746, 0.010975, 0.022335, 0.003204, 0.004185]
num_2 = [0.025247, 0.023003, 0.063963, 0.007240, 0.010406]
num_3 = [0.074576, 0.070127, 0.137405, 0.029634, 0.025371]
num_4 = [0.243541, 0.226555, 0.493655, 0.089706, 0.089357]

x = range(len(items))
plt.bar(x, num_1, width=0.1, facecolor='red', label='1')
plt.bar([i+0.1 for i in x], num_2, width=0.1, facecolor='green', label='2')
plt.bar([i+0.2 for i in x], num_3, width=0.1, facecolor='blue', label='3')
plt.bar([i+0.3 for i in x], num_4, width=0.1, facecolor='orange', label='4')
## move x_label
plt.xticks([i+0.15 for i in x], items)

plt.legend(loc='upper right', fontsize=8, edgecolor='black')
# plt.grid(linestyle="--")

plt.show()
