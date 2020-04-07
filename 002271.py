#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

in_path = r'E:/BC/data/da/'
total_data = pd.read_excel(in_path + '271.xls', header=0, encoding='gbk')
t = total_data.iloc[:, 4:6]


# t = total_data.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])

def test(p=30, percent=1):
    p1 = p
    p2 = p * (1 + percent / 100)
    count = 0
    k = 0
    tag = 0
    time = 0
    for i in range(len(t)):
        low = t.iloc[i, 1]
        high = t.iloc[i, 0]
        if low <= p1 and k == 0:
            k = 1
            tag = p1
            # print('buy', p1)
        if high >= p2 and k == 1:
            k = 0
            count += (p2 - tag) / tag - 0.002
            time += 1
            # print('sell', p2)
    # print(count * 100, p, percent, time)
    # return [count * 100, p, percent, time]
    return count * 100


def per(p):
    st = [p, 28.91, 30.61, 31.41, 31.727, 32.2, 32.62, 32.87, 33.12, 33.37, 33.81]
    st = pd.DataFrame(st)
    sz = st.iloc[:, 0].size - 1
    st['new'] = st.iloc[:, 0].rank(method='max').apply(lambda x: 100.0 * (x - 1) / sz)
    return 1 - st.iloc[0, 1] / 100.0


t_YH = []
a = list(map(lambda x: x / 20.0, range(600, 670)))
b = list(map(lambda x: x / 10.0, range(10, 61)))

for b0 in b:
    yh = []
    for a0 in a:
        yh.append(test(a0, b0))
    t_YH.append(yh)
t = pd.DataFrame(t_YH)
print(t)
D = t[t != 0].describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
name = 'YH3410.xls'

D.to_excel(in_path + 'des1_' + name)
D = D.T
D.to_excel(in_path + 'des2_' + name)
t.to_excel(in_path + name)
