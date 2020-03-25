#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

evo_traj tum --ref=./groundtruth_tum.txt ./estimate_has_prior.txt ./estimate_no_prior.txt -a -p -v