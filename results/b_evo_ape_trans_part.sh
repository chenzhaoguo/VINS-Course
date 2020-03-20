#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

rm -rf *.zip

evo_ape tum ./groundtruth.tum ./estimate_result.txt -a --save_results ./estimate_result.zip
evo_ape tum ./groundtruth.tum ./pose_output_source_result.txt -a --save_results ./pose_output_source_result.zip
evo_ape tum ./groundtruth.tum ./pose_output_first_result.txt -a --save_results ./pose_output_first_result.zip
evo_res ./*.zip  -p