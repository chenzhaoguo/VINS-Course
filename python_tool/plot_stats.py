## -*- coding: utf-8 -*-

import numpy as np  
import matplotlib
import matplotlib.pyplot as plt

items = ['rmse', 'mean', 'max', 'min', 'std']
x = range(len(items))

num_1 = [0.011746, 0.010975, 0.022335, 0.003204, 0.004185]
num_2 = [0.025247, 0.023003, 0.063963, 0.007240, 0.010406]
num_3 = [0.074576, 0.070127, 0.137405, 0.029634, 0.025371]
num_4 = [0.243541, 0.226555, 0.493655, 0.089706, 0.089357]

fig, ax = plt.subplots()
ax.bar(x, num_1, width=0.1, facecolor='r', label='1')
ax.bar([i+0.1 for i in x], num_2, width=0.1, facecolor='g', label='2')
ax.bar([i+0.2 for i in x], num_3, width=0.1, facecolor='b', label='3')
ax.bar([i+0.3 for i in x], num_4, width=0.1, facecolor='tab:orange', label='4')
## move x_label
ax.set_xticks([i+0.15 for i in x], items)
ax.legend(loc='upper right', fontsize=8, edgecolor='k')

plt.show()
