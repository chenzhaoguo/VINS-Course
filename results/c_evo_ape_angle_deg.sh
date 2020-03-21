#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

rm -rf *.zip

evo_ape tum ./groundtruth_MH_02.tum ./estimate_result.txt -a -r angle_deg --save_results ./estimate_result.zip
evo_ape tum ./groundtruth_MH_02.tum ./estimate_result_base.txt -a -r angle_deg --save_results ./estimate_result_base.zip
evo_res ./*.zip -p
