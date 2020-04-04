#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import argparse
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import associate

file_acc_gt = os.path.abspath('.') + '/imu_bias_gt/acc_bias_gt.txt'
file_gyro_gt = os.path.abspath('.') + '/imu_bias_gt/gyro_bias_gt.txt'
file_acc_est = os.path.abspath('.') + '/acc_bias_estimate.txt'
file_gyro_est = os.path.abspath('.') + '/gyro_bias_estimate.txt'
file_acc_match = os.path.abspath('.') + '/match_acc_bias_gt_est.txt'
file_gyro_match = os.path.abspath('.') + '/match_gyro_bias_gt_est.txt'

def plot_imu_bias_gt():
    fig1, (ax11, ax12) = plt.subplots(2, 1, figsize=(6, 5))
    acc_bias_gt_x = []
    acc_bias_gt = []
    acc_bias_gt_x = np.loadtxt(file_acc_gt, usecols = (0))
    acc_bias_gt = np.loadtxt(file_acc_gt, usecols = (1, 2, 3))
    ## 画图: acc bias groundtruth
    ax11.plot(acc_bias_gt_x, acc_bias_gt[:, 0], linewidth=0.8, color='r', label='x')
    ax11.plot(acc_bias_gt_x, acc_bias_gt[:, 1], linewidth=0.8, color='g', label='y')
    ax11.plot(acc_bias_gt_x, acc_bias_gt[:, 2], linewidth=0.8, color='b', label='z')
    ax11.set_ylabel('acc_bias_gt [m/s^2]', fontsize=10)
    ax11.tick_params(labelsize=9)
    ax11.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax11.grid(linestyle="--")

    gyro_bias_gt_x = []
    gyro_bias_gt = []
    gyro_bias_gt_x = np.loadtxt(file_gyro_gt, usecols = (0))
    gyro_bias_gt = np.loadtxt(file_gyro_gt, usecols = (1, 2, 3))
    ## 画图: gyro bias groundtruth
    ax12.plot(gyro_bias_gt_x, gyro_bias_gt[:, 0], linewidth=0.8, color='r', label='x')
    ax12.plot(gyro_bias_gt_x, gyro_bias_gt[:, 1], linewidth=0.8, color='g', label='y')
    ax12.plot(gyro_bias_gt_x, gyro_bias_gt[:, 2], linewidth=0.8, color='b', label='z')
    ax12.set_xlabel('t [s]', fontsize=10)
    ax12.set_ylabel('gyro_bias_gt [rad/s]', fontsize=10)
    ax12.tick_params(labelsize=9)
    ax12.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax12.grid(linestyle="--")


def plot_imu_bias_est():
    fig2, (ax21, ax22) = plt.subplots(2, 1, figsize=(6, 5))
    acc_bias_est_x = []
    acc_bias_est = []
    acc_bias_est_x = np.loadtxt(file_acc_est, usecols = (0))
    acc_bias_est = np.loadtxt(file_acc_est, usecols = (1, 2, 3))
    ## 画图: acc bias estimate
    ax21.plot(acc_bias_est_x, acc_bias_est[:, 0], linewidth=1.0, color='r', label='x')
    ax21.plot(acc_bias_est_x, acc_bias_est[:, 1], linewidth=1.0, color='g', label='y')
    ax21.plot(acc_bias_est_x, acc_bias_est[:, 2], linewidth=1.0, color='b', label='z')
    ax21.set_ylabel('acc_bias_est [m/s^2]', fontsize=10)
    ax21.tick_params(labelsize=9)
    ax21.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax21.grid(linestyle="--")

    gyro_bias_est_x = []
    gyro_bias_est = []
    gyro_bias_est_x = np.loadtxt(file_gyro_est, usecols = (0))
    gyro_bias_est = np.loadtxt(file_gyro_est, usecols = (1, 2, 3))
    ## 画图: gyro bias estimate
    ax22.plot(gyro_bias_est_x, gyro_bias_est[:, 0], linewidth=1.0, color='r', label='x')
    ax22.plot(gyro_bias_est_x, gyro_bias_est[:, 1], linewidth=1.0, color='g', label='y')
    ax22.plot(gyro_bias_est_x, gyro_bias_est[:, 2], linewidth=1.0, color='b', label='z')
    ax22.set_xlabel('t [s]', fontsize=10)
    ax22.set_ylabel('gyro_bias_est [rad/s]', fontsize=10)
    ax22.tick_params(labelsize=9)
    ax22.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax22.grid(linestyle="--")


