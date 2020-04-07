#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import numpy as np

out_path = r'E:/11.csv'
in_path = r'E:/BC/data/na_data/'
name = '日期', '价格', '收益率', 'choice价格', '转股价', '转股价值', '转股市净率', '转股市盈率', '转股溢价率', '伪价市净率', '伪价市盈率', '价值市净率', '价值市盈率'


# total_data = pd.read_csv(in_path + 't1.csv', names=name)
# total_data = pd.read_csv(in_path + 'th_t1.csv', index_col=0,header=1)


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
        return result


def get_temperature(t):
    # day_temperature.append(list(total_data.iloc[:, 0])[::-1])
    # day_temperature.append(list(total_data.iloc[:, 1])[::-1])
    for i in t.columns:
        k = list(total_data.loc[:, i])
        if i == 2:
            day_temperature.append(cal(k, axr=1))
        else:
            day_temperature.append(cal(k))


# col = []
# # col = ['date', 'price']
# for i0 in name[1:12]:
#     col.append(i0)
# for i0 in name[1:12]:
#     col.append(i0)
day_temperature = []
total_data = pd.read_csv(in_path + 'th_t1.csv', index_col=0, header=None)

get_temperature(total_data)
day_temperature = pd.DataFrame(day_temperature)
day_temperature = day_temperature.T
# col = pd.DataFrame(col).T
# day_temperature = pd.concat([col, day_temperature])
print(day_temperature)
day_temperature.to_csv(in_path + 'tht1_temperature.csv', header=0, index=1)

# p_dic = {}
# r_dic = {}
#
# for total_i in total_data:
#     if total_i[0] in p_dic:
#         p_dic[total_i[0]].append(total_i[1])
#         r_dic[total_i[0]].append(total_i[2])
#     else:
#         p_dic[total_i[0]] = [total_i[1]]
#         r_dic[total_i[0]] = [total_i[2]]
#
#
# # print(p_dic)
# # print(r_dic)
# def avg(dic):
#     avg_dic = {}
#
#     for a in dic:
#         su = 0
#         for b in dic[a]:
#             su += b
#         avg_dic[a] = su / len(dic[a])
#     return avg_dic
#
#
# def avg_20(dic):
#     avg_dic = {}
#
#     for a in dic:
#         su = 0
#         if len(dic[a]) > 20:
#             dic[a] = list(sorted(dic[a]))
#             dic[a].pop(0)
#             dic[a].pop(-1)
#         for b in dic[a]:
#             su += b
#         avg_dic[a] = su / len(dic[a])
#     # p_print(dic)
#     return avg_dic
#
#
# def sum_total(dic):
#     sum_dic = {}
#
#     for a in dic:
#         sum_dic[a] = len(dic[a])
#     return sum_dic
#
#
# def p_print(dic):
#     # 倒序输出数据，方便比较
#     o = []
#     ab = []
#     for i in dic:
#         ab.insert(0, [i, dic[i]])
#     ab = list(sorted(ab))
#     for p in ab:
#         o.insert(0, p)
#     for k in o:
#         print(len(k[1]))
#
#
# def list_dic(dic):
#     # 重新排列数据，便于指定区间区分历史集和训练集
#     oo = []
#     ab = []
#     for i in dic:
#         ab.insert(0, [i, dic[i]])
#     ab = list(sorted(ab))
#     for p in ab:
#         oo.append(p[1])
#     return oo
#
#
# p_avg = avg(p_dic)  # 求平均价格
# r_avg = avg(r_dic)
# p_s = sum_total(p_dic)  # 求每日转债个数
# r_s = sum_total(r_dic)
# l_p = list_dic(p_avg)  # 重新排列数据，便于指定区间区分历史集和训练集
# l_r = list_dic(r_avg)
#
# for i2 in range(len(l_p)):
#     print(l_p[len(l_p) - 1 - i2])
# data_price = l_p[-2800:-2000]  # 历史价格
# data_ytm = l_r[-2800:-2000]  # 历史利率
# data1 = l_p[-2000:]  # 训练价格
# data2 = l_r[-2000:]  # 训练利率
#
#
# def cal_p(da, dp):
#     count = 0
#     result = []
#     if 1:
#         for k1 in range(len(da)):
#             for n1 in range(len(dp)):
#                 if dp[n1] < da[k1]:
#                     count += 1
#             result.insert(0, round(count * 100 / len(dp), 5))
#             count = 0
#             dp.append(da[k1])
#         return result
#
#
# def cal_y(db, dy):
#     count = 0
#     result = []
#     if 1:
#         for k2 in range(len(db)):
#             for n2 in range(len(dy)):
#                 if dy[n2] > db[k2]:
#                     count += 1
#             result.insert(0, round(count * 100 / len(dy), 5))
#             count = 0
#             dy.append(db[k2])
#         return result
#
#
# '''D1 = np.array(cal_p(data1, data_price))
# D2 = np.array(cal_y(data2, data_ytm))
# D = np.column_stack((D1, D2))
# np.savetxt('D.csv', D)
# '''
# D1 = cal_p(data1, data_price)
# D2 = cal_y(data2, data_ytm)
# D = ''
#
# for out_index in range(len(data1)):
#     D = D + (str(D1[out_index]) + ',' + str(D2[out_index]) + '\n')
# with open(out_path, 'w') as O_file:
#     O_file.write(D)
