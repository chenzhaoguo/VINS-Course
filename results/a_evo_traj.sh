#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

evo_traj tum --ref=./groundtruth.tum ./estimate_result.txt -a -p -v 
# evo_traj tum --ref=./groundtruth.tum ./pose_output_source_result.txt ./pose_output_first_result.txt ./estimate_result.txt -a -p -v 