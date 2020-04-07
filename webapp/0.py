#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from EmQuantAPI import *
from WindPy import w
import pandas as pd
import numpy as np
import datetime
import os
import xlrd
import xlwt

ut_path = r'E:/11.csv'
in_path = r'E:/BC/data/G/'
# w.start()
# k = w.wsd('cl.nym', 'close', '2000-01-01', '2020-03-25', 'TradingCalendar=NYMEX')
t_data = pd.read_excel(in_path + 'T_am.xlsx', enconding='gbk')
c_data = pd.read_excel(in_path + 'amclose.xlsx', header=1, enconding='gbk')
total_data = pd.concat([t_data, c_data.iloc[:, 1:]], axis=1)

for i in range(25, 37):
    for j in range(len(total_data)):
        if total_data.iloc[j, i] == 0:
            print(j, i)
            total_data.iloc[j, i + 12] = 0

total_data['时间'] = total_data['时间'].dt.date
total_data.to_csv(in_path + 'total_am.csv', index=0)
