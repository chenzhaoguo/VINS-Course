#!/usr/bin/python
# Requirements: 
# sudo apt-get install python-argparse

"""
This script computes the absolute trajectory error from the ground truth
trajectory and the estimated trajectory.
"""

import sys
import numpy as np
import argparse
import associate
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

    first_list = associate.read_file_list("./groundtruth_MH_04.tum")
    second_list = associate.read_file_list("./estimate_result.txt")
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

    ###    output result    ###
    print "compared_pose_pairs %d pairs"%(len(trans_error))
    print "APE.rmse %f m"%np.sqrt(np.dot(trans_error,trans_error) / len(trans_error))
    print "APE.mean %f m"%np.mean(trans_error)
    print "APE.median %f m"%np.median(trans_error)
    print "APE.std %f m"%np.std(trans_error)
    print "APE.min %f m"%np.min(trans_error)
    print "APE.max %f m"%np.max(trans_error)

    ###    plot trajectory    ###
    traj_gt_time = np.loadtxt('./groundtruth_MH_04.tum', usecols=(0))
    traj_gt_time_relative = traj_gt_time - traj_gt_time[0]
    traj_gt = np.loadtxt('./groundtruth_MH_04.tum', usecols=(1, 2, 3))
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    plt.plot(traj_gt[:,0], traj_gt[:,1], traj_gt[:,2], '--', linewidth=1.0, color="red", label='groundtruth')
    plot_traj(ax, second_stamps, second_xyz_full_aligned.transpose().A, '-', 0.7, "blue", "estimate_result")
    ax.legend(loc='upper right', fontsize=8, edgecolor='black')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    plt.grid(linestyle="--")

    ###    plot trajectory x/y/z    ###
    time1 = []
    pose_x_est = []
    pose_y_est = []
    pose_z_est = []
    for (a,b),(x1,y1,z1),(x2,y2,z2) in zip(matches,first_xyz.transpose().A, second_xyz_aligned.transpose().A):
        time1.append(b-traj_gt_time[0])
        pose_x_est.append(x2)
        pose_y_est.append(y2)
        pose_z_est.append(z2)
    fig = plt.figure(2)
    plt.subplot(311)
    plt.plot(traj_gt_time_relative, traj_gt[:,0], '--', linewidth=1.2, color="red", label='groundtruth')
    plt.plot(time1, pose_x_est, '-', linewidth=0.7, color="blue", label='estimate_result')
    plt.ylabel('x [m]')
    plt.legend(loc='upper right', fontsize=6, edgecolor='black')
    plt.grid(linestyle="--")
    plt.subplot(312)
    plt.plot(traj_gt_time_relative, traj_gt[:,1], '--', linewidth=1.2, color="red")
    plt.plot(time1, pose_y_est, '-', linewidth=0.7, color="blue")
    plt.ylabel('y [m]')
    plt.grid(linestyle="--")
    plt.subplot(313)
    plt.plot(traj_gt_time_relative, traj_gt[:,2], '--', linewidth=1.2, color="red")
    plt.plot(time1, pose_z_est, '-', linewidth=0.7, color="blue")
    plt.ylabel('z [m]')
    plt.xlabel('t [s]')
    plt.grid(linestyle="--")

    ###    plot position error of x/y/z    ###
    time2 = []
    diff_x = []
    diff_y = []
    diff_z = []
    for (a,b),(x1,y1,z1),(x2,y2,z2) in zip(matches,first_xyz.transpose().A, second_xyz_aligned.transpose().A):
        time2.append(b-traj_gt_time[0])
        diff_x.append(x2-x1)
        diff_y.append(y2-y1)
        diff_z.append(z2-z1)
    fig = plt.figure(3)
    plt.plot(time2, diff_x, linewidth=1.0, color="red", label='x')
    plt.plot(time2, diff_y, linewidth=1.0, color="green", label='y')
    plt.plot(time2, diff_z, linewidth=1.0, color="blue", label='z')
    plt.xlabel('t [s]')
    plt.ylabel('positon error[m]')
    plt.legend(loc='upper right', fontsize=8, edgecolor='black')
    plt.grid(linestyle="--")

    plt.show()
    
    if args.save_position:
        file = open(args.save_position,"w")
        file.write("\n".join(["%f %f %f %f %f %f %f %f"%(a,x1,y1,z1,b,x2,y2,z2) for (a,b),(x1,y1,z1),(x2,y2,z2) in zip(matches,first_xyz.transpose().A,second_xyz_aligned.transpose().A)]))
        file.close()
    
    if args.save_aligned:
        file = open(args.save_aligned,"w")
        file.write("\n".join(["%f "%stamp+" ".join(["%f"%d for d in line]) for stamp,line in zip(second_stamps,second_xyz_full_aligned.transpose().A)]))
        file.close()

    if args.save:
        file = open(args.save,"w")
        file.write("\n".join(["%f %s %f %s"%(a, " ".join(first_list[a]), b-float(args.offset), " ".join(second_list[b])) for a,b in matches]))
        file.close()
        