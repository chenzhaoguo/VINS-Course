#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

evo_traj tum --ref=./groundtruth_MH_01.tum ./estimate_result.txt -a -p -v
