#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import datetime
import os
import xlrd
import xlwt
import pandas as pd
import numpy as np

in_path = r'E:/BC/data/na_data/'
total_data = pd.read_csv(in_path + '000tht1_temperature.csv', header=None, index_col=0)

money_data = total_data.iloc[0:1007, -7:]
money_data['27'] = total_data.iloc[0:1007, 2]
# print(money_data)
p = list(total_data.iloc[0:2000, 0][::-1])
# print(p)
m = list(total_data.iloc[0:2000, -7])[::-1]


# p=[0.5,1,0.5,1]
def ca_m(t):
    cash = 1
    f = 0
    s = 1
    for i in range(len(t)):
        if 1:
            print(t[i], p[i])
            s = cash + f * p[i]
            cash = s * t[i] / 100
            f = s * (100 - t[i]) / 100 / p[i]

            print(cash, f, s)
    print("s=", s / p[-1] * p[0], p[-1] / p[0])


# 0.47961071 35.70067
# 0.47389552
ca_m(m)