def plot_imu_bias_error():
    fig3, (ax31, ax32) = plt.subplots(2, 1, figsize=(6, 5))
    fig3.tight_layout()
    acc_bias_match_x = np.loadtxt(file_acc_match, usecols = (0))
    acc_bias_match_gt = np.loadtxt(file_acc_match, usecols = (1, 2, 3))
    acc_bias_match_est = np.loadtxt(file_acc_match, usecols = (5, 6, 7))
    diff_acc_bias = np.array(acc_bias_match_est) - np.array(acc_bias_match_gt)
    ## 画图: diff acc bias
    ax31.plot(acc_bias_match_x, diff_acc_bias[:, 0], linewidth=0.8, color='r', label='x')
    ax31.plot(acc_bias_match_x, diff_acc_bias[:, 1], linewidth=0.8, color='g', label='y')
    ax31.plot(acc_bias_match_x, diff_acc_bias[:, 2], linewidth=0.8, color='b', label='z')
    ax31.set_xlabel('t [s]', fontsize=10)
    ax31.set_ylabel('acc_bias err. [m/s^2]', fontsize=10)
    ax31.tick_params(labelsize=9)
    ax31.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax31.grid(linestyle="--")

    gyro_bias_match_x = np.loadtxt(file_gyro_match, usecols = (0))
    gyro_bias_match_gt = np.loadtxt(file_gyro_match, usecols = (1, 2, 3))
    gyro_bias_match_est = np.loadtxt(file_gyro_match, usecols = (5, 6, 7))
    diff_gyro_bias = np.array(gyro_bias_match_est) - np.array(gyro_bias_match_gt)
    ## 画图: diff gyro bias
    ax32.plot(gyro_bias_match_x, diff_gyro_bias[:, 0], linewidth=0.8, color='r', label='x')
    ax32.plot(gyro_bias_match_x, diff_gyro_bias[:, 1], linewidth=0.8, color='g', label='y')
    ax32.plot(gyro_bias_match_x, diff_gyro_bias[:, 2], linewidth=0.8, color='b', label='z')
    ax32.set_xlabel('t [s]', fontsize=10)
    ax32.set_ylabel('gyro_bias err. [rad/s]', fontsize=10)
    ax32.tick_params(labelsize=9)
    ax32.legend(loc='upper right', fontsize=8, edgecolor='w')
    ax32.grid(linestyle="--")


if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='''
    This script computes the absolute trajectory error from the ground truth trajectory and the estimated trajectory. 
    ''')
    parser.add_argument('--offset', help='time offset added to the timestamps of the second file (default: 0.0)', default=0.0)
    parser.add_argument('--scale', help='scaling factor for the second trajectory (default: 1.0)', default=1.0)
    parser.add_argument('--max_difference', help='maximally allowed time difference for matching entries (default: 0.02)', default=0.02)
    parser.add_argument('--save_acc', help='save associated first and aligned second trajectory to disk (format: stamp1 bias_x bias_y bias_z stamp2 bias_x bias_y bias_z)')
    parser.add_argument('--save_gyro', help='save associated first and aligned second trajectory to disk (format: stamp1 bias_x bias_y bias_z stamp2 bias_x bias_y bias_z)')
    parser.add_argument('-p', help='plot', action='store_true')
    args = parser.parse_args()

    acc_gt = associate.read_file_list(file_acc_gt)
    acc_est = associate.read_file_list(file_acc_est)
    matches_acc = associate.associate(acc_gt, acc_est, float(args.offset), float(args.max_difference))    
    if len(matches_acc)<2:
        sys.exit("Couldn't find matching timestamp pairs between groundtruth and estimated trajectory! Did you choose the correct sequence?")

    gyro_gt = associate.read_file_list(file_gyro_gt)
    gyro_est = associate.read_file_list(file_gyro_est)
    matches_gyro = associate.associate(gyro_gt, gyro_est, float(args.offset), float(args.max_difference))    
    if len(matches_gyro)<2:
        sys.exit("Couldn't find matching timestamp pairs between groundtruth and estimated trajectory! Did you choose the correct sequence?")

    if args.save_acc:
        file = open(args.save_acc,"w")
        file.write("\n".join(["%f %s %f %s"%(a, " ".join(acc_gt[a]), b-float(args.offset), " ".join(acc_est[b])) for a,b in matches_acc]))
        file.close()

    if args.save_gyro:
        file = open(args.save_gyro,"w")
        file.write("\n".join(["%f %s %f %s"%(a, " ".join(gyro_gt[a]), b-float(args.offset), " ".join(gyro_est[b])) for a,b in matches_acc]))
        file.close()

    if args.p:
        plot_imu_bias_gt()
        plot_imu_bias_est()
        plot_imu_bias_error()
        plt.show()
