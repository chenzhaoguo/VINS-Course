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

file_traj_gt = os.path.abspath('.') + '/groundtruth_MH_04.tum'
file_traj_estimate = os.path.abspath('.') + '/estimate_result.txt'
file_euler_gt = os.path.abspath('.') + '/euler_gt.txt'
file_euler_estimate = os.path.abspath('.') + '/euler_estimate.txt'
file_euler_error = os.path.abspath('.') + '/euler_error.txt'

###    plot orientaiton r/p/y    ###
euler_gt_time = np.loadtxt(file_traj_gt, usecols=(0))
euler_gt_time_relative = euler_gt_time - euler_gt_time[0]
euler_gt = np.loadtxt(file_euler_gt, usecols=(1, 2, 3))
euler_est_time = np.loadtxt(file_traj_estimate, usecols=(0))
euler_est_time_relative = euler_est_time - euler_gt_time[0]
euler_estimate = np.loadtxt(file_euler_estimate, usecols=(1, 2, 3))

fig1, (ax11, ax12, ax13) = plt.subplots(3, 1, figsize=(6, 3.5), sharex=True)
## roll
ax11.plot(euler_gt_time_relative, euler_gt[:,0], linestyle='--', linewidth=1.0, color='r')
ax11.plot(euler_est_time_relative, euler_estimate[:,0], linestyle='-', linewidth=0.8, color='b')
ax11.set_ylabel('roll [deg]', fontsize=10)
ax11.tick_params(labelsize=9)
ax11.grid(linestyle="--")
## pitch
ax12.plot(euler_gt_time_relative, euler_gt[:,1], linestyle='--', linewidth=1.0, color='r')
ax12.plot(euler_est_time_relative, euler_estimate[:,1], linestyle='-', linewidth=0.8, color='b')
ax12.set_ylabel('pitch [deg]', fontsize=10)
ax12.tick_params(labelsize=9)
ax12.grid(linestyle="--")
## yaw
ax13.plot(euler_gt_time_relative, euler_gt[:,2], linestyle='--', linewidth=1.0, color='r', label='groundtruth')
ax13.plot(euler_est_time_relative, euler_estimate[:,2], linestyle='-', linewidth=0.8, color='b', label='estimate_result')
ax13.set_ylabel('yaw [deg]', fontsize=10)
ax13.set_xlabel('t [s]', fontsize=10)
ax13.tick_params(labelsize=9)
ax13.legend(loc='upper right', fontsize=6, edgecolor='w')
ax13.grid(linestyle="--")


########  plot orientation error  ########
first_list = associate.read_file_list(file_traj_gt)
second_list = associate.read_file_list(file_traj_estimate)
matches = associate.associate(first_list, second_list, 0.0, 0.02)
time = []
for a,b in matches:
    time.append(b-euler_gt_time[0])
diff_euler = []
diff_euler = np.loadtxt(file_euler_error, usecols=(1, 2, 3))

fig2, ax2 = plt.subplots(figsize=(6, 3))
ax2.plot(time, diff_euler[:, 0], linewidth=1.0, color='r',label='roll')
ax2.plot(time, diff_euler[:, 1], linewidth=1.0, color='g', label='pitch')
ax2.plot(time, diff_euler[:, 2], linewidth=1.0, color='b', label='yaw')
ax2.set_xlabel('t [s]', fontsize=10)
ax2.set_ylabel('orientation err. [deg]', fontsize=10)
ax2.tick_params(labelsize=9)
ax2.legend(loc='upper right', fontsize=8, edgecolor='w')
ax2.grid(linestyle="--")
## add small figure
insert_ax = fig2.add_axes([0.70, 0.33, 0.18, 0.20])
insert_ax.plot(time, diff_euler[:, 0], linewidth=0.8, color='r', label='roll')
insert_ax.plot(time, diff_euler[:, 1], linewidth=0.8, color='g', label='pitch')
insert_ax.plot(time, diff_euler[:, 2], linewidth=0.8, color='b', label='yaw')
insert_ax.set_xlim(0, 100)
insert_ax.set_ylim(-4, 2)
insert_ax.tick_params(labelsize=7)
insert_ax.grid(linestyle="--")

plt.show()
