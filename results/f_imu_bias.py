#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

filepath_estimate = os.path.abspath('..') + "/bin"
filepath_gt = os.path.abspath('./imu_bias_gt')

col_index = 0

########  imu bias estimate  ########
acc_bias_estimate = []
acc_bias_estimate_x = np.loadtxt(filepath_estimate + '/acc_bias_estimate.txt', usecols = (col_index))
acc_bias_estimate = np.loadtxt(filepath_estimate + '/acc_bias_estimate.txt', usecols = (col_index+1, col_index+2, col_index+3))
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
gyro_bias_estimate_x = np.loadtxt(filepath_estimate + '/gyro_bias_estimate.txt', usecols = (col_index))
gyro_bias_estimate = np.loadtxt(filepath_estimate + '/gyro_bias_estimate.txt', usecols = (col_index+1, col_index+2, col_index+3))
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


########  imu bias groundtruth  ########
acc_bias_gt = []
acc_bias_gt_x = np.loadtxt(filepath_gt + '/acc_bias_gt.txt', usecols = (col_index))
acc_bias_gt = np.loadtxt(filepath_gt + '/acc_bias_gt.txt', usecols = (col_index+1, col_index+2, col_index+3))
## 画图: acc bias groundtruth
fig = plt.figure(3)
plt.plot(acc_bias_gt_x, acc_bias_gt[:, 0], linewidth=1.0, color="red", label='X')
plt.plot(acc_bias_gt_x, acc_bias_gt[:, 1], linewidth=1.0, color="green", label='Y')
plt.plot(acc_bias_gt_x, acc_bias_gt[:, 2], linewidth=1.0, color="blue", label='Z')
plt.xlabel('time [s]')
plt.ylabel('acc_bias_gt [rad/s]')
plt.title("acc_bias groundtruth", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")

gyro_bias_gt = []
gyro_bias_gt_x = np.loadtxt(filepath_gt + '/gyro_bias_gt.txt', usecols = (col_index))
gyro_bias_gt = np.loadtxt(filepath_gt + '/gyro_bias_gt.txt', usecols = (col_index+1, col_index+2, col_index+3))
## 画图: gyro bias groundtruth
fig = plt.figure(4)
plt.plot(gyro_bias_gt_x, gyro_bias_gt[:, 0], linewidth=1.0, color="red", label='X')
plt.plot(gyro_bias_gt_x, gyro_bias_gt[:, 1], linewidth=1.0, color="green", label='Y')
plt.plot(gyro_bias_gt_x, gyro_bias_gt[:, 2], linewidth=1.0, color="blue", label='Z')
plt.xlabel('time [s]')
plt.ylabel('gyro_bias_gt [rad/s]')
plt.title("gyro_bias groundtruth", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")


########  imu bias error  ########
row_index = np.arange(248, 3989, 20)
acc_data_gt_select = []
with open(filepath_gt + '/acc_bias_gt.txt', 'r') as f:
    data = f.readlines()
    for i in row_index:
        line = data[i-1][:-1].split()
        arr_float = map(float, line)  # 转化为浮点数
        acc_data_gt_select.append(arr_float)
acc_bias_estimate_all = np.loadtxt(filepath_estimate + '/acc_bias_estimate.txt')
diff_acc_bias = np.array(acc_bias_estimate_all) - np.array(acc_data_gt_select)
## 画图: diff acc bias
fig = plt.figure(5)
plt.plot(acc_bias_estimate_all[:, 0], diff_acc_bias[:, 1], linewidth=1.0, color="red", label='X')
plt.plot(acc_bias_estimate_all[:, 0], diff_acc_bias[:, 2], linewidth=1.0, color="green", label='Y')
plt.plot(acc_bias_estimate_all[:, 0], diff_acc_bias[:, 3], linewidth=1.0, color="blue", label='Z')
plt.plot(acc_bias_estimate_all[:, 0], diff_acc_bias[:, 0], linewidth=1.0, color="black", label='timestamp')
plt.xlabel('time [s]')
plt.ylabel('acc_bias_error [rad/s]')
plt.title("acc_bias error", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")

gyro_data_gt_select = []
with open(filepath_gt + '/gyro_bias_gt.txt', 'r') as f:
    data = f.readlines()
    for i in row_index:
        line = data[i-1][:-1].split()
        arr_float = map(float, line)  # 转化为浮点数
        gyro_data_gt_select.append(arr_float)
gyro_bias_estimate_all = np.loadtxt(filepath_estimate + '/gyro_bias_estimate.txt')
diff_gyro_bias = np.array(gyro_bias_estimate_all) - np.array(gyro_data_gt_select)
## 画图: diff gyro bias
fig = plt.figure(6)
plt.plot(gyro_bias_estimate_all[:, 0], diff_gyro_bias[:, 1], linewidth=1.0, color="red", label='X')
plt.plot(gyro_bias_estimate_all[:, 0], diff_gyro_bias[:, 2], linewidth=1.0, color="green", label='Y')
plt.plot(gyro_bias_estimate_all[:, 0], diff_gyro_bias[:, 3], linewidth=1.0, color="blue", label='Z')
plt.plot(gyro_bias_estimate_all[:, 0], diff_gyro_bias[:, 0], linewidth=1.0, color="black", label='timestamp')
plt.xlabel('time [s]')
plt.ylabel('gyro_bias_error [rad/s]')
plt.title("gyro_bias error", fontsize=12, verticalalignment='baseline', color='black')
plt.legend(loc='upper right', fontsize=8, edgecolor='black')
plt.grid(linestyle="--")

plt.show()
