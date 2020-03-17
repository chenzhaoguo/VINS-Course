#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

cp ../../../01-chapter2_IMU/vio_data_simulation/bin/imu_output.txt .
cp ../../../01-chapter2_IMU/vio_data_simulation/bin/groundtruth_tum.txt .
cp ../../../01-chapter2_IMU/vio_data_simulation/bin/camera_pose_tum.txt .
cp -r ../../../01-chapter2_IMU/vio_data_simulation/bin/keyframe .