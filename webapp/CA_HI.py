#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ARASHI'

import xlrd
import datetime
from scipy import optimize
import numpy as np
import pandas as pd

in_path = r'E:/BC/data/na_data/'

over_book = xlrd.open_workbook(in_path + 'Lday.xlsx')
over_sheet = over_book.sheet_by_index(0)
over = []
for k in range(1, over_sheet.nrows):
    line = over_sheet.row_values(k)
    if line[11] == '':
        line[11] = line[13]
    if line[11] < line[13]:
        line[11] = line[13]
    over.append([line[1], line[11], line[5]])
#  代码 最后交易日 期限（年）
Lil_book = xlrd.open_workbook(in_path + 'Lilv.xlsx')
# 读取利率条款
Lil_sheet = Lil_book.sheet_by_index(0)
lil = []
for i in range(Lil_sheet.nrows):
    line = Lil_sheet.row_values(i)
    lil.append([line[1], line[3], line[4], line[5], line[6], line[7], line[8], line[10]])


#  代码 一到六年利率 赎回价

def xnpv(rate, cashflows):
    return sum([cf / (1 + rate) ** ((t - cashflows[0][0]).days / 365.0) for (t, cf) in cashflows])


def xirr(cashflows, guess=0.1):
    try:
        return optimize.newton(lambda r: xnpv(r, cashflows), guess)
    except:
        print(cashflows)
        print('Calc Wrong')


def xir(cashflows):
    years = [(ta[0] - cashflows[0][0]).days / 365. for ta in cashflows]
    residual = 0.8
    step = 0.05
    guess = 0.1
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i_c, trans in enumerate(cashflows):
            residual += trans[1] / pow(guess, years[i_c])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess - 1


def c_date(date_day):
    delta = datetime.timedelta(days=date_day)
    m_date = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta
    # return m_date.strftime('%Y-%m-%d')
    return m_date


def c_last_y(date_y, times):
    date_new = datetime.datetime(date_y.year - times, date_y.month, date_y.day)
    return date_new


def ca_dd100(lil_01, time, p, vol, add_data):
    # 利率、到期时间等条款，日期，收盘价，成交量
    rate = 1  # 1为税前收益率 0.8为税后收益率
    p_data = []
    time.pop(0)
    p.pop(0)
    vol.pop(0)
    while p[0] == 100:
        time.pop(0)
        p.pop(0)
        vol.pop(0)
    if lil_01[7] == 0:  # 计算赎回价格
        if lil_01[6] == 0:
            if lil_01[5] == 0:
                if lil_01[4] == 0:
                    lil_01[7] = 100 + lil_01[3]
                lil_01[7] = 100 + lil_01[4]
            lil_01[7] = 100 + lil_01[5]
        lil_01[7] = 100 + lil_01[6]
    for i1 in range(len(p)):
        if p[i1] != add_data[i1][0]:
            print(time[i1], p[i1], add_data[i1][0])
            with open(in_path + 'log_error.txt', mode='a') as f:
                f.writelines(str(time[i1]) + ' ' + str(p[i1]) + ' ' + str(add_data[i1][0]) + '\n')
        p_line_data = []
        if vol[i1] == 0:
            continue
        data = [(datetime.datetime.strptime(time[i1], '%Y-%m-%d'), -1 * p[i1])]
        last_day = c_date(lil_01[-1])
        if lil_01[-2] == 6:
            if c_last_y(last_day, 5) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 5), lil_01[1] * rate))
            if c_last_y(last_day, 4) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 4), lil_01[2] * rate))
            if c_last_y(last_day, 3) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 3), lil_01[3] * rate))
            if c_last_y(last_day, 2) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 2), lil_01[4] * rate))
            if c_last_y(last_day, 1) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 1), lil_01[5] * rate))
        elif lil_01[-2] == 5:
            if c_last_y(last_day, 4) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 4), lil_01[1] * rate))
            if c_last_y(last_day, 3) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 3), lil_01[2] * rate))
            if c_last_y(last_day, 2) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 2), lil_01[3] * rate))
            if c_last_y(last_day, 1) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 1), lil_01[4] * rate))
        elif lil_01[-2] == 4:
            if c_last_y(last_day, 3) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 4), lil_01[1] * rate))
            if c_last_y(last_day, 2) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 3), lil_01[2] * rate))
            if c_last_y(last_day, 1) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 2), lil_01[3] * rate))
        elif lil_01[-2] == 3:
            if c_last_y(last_day, 2) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 4), lil_01[1] * rate))
            if c_last_y(last_day, 1) > datetime.datetime.strptime(time[i1], '%Y-%m-%d'):
                data.append((c_last_y(c_date(lil_01[-1]), 3), lil_01[2] * rate))
        data.append((c_date(lil_01[-1]), 100 + (lil_01[7] - 100) * rate))
        # print(data)
        # p_data.insert(0, xir(data))
        p_line_data.append(time[i1])
        p_line_data.append(p[i1])
        p_line_data.append(xir(data))
        p_line_data.extend(add_data[i1])
        p_data.append(p_line_data)
    # for i7 in range(len(p_data)):
    #     print(p_data[i7])
    return p_data


