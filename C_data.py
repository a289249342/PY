#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import tushare as ts

# ds = ts.get_hist_data('600703',start='2020-02-18')
ds = ts.get_today_all()
#ds.to_csv('E:/BC/data/00.csv', columns=['changepercent'])
# print(ds)
# ds.to_excel('E:/BC/data/0022.xlsx')
