#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import numpy as np
import argparse
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import associate

np.set_printoptions(suppress = True)
filepath = os.path.abspath('.') + "/"

first_list = associate.read_file_list("./groundtruth_MH_04.tum")
second_list = associate.read_file_list("./estimate_result.txt")
matches = associate.associate(first_list, second_list, 0.0, 0.02)
first_stamps = first_list.keys()
first_stamps.sort()
time = []
for a,b in matches:
    time.append(b-first_stamps[0])

###    plot orientaiton r/p/y    ###
euler_gt = np.loadtxt(filepath + 'euler_gt.txt', usecols=(1, 2, 3))
euler_estimate = np.loadtxt(filepath + 'euler_estimate.txt', usecols=(1, 2, 3))
fig = plt.figure(1)
plt.subplot(311)
plt.plot(time, euler_gt[:,0], '--', linewidth=1.0, color="red", label='groundtruth')
plt.plot(time, euler_estimate[:,0], '-', linewidth=1.0, color="blue", label='estimate_result')
plt.ylabel('roll [deg]')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")
plt.subplot(312)
plt.plot(time, euler_gt[:,1], '--', linewidth=1.0, color="red")
plt.plot(time, euler_estimate[:,1], '-', linewidth=1.0, color="blue")
plt.ylabel('pitch [deg]')
plt.grid(linestyle="--")
plt.subplot(313)
plt.plot(time, euler_gt[:,2], '--', linewidth=1.0, color="red")
plt.plot(time, euler_estimate[:,2], '-', linewidth=1.0, color="blue")
plt.ylabel('yaw [deg]')
plt.xlabel('t [s]')
plt.grid(linestyle="--")

########  plot orientation error  ########
diff_euler = []
diff_euler = np.loadtxt(filepath + 'euler_error.txt', usecols=(1, 2, 3))
## 画图:
fig = plt.figure(2)
plt.plot(time, diff_euler[:, 0], linewidth=1.0, color="red", label='roll')
plt.plot(time, diff_euler[:, 1], linewidth=1.0, color="green", label='pitch')
plt.plot(time, diff_euler[:, 2], linewidth=1.0, color="blue", label='yaw')
plt.xlabel('t [s]')
plt.ylabel('orientation error [deg]')
plt.legend(loc='upper right', fontsize=9, edgecolor='black')
plt.grid(linestyle="--")

plt.show()
