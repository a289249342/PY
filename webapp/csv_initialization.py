#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

in_path = r'E:/BC/data/SBsb/'
hs300 = pd.read_csv(in_path + '000300.csv', index_col=0)
sz50 = pd.read_csv(in_path + '000016.csv', index_col=0)
zz500 = pd.read_csv(in_path + '000905.csv', index_col=0)
year10 = pd.read_csv(in_path + 'year10.csv', index_col=0)
hs300.index = pd.DatetimeIndex(hs300.index)
sz50.index = pd.DatetimeIndex(sz50.index)
zz500.index = pd.DatetimeIndex(zz500.index)
year10.index = pd.DatetimeIndex(year10.index)
total = pd.merge(year10, sz50, on='时间', how='outer')
total = pd.merge(total, hs300, on='时间', how='outer')
total = pd.merge(total, zz500, on='时间', how='outer')
new = total.iloc[:, [3, 8, 17, 26, 27]]
new.columns = ['y_10', 'pe_50', 'pe_300', 'pb_500', 'pre_500']
new.index.name = 'time'
new.to_csv(in_path + 'SYB.csv')
