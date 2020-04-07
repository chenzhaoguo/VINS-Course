#!/usr/bin/python
# Requirements: 
# sudo apt-get install python-argparse

"""
This script computes the absolute trajectory error from the ground truth
trajectory and the estimated trajectory.
"""

import os
import sys
import math
import numpy as np
import argparse
import associate
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_gt = os.path.abspath('.') + '/groundtruth_tum.txt'
file_estimate = os.path.abspath('.') + '/estimate_result.txt'
file_ins_int = os.path.abspath('.') + '/imu_int_pose_noise.txt'
file_euler_error = os.path.abspath('.') + '/euler_error.txt'
file_euler_gt = os.path.abspath('.') + '/euler_gt.txt'

def align(model,data):
    """Align two trajectories using the method of Horn (closed-form).
    Input:
    model -- first trajectory (3xn)
    data -- second trajectory (3xn)
    
    Output:
    rot -- rotation matrix (3x3)
    trans -- translation vector (3x1)
    trans_error -- translational error per point (1xn)
    """
    np.set_printoptions(precision=3,suppress=True)
    model_zerocentered = model - model.mean(1)
    data_zerocentered = data - data.mean(1)
    
    W = np.zeros( (3,3) )
    for column in range(model.shape[1]):
        W += np.outer(model_zerocentered[:,column],data_zerocentered[:,column])
    U,d,Vh = np.linalg.linalg.svd(W.transpose())
    S = np.matrix(np.identity( 3 ))
    if(np.linalg.det(U) * np.linalg.det(Vh)<0):
        S[2,2] = -1
    rot = U*S*Vh
    trans = data.mean(1) - rot * model.mean(1)
    
    model_aligned = rot * model + trans
    alignment_error = model_aligned - data
    
    trans_error = np.sqrt(np.sum(np.multiply(alignment_error,alignment_error),0)).A[0]
        
    return rot,trans,trans_error


def plot_traj(ax, stamps, traj, style, linewidth, color, label):
    """
    Plot a trajectory using matplotlib. 
    Input:
    ax -- the plot
    stamps -- time stamps (1xn)
    traj -- trajectory (3xn)
    style -- line style
    color -- line color
    label -- plot legend
    """
    stamps.sort()
    interval = np.median([s-t for s,t in zip(stamps[1:],stamps[:-1])])
    x = []
    y = []
    z = []
    last = stamps[0]
    for i in range(len(stamps)):
        if stamps[i]-last < 2*interval:
            x.append(traj[i][0])
            y.append(traj[i][1])
            z.append(traj[i][2])
        elif len(x)>0:
            ax.plot(x, y, z, style, linewidth=linewidth, color=color, label=label)
            label = ""
            x= []
            y= []
            z= []
        last= stamps[i]
    if len(x)>0:
        ax.plot(x, y, z, style, linewidth=linewidth, color=color, label=label)


