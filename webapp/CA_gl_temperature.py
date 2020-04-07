#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from EmQuantAPI import *
import pandas as pd
import numpy as np
import datetime
import os
import xlrd
import xlwt

in_path = r'E:/BC/data/G/'
code = 'Wind_000002.SH'
total_data = pd.read_csv(in_path + code + '.csv')
print(total_data)


def cal(da, axr=0):
    dp = []
    count = 0
    result = []
    if 1:
        for k1 in range(len(da)):
            dp.append(da[k1])
            for n1 in range(len(dp)):
                if dp[n1] < da[k1]:
                    count += 1
            if axr == 0:
                result.insert(0, round(count * 100 / len(dp), 5))
            if axr == 1:
                result.insert(0, round(100 - count * 100 / len(dp), 5))
            count = 0
        return result[::-1]


d1 = list(total_data.iloc[:, 0])
e1 = list(total_data.iloc[:, 1])
e2 = list(total_data.iloc[:, 2])
b1 = list(total_data.iloc[:, 3])
b2 = list(total_data.iloc[:, 4])
ce1 = cal(e1)
ce2 = cal(e2)
cb1 = cal(b1)
cb2 = cal(b2)
t_gl = [d1]
t_gl.append(ce1)
t_gl.append(ce2)
t_gl.append(cb1)
t_gl.append(cb1)
t_gl = pd.DataFrame(t_gl).T
print(t_gl)
t_gl.to_csv(in_path + 'T_' + code + '.csv', index=0)
