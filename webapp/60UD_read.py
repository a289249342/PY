#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

day_set = 60
threshold_value = 2
in_path = r'E:/BC/data/60UD/'
d = pd.read_csv(in_path + '002714.csv', index_col=0)
d.index = pd.to_datetime(d.index)
d = d['2022':'2018'][::-1]
p = list(d.iloc[:, 0])

s = []
UD_date = []
for i in range(day_set, len(p)):
    k = len(list(filter(lambda x: x <= p[i], p[i - day_set:i])))
    if k < threshold_value:
        print(d.index[i], p[i])
print(d)
