#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import datetime
import os
import xlrd
import xlwt
import pandas as pd
import numpy as np

in_path = r'E:/BC/data/G/'
code = '000001.SH'
ta_data = pd.read_excel(in_path + 'windQA.xlsx', header=1, enconding='gbk')


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


time = list(ta_data.iloc[:, 0])
pb1 = cal(list(ta_data.iloc[:, 1]))
pb2 = cal(list(ta_data.iloc[:, 2]))
pb3 = cal(list(ta_data.iloc[:, 3]))
pe1 = cal(list(ta_data.iloc[:, 4]))
pe2 = cal(list(ta_data.iloc[:, 5]))
pe3 = cal(list(ta_data.iloc[:, 6]))
cl1 = list(ta_data.iloc[:, 7])
cl2 = list(ta_data.iloc[:, 8])
cl3 = list(ta_data.iloc[:, 9])
g = [time, pb1, pe1, pb2, pe2, pb3, pe3, cl1, cl2, cl3]
ga = pd.DataFrame(g).T

print(ga)
ga.columns = ['时间', '中证全指pb', '中证全指pe', '万得全A去金融两油pb', '万得全A去金融两油pe', '万得全Apb', '万得全Ape',
              '中证全指价格指数', '全A去金融两油价格', '全A价格指数']
ga['中证温度21'] = ga.apply(lambda x: (2 * x[1] + x[2]) / 3, axis=1)
ga['中证温度28'] = ga.apply(lambda x: (4 * x[1] + x[2]) / 5, axis=1)
ga['全A双去温度21'] = ga.apply(lambda x: (2 * x[3] + x[4]) / 3, axis=1)
ga['全A双去温度28'] = ga.apply(lambda x: (4 * x[3] + x[4]) / 5, axis=1)
ga['全A温度21'] = ga.apply(lambda x: (2 * x[5] + x[6]) / 3, axis=1)
ga['全A温度28'] = ga.apply(lambda x: (4 * x[5] + x[6]) / 5, axis=1)
ga['时间'] = ga['时间'].dt.date
ga.to_excel(in_path + 'T_windQA.xls', index=0)
# total_data = pd.DataFrame(total_data)
# total_data.pop('市盈率')
# total_data.loc[:, '市净率'] = total_data.apply(lambda x: x[4] * x[10] / 100, axis=1)
# # print(total_data)
#
# new_data = (total_data.apply(lambda x: x * x[4] / x[0], axis=1)).iloc[:, 4:]
# total_data[['调和转股价值', '调和转股市净率', '调和转股市盈率', '调和转股溢价率', '调和伪价市净率', '调和伪价市盈率', '调和市净率']] = new_data
# total_data[['1', '2', '3', '4', '5', '6', '7']] = total_data.apply(lambda x: x * x[4] / x[0], axis=1).iloc[:, -7:]
#
# t1 = total_data.groupby('日期').mean()
# t1.to_csv(in_path + 'th_t1.csv', header=0, index=1)
# # t1 = total_data.groupby('日期').mean()
# # t2 = total_data.groupby('日期').median()
# # t1.to_csv(in_path + 't1.csv', header=0)
# # t2.to_csv(in_path + 't2.csv', header=0)