if __name__=="__main__":
    # parse command line
    parser = argparse.ArgumentParser(description='''
    This script computes the absolute trajectory error from the ground truth trajectory and the estimated trajectory. 
    ''')
    parser.add_argument('--offset', help='time offset added to the timestamps of the second file (default: 0.0)',default=0.0)
    parser.add_argument('--scale', help='scaling factor for the second trajectory (default: 1.0)',default=1.0)
    parser.add_argument('--max_difference', help='maximally allowed time difference for matching entries (default: 0.02)',default=0.02)
    parser.add_argument('--save_aligned', help='save aligned second trajectory to disk (format: stamp2 x2 y2 z2)')
    parser.add_argument('--save_position', help='save associated first and aligned second trajectory to disk (format: stamp1 x1 y1 z1 stamp2 x2 y2 z2)')
    parser.add_argument('--save', help='save associated first and aligned second trajectory to disk (format: stamp1 x1 y1 z1 qx1 qy1 qz1 qw1 stamp2 x2 y2 z2 qx2 qy2 qz2 qw2)')
    args = parser.parse_args()

    first_list = associate.read_file_list(file_gt)
    second_list = associate.read_file_list(file_estimate)
    matches = associate.associate(first_list, second_list, float(args.offset), float(args.max_difference))    
    if len(matches)<2:
        sys.exit("Couldn't find matching timestamp pairs between groundtruth and estimated trajectory! Did you choose the correct sequence?")

    first_xyz = np.matrix([[float(value) for value in first_list[a][0:3]] for a,b in matches]).transpose()
    second_xyz = np.matrix([[float(value)*float(args.scale) for value in second_list[b][0:3]] for a,b in matches]).transpose()
    rot,trans,trans_error = align(second_xyz,first_xyz)
    
    second_xyz_aligned = rot * second_xyz + trans
    
    first_stamps = first_list.keys()
    first_stamps.sort()
    first_xyz_full = np.matrix([[float(value) for value in first_list[b][0:3]] for b in first_stamps]).transpose()
    
    second_stamps = second_list.keys()
    second_stamps.sort()
    second_xyz_full = np.matrix([[float(value)*float(args.scale) for value in second_list[b][0:3]] for b in second_stamps]).transpose()
    second_xyz_full_aligned = rot * second_xyz_full + trans


    ###    plot trajectory    ###
    fig1 = plt.figure(num=1, figsize=(6, 4))
    ax1 = fig1.gca(projection='3d')
    traj_gt_time = []
    traj_gt = []
    traj_gt_time = np.loadtxt(file_gt, usecols=(0))
    traj_gt = np.loadtxt(file_gt, usecols=(1, 2, 3))
    traj_ins_int = np.loadtxt(file_ins_int, usecols=(5, 6, 7))
    ax1.plot(traj_gt[:,0], traj_gt[:,1], traj_gt[:,2], linestyle='--', linewidth=1.0, color='r', label='ground truth')
    ax1.plot([traj_gt[0, 0]], [traj_gt[0, 1]], [traj_gt[0, 2]], 'o', markersize=4, color='r', label='start&end point')
    ax1.plot(traj_ins_int[:, 0], traj_ins_int[:, 1], traj_ins_int[:, 2], linestyle='-', linewidth=0.8, color='g', label='INS')
    plot_traj(ax1, second_stamps, second_xyz_full_aligned.transpose().A, '-', 0.8, 'b', 'Visual-Inertial system')
    ax1.set_xlabel('x [m]', fontsize=10)
    ax1.set_ylabel('y [m]', fontsize=10)
    ax1.set_zlabel('z [m]', fontsize=10)
    ax1.tick_params(labelsize=9)
    ax1.legend(loc='upper right', fontsize=7, edgecolor='w')
    ax1.grid(linestyle="--")


    ###    plot position error of x/y/z    ###
    fig2, (ax21, ax22) = plt.subplots(2, 1, figsize=(4.5, 4.0))
    ## ins
    diff_ins_x = np.loadtxt(file_ins_int, usecols=(0))
    diff_position_noise = np.array(traj_ins_int) - np.array(traj_gt[1:8001])
    ax21.plot(diff_ins_x, diff_position_noise[:, 0], linewidth=1.0, color='r', label='x')
    ax21.plot(diff_ins_x, diff_position_noise[:, 1], linewidth=1.0, color='g', label='y')
    ax21.plot(diff_ins_x, diff_position_noise[:, 2], linewidth=1.0, color='b', label='z')
    ax21.set_ylabel('translation err. [m]', fontsize=10)
    ax21.set_title('INS', fontsize=10)
    ax21.tick_params(labelsize=9)
    ax21.legend(loc='upper right', fontsize=7, edgecolor='w')
    ax21.grid(linestyle="--")

    ## visual-inertial
    time2 = []
    diff_x = []
    diff_y = []
    diff_z = []
    for (a,b),(x1,y1,z1),(x2,y2,z2) in zip(matches, first_xyz.transpose().A, second_xyz_aligned.transpose().A):
        time2.append(b-traj_gt_time[0])
        diff_x.append(x2-x1)
        diff_y.append(y2-y1)
        diff_z.append(z2-z1)
    ax22.plot(time2, diff_x, linewidth=1.0, color='r', label='x')
    ax22.plot(time2, diff_y, linewidth=1.0, color='g', label='y')
    ax22.plot(time2, diff_z, linewidth=1.0, color='b', label='z')
    ax22.set_xlabel('t [s]', fontsize=10)
    ax22.set_ylabel('translation err. [m]', fontsize=10)
    # ax22.set_title('Visual-Inertial system', fontsize=10)
    ax22.tick_params(labelsize=9)
    ax22.legend(loc='upper right', fontsize=7, edgecolor='w')
    ax22.grid(linestyle="--")


    ###    plot euler error of roll/pitch/yaw    ###
    fig3, (ax31, ax32) = plt.subplots(2, 1, figsize=(4.5, 4.0))
    ## ins
    euler_int_noise_rad = []
    euler_int_noise_x = np.loadtxt(file_ins_int, usecols=(0))
    euler_int_noise_rad = np.loadtxt(file_ins_int, usecols=(8, 9 ,10))
    euler_int_noise_deg = euler_int_noise_rad * 180 / math.pi
    euler_gt = np.loadtxt(file_euler_gt, usecols=(1, 2, 3))
    diff_euler_int_noise_deg = np.array(euler_int_noise_deg) - np.array(euler_gt[1:8001])
    ax31.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 0], linewidth=1.0, color='r', label='roll')
    ax31.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 1], linewidth=1.0, color='g', label='pitch')
    ax31.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 2], linewidth=1.0, color='b', label='yaw')
    ax31.set_ylabel('rotation err. [deg]', fontsize=10)
    ax31.set_title('INS', fontsize=10)
    ax31.tick_params(labelsize=9)
    ax31.legend(loc='upper right', fontsize=7, edgecolor='w')
    ax31.grid(linestyle="--")
    ## add small figure
    insert_ax1 = fig3.add_axes([0.54, 0.60, 0.30, 0.15])
    insert_ax1.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 0], linewidth=0.7, color='r', label='roll')
    insert_ax1.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 1], linewidth=0.7, color='g', label='pitch')
    insert_ax1.plot(euler_int_noise_x, diff_euler_int_noise_deg[:, 2], linewidth=0.7, color='b', label='yaw')
    insert_ax1.set_xlim(0, 40.0)
    insert_ax1.set_ylim(-0.8, 0.8)
    insert_ax1.tick_params(labelsize=6.5)
    insert_ax1.grid(linestyle="--")

    ## visual-inertial
    time = []
    for a,b in matches:
        time.append(b-traj_gt_time[0])
    diff_euler = []
    diff_euler = np.loadtxt(file_euler_error, usecols=(1, 2, 3))
    ax32.plot(time, diff_euler[:, 0], linewidth=1.0, color='r',label='roll')
    ax32.plot(time, diff_euler[:, 1], linewidth=1.0, color='g', label='pitch')
    ax32.plot(time, diff_euler[:, 2], linewidth=1.0, color='b', label='yaw')
    ax32.set_xlabel('t [s]', fontsize=10)
    ax32.set_ylabel('rotation err. [deg]', fontsize=10)
    # ax32.set_title('Visual-Inertial system', fontsize=10)
    ax32.tick_params(labelsize=9)
    ax32.legend(loc='upper right', fontsize=7, edgecolor='w')
    ax32.grid(linestyle="--")
    ## add small figure
    insert_ax2 = fig3.add_axes([0.54, 0.18, 0.30, 0.15])
    insert_ax2.plot(time, diff_euler[:, 0], linewidth=0.9, color='r', label='roll')
    insert_ax2.plot(time, diff_euler[:, 1], linewidth=0.9, color='g', label='pitch')
    insert_ax2.plot(time, diff_euler[:, 2], linewidth=0.9, color='b', label='yaw')
    insert_ax2.set_xlim(0, 40)
    insert_ax2.set_ylim(-0.4, 0.4)
    insert_ax2.tick_params(labelsize=6.5)
    insert_ax2.grid(linestyle="--")

    plt.show()