log_txt = []
total_data = []
with open(in_path + 'log.txt') as I_File:
    for i in I_File:
        log_txt.append(i.strip('\n'))
# log_txt = ['128094.SZ', '110031.SH']
for path in log_txt:
    add = []
    lil_00 = []
    workbook = xlrd.open_workbook(in_path + 'na_' + path + '.xls')
    names = workbook.sheet_names()
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    ncols = worksheet.ncols
    # for i1 in range(nrows):
    #     print(worksheet.row_values(i1))
    for i in range(len(lil)):  # 匹配转债代码并将条款传入lil_00
        if lil[i][0] == worksheet.col_values(0)[1]:
            lil_00 = lil[i]
            break
    for i in range(len(lil)):
        if over[i][0] == worksheet.col_values(0)[1]:  # 匹配后传入期限和最后交易日
            lil_00.append(over[i][2])
            lil_00.append(over[i][1])
    for i in range(1, nrows):
        adi = []
        for i0 in range(9, ncols):
            adi.append(worksheet.col_values(i0)[i])
        add.append(adi)
    day_data = ca_dd100(lil_00, worksheet.col_values(2), worksheet.col_values(6), worksheet.col_values(7), add)
    # 利率条款 日期 收盘价 成交量
    total_data.extend(day_data)
# save_data = []
# p_dic = {}
# r_dic = {}
# print(total_data)
# for total_t in total_data:
#     for total_i in total_t:
#         if total_i[0] in p_dic:
#             p_dic[total_i[0]].append(total_i[1])
#             r_dic[total_i[0]].append(total_i[2])
#         else:
#
#             p_dic[total_i[0]] = [total_i[1]]
#             r_dic[total_i[0]] = [total_i[2]]
#         save_data.append(total_i)
# s = np.array(total_data)
# np.savetxt(in_path + 'total.gz', s)
s = pd.DataFrame(total_data)
s.to_csv(in_path + 'all_data.csv', header=0, index=0)
out_path = r'E:/11.csv'
in_path = r'E:/BC/data/na_data/'
name = '日期', '价格', '收益率', 'choice价格', '转股价', '转股价值', '转股市净率', '转股市盈率', '转股溢价率', '伪价市净率', '伪价市盈率', '市净率', '市盈率'
total_data = pd.read_csv(in_path + 'all_data.csv', names=name)
total_data = pd.DataFrame(total_data)
total_data.loc[:, '市净率'] = total_data.apply(lambda x: x[5] * x[11] / 100, axis=1)
# print(total_data)
t1 = total_data.groupby('日期').mean()
t2 = total_data.groupby('日期').median()
t1.to_csv(in_path + 't1.csv', header=0)
t2.to_csv(in_path + 't2.csv', header=0)
