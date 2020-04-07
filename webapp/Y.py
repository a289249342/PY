#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import datetime
import os
import xlrd
import xlwt
import pandas as pd
import numpy as np


out_path = r'E:/11.csv'
in_path = r'E:/BC/data/Y/'
name = '日期', '价格', '收益率', 'choice价格', '转股价', '转股价值', '转股市净率', '转股市盈率', '转股溢价率', '伪价市净率', '伪价市盈率', '市净率', '市盈率'
total_data = pd.read_csv(in_path + 'c.csv', header=0)

d = {}
d1 = {}
d2 = {}
d3 = {}
d4 = {}
d5 = {}
d6 = {}
d7 = {}
d8 = {}


def px(p):
    pd = []
    data = []
    for pp in p:
        pd = [pp[0], '', '', '', '', '', '', '', '']
        for ppp in range(len(pp)):

            if pp[ppp] == 'NYMEX原油':
                pd[1] = pp[ppp + 1]
            if pp[ppp] == '嘉实原油':
                pd[2] = pp[ppp + 1]
            if pp[ppp] == '南方原油A':
                pd[3] = pp[ppp + 1]
            if pp[ppp] == '广发道琼斯美国石油A人民币':
                pd[4] = pp[ppp + 1]
            if pp[ppp] == '原油基金':
                pd[5] = pp[ppp + 1]
            if pp[ppp] == '华宝标普油气A人民币':
                pd[6] = pp[ppp + 1]
            if pp[ppp] == '华安标普全球石油':
                pd[7] = pp[ppp + 1]
            if pp[ppp] == '国泰大宗商品':
                pd[8] = pp[ppp + 1]
        data.append(pd)
    return data


def add(ii, dic):
    if ii[1] in dic:
        dic[ii[1]].append(ii[0])
        dic[ii[1]].append(ii[2])
    else:
        dic[ii[1]] = [ii[0]]
        dic[ii[1]].append(ii[2])


for i in range(len(total_data)):
    i1 = list(total_data.iloc[i, 1:4])
    i2 = list(total_data.iloc[i, 5:8])
    i3 = list(total_data.iloc[i, 9:12])
    i4 = list(total_data.iloc[i, 13:16])
    i5 = list(total_data.iloc[i, 17:20])
    i6 = list(total_data.iloc[i, 21:24])
    i7 = list(total_data.iloc[i, 25:28])
    i8 = list(total_data.iloc[i, 29:32])
    add(i1, d)
    add(i2, d)
    add(i3, d)
    add(i4, d)
    add(i5, d)
    add(i6, d)
    add(i7, d)
    add(i8, d)

s1 = []
s2 = []
s3 = []
for q in d:
    s1 = [q]
    s1.extend(d[q])
    s2.append(s1)

for l in s2:
    if len(l) == 17:
        s3.append(l)

s0 = []
s0.append(s3[0][2])
print(s3[32])
s4 = px(s3)
s4 = pd.DataFrame(s4)
s4.to_csv(in_path + 's3.csv', header=0, index=0)