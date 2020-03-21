#########################################################################
# File Name: build.sh
# Author: Mr Chen 
# Created Time: 2019年12月06日 星期五 16时31分41秒
#########################################################################
#!/bin/bash

rm -rf *.zip

evo_rpe tum ./groundtruth_MH_04.tum ./estimate_result.txt -a --save_results ./estimate_result.zip
evo_rpe tum ./groundtruth_MH_04.tum ./estimate_result_base.txt -a --save_results ./estimate_result_base.zip
evo_res ./*.zip -p
