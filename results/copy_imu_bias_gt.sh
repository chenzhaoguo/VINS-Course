#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

rm -rf ./imu_bias_gt/*

cp ../../../01-chapter2_IMU/vio_data_simulation/bin/acc_bias.txt ./imu_bias_gt/
cp ../../../01-chapter2_IMU/vio_data_simulation/bin/gyro_bias.txt ./imu_bias_gt/
