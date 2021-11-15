#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from WindPy import *
import numpy as np
import pandas as pd
import datetime
import time
import requests
import webbrowser
import random

in_path = r'E:/BC/data/G/'
# G：global 全球温度计  A ：A股温度计
data = pd.read_excel(in_path + '53.xlsx', header=0, index_col=0, encoding='gbk')

D = data.describe([.1, .2, .3, .4, .5, .6, .7, .8, .9])

Z = data.iloc[:, 0]
H = data.iloc[:, 7]


def test_cp():
    s = []
    for k in range(140,260,5):

        for i in range(10000):
            r = random.randint(0, 1791 - k)
            z = Z[r + k] / Z[r]
            h = H[r + k] / H[r]
            s.append([z, h, z - h])
        S = pd.DataFrame(s)
        sss = S.sort_values(by=2)
        sf = sss[(sss.iloc[:, 0] < 1) & (sss.iloc[:, 1] < 1)]
        if len(sf)>0:
            print(sf.iloc[0,2])


test_cp()
# in_path = r'E:/BC/data/300500/202008/'
# c = 0
# c1 = 0
# c2 = 0
# t = 6246.6 * 200 * 0.85
# for k in os.listdir(in_path):
#     data = pd.read_csv(in_path + k, header=0, index_col=0, encoding='gbk')
#
#     a1 = data.loc['IC2103                        ', '今结算']
#     a2 = data.loc['IO2103-P-4700                 ', '今结算']
#     a3 = data.loc['IO2106-P-4700                 ', '今结算']
#     c = 200 * a1 + 100 * (a2 + a3) - t - 276818
#     c1 = 200 * a1 + 300 * a2 - t - 310038
#     c2 = 200 * a1 + 300 * a3 - t - 333018
#     c4 = 200 * a1 - t - 187398
#     print(k, a1, a2, a3, '***', c, c1, c2, c4, '|||', a1 * 0.15 * 200)
