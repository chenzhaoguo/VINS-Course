#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

rm -rf *.zip

evo_rpe tum ./groundtruth_tum.txt ./estimate_has_prior.txt -a --save_results ./estimate_has_prior.zip
evo_rpe tum ./groundtruth_tum.txt ./estimate_no_prior.txt -a --save_results ./estimate_no_prior.zip
evo_res ./*.zip -p
