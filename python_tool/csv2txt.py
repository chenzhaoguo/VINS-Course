# -*- coding: utf-8 -*-

import os
import pandas as pd

filepath_csv = os.path.abspath('../euroc_data/mav0/imu0/')  # source file: .csv
data = pd.read_csv(filepath_csv + 'data.csv', encoding='utf-8', skiprows=1, header=None)
# print data

filepath_txt = os.path.abspath('./')  # result file: .txt
with open(filepath_txt + 'imu.txt', 'a+') as f:
    for line in data.values:
        f.write(str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) + ' ' + str(line[3]) + ' ' + str(line[4]) + ' ' + str(line[5]) + ' ' + str(line[6]) + '\n')
