#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.set_printoptions(suppress = True)
filepath = os.path.abspath('.') + "/"

col_index = 0

########  imu bias estimate  ########
acc_bias_estimate = []
acc_bias_estimate_x = np.loadtxt(filepath + 'acc_bias_estimate.txt', usecols = (col_index))
acc_bias_estimate = np.loadtxt(filepath + 'acc_bias_estimate.txt', usecols = (col_index+1, col_index+2, col_index+3))
## 画图: acc bias estimate
fig = plt.figure(1)
plt.plot(acc_bias_estimate_x, acc_bias_estimate[:, 0], linewidth=1.0, color="red", label='X')
plt.plot(acc_bias_estimate_x, acc_bias_estimate[:, 1], linewidth=1.0, color="green", label='Y')
plt.plot(acc_bias_estimate_x, acc_bias_estimate[:, 2], linewidth=1.0, color="blue", label='Z')
plt.xlabel('time [s]')
plt.ylabel('acc_bias_estimate [rad/s]')
plt.title("acc_bias estimate", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")

gyro_bias_estimate = []
gyro_bias_estimate_x = np.loadtxt(filepath + 'gyro_bias_estimate.txt', usecols = (col_index))
gyro_bias_estimate = np.loadtxt(filepath + 'gyro_bias_estimate.txt', usecols = (col_index+1, col_index+2, col_index+3))
## 画图: gyro bias estimate
fig = plt.figure(2)
plt.plot(gyro_bias_estimate_x, gyro_bias_estimate[:, 0], linewidth=1.0, color="red", label='X')
plt.plot(gyro_bias_estimate_x, gyro_bias_estimate[:, 1], linewidth=1.0, color="green", label='Y')
plt.plot(gyro_bias_estimate_x, gyro_bias_estimate[:, 2], linewidth=1.0, color="blue", label='Z')
plt.xlabel('time [s]')
plt.ylabel('gyro_bias_estimate [rad/s]')
plt.title("gyro_bias estimate", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")

plt.show()
