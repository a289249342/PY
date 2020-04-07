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

out_path = r'E:/11.csv'
in_path = r'E:/BC/data/G/'

ta_data = pd.read_excel(in_path + 'windQA.xlsx', header=1, enconding='gbk')
total_data = pd.read_excel(in_path + 'am325.xlsx', header=1, encoding='gbk')


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
ga['中证温度'] = ga.apply(lambda x: (2 * x[1] + x[2]) / 3, axis=1)
ga['全A双去温度'] = ga.apply(lambda x: (2 * x[3] + x[4]) / 3, axis=1)
ga['全A温度'] = ga.apply(lambda x: (2 * x[5] + x[6]) / 3, axis=1)
ga['时间'] = ga['时间'].dt.date
ga.to_csv(in_path + 'T_windQA.csv', index=0)

# t = total_data != 0
# t = total_data[t]
# total_data = total_data.loc['2283':, :]
print(total_data)
t1 = cal(list(total_data['道琼斯工业指数']))
t2 = cal(list(total_data['道琼斯工业指数.1']))
t3 = cal(list(total_data['纳斯达克指数']))
t4 = cal(list(total_data['纳斯达克指数.1']))
t5 = cal(list(total_data['标普500']))
t6 = cal(list(total_data['标普500.1']))
t7 = cal(list(total_data['富时100']))
t8 = cal(list(total_data['富时100.1']))
t9 = cal(list(total_data['法国CAC40']))
t10 = cal(list(total_data['法国CAC40.1']))
t11 = cal(list(total_data['德国DAX']))
t12 = cal(list(total_data['德国DAX.1']))
t13 = cal(list(total_data['日经225']))
t14 = cal(list(total_data['日经225.1']))
t15 = cal(list(total_data['韩国综合指数']))
t16 = cal(list(total_data['韩国综合指数.1']))
t17 = cal(list(total_data['恒生指数']))
t18 = cal(list(total_data['恒生指数.1']))
t19 = cal(list(total_data['澳洲标普200']))
t20 = cal(list(total_data['澳洲标普200.1']))
t21 = cal(list(total_data['孟买SENSEX30']))
t22 = cal(list(total_data['孟买SENSEX30.1']))
t23 = cal(list(total_data['俄罗斯RTS']))
t24 = cal(list(total_data['俄罗斯RTS.1']))
gl = [list(total_data['时间']), t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20,
      t21, t22, t23, t24]

gl = pd.DataFrame(gl).T
gl.columns = [
    '时间', '道琼斯工业指数pb', '道琼斯工业指数pe', '纳斯达克指数pb', '纳斯达克指数pe', '标普500pb', '标普500pe', '富时100pb',
    '富时100pe', '法国CAC40pb', '法国CAC40pe', '德国DAXpb', '德国DAXpe', '日经225pb', '日经225pe', '韩国综合指数pb',
    '韩国综合指数pe', '恒生指数pb', '恒生指数pe', '澳洲标普200pb', '澳洲标普200pe', '孟买SENSEX30pb', '孟买SENSEX30pe',
    '俄罗斯RTSpb', '俄罗斯RTSpe']
gl['道琼斯工业指数温度'] = gl.apply(lambda x: (2 * x[1] + x[2]) / 3, axis=1)
gl['纳斯达克指数温度'] = gl.apply(lambda x: (2 * x[3] + x[4]) / 3, axis=1)
gl['标普500温度'] = gl.apply(lambda x: (2 * x[5] + x[6]) / 3, axis=1)
gl['富时100温度'] = gl.apply(lambda x: (2 * x[7] + x[8]) / 3, axis=1)
gl['法国CAC40温度'] = gl.apply(lambda x: (2 * x[9] + x[10]) / 3, axis=1)
gl['德国DAX温度'] = gl.apply(lambda x: (2 * x[11] + x[12]) / 3, axis=1)
gl['日经225温度'] = gl.apply(lambda x: (2 * x[13] + x[14]) / 3, axis=1)
gl['韩国综合指数温度'] = gl.apply(lambda x: (2 * x[15] + x[16]) / 3, axis=1)
gl['恒生指数温度'] = gl.apply(lambda x: (2 * x[17] + x[18]) / 3, axis=1)
gl['澳洲标普200温度'] = gl.apply(lambda x: (2 * x[19] + x[20]) / 3, axis=1)
gl['孟买SENSEX30温度'] = gl.apply(lambda x: (2 * x[21] + x[22]) / 3, axis=1)
gl['俄罗斯RTS温度'] = gl.apply(lambda x: (2 * x[23] + x[24]) / 3, axis=1)
gl['时间'] = gl['时间'].dt.date
print(gl)
gl.to_excel(in_path + 'T_am.xlsx', index=0)
