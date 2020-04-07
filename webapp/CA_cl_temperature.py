#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

in_path = r'E:/BC/data/G/'
total_data = pd.read_excel(in_path + 'cl.xlsx', header=0, encoding='gbk')


def cal(da, axr=0):
    dp = [0]
    count = 0
    result = []
    if 1:
        for k1 in range(len(da)):
            if da[k1] != 0:
                dp.append(da[k1])
            for n1 in range(len(dp)):
                if dp[n1] < da[k1]:
                    count += 1
            if axr == 0:
                result.append(round(count * 100 / len(dp), 5))
            if axr == 1:
                result.append(round(100 - count * 100 / len(dp), 5))
            count = 0
        print(result)
        return result


d = total_data.describe()
d.to_excel(in_path + 'des_cl.xlsx')
time = list(total_data.iloc[:, 0])
p = list(total_data.iloc[:, 1])
wd = cal(list(total_data.iloc[:, 1]))
c = pd.DataFrame([time, p, wd]).T
c.columns = ['时间', '原油价格', '温度']
c['时间'] = c['时间'].dt.date
c.to_csv(in_path + 'T_CL.NYMEX.csv', index=0)
