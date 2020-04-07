#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import numpy as np
import datetime
import time
import os
import xlrd
import xlwt
from EmQuantAPI import *

out_path = r'E:/BC/data/na_data/'
in_path = r'E:/BC/data/n_data/'
log_txt = []


def data_up(code, day):
    time.sleep(0.09)
    day = "TradeDate=" + day + ",Type=9"  # Type=9 取滚动市盈率TTM
    data = list(c.css(code, "CBSTOCKPB,CBUNDERLYINGPE", day).Data.values())
    # 市净率 市盈率
    return data[0]


with open(in_path + 'log.txt') as I_File:
    for i in I_File:
        log_txt.append(i.strip('\n'))
# log_txt = ['100001.SH']
c.start()
for path in log_txt:
    #  na_all = []
    workbook = xlrd.open_workbook(in_path + 'n_' + path + '.xls')
    names = workbook.sheet_names()
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    ncols = worksheet.ncols
    na_all = worksheet.row_values(0)
    na_all.append('市净率')
    na_all.append('市盈率')
    na_all = [na_all]
    for ch in worksheet.col_values(2):
        if ch == '':
            print(path)
            break
    for i in range(1, nrows):
        na = worksheet.row_values(i)
        if na[7] == 0:
            continue
        try:
            k = data_up(path, na[2])
            na.append(k[0])
            na.append(k[1])
            na_all.append(na)
        except TypeError as e:
            print(na[2], e, '******************************************************************')
    print(na_all[1])
    new_book = xlwt.Workbook()
    new_sheet = new_book.add_sheet("file")
    for i in range(len(na_all)):
        for j in range(len(na_all[i])):
            new_sheet.write(i, j, na_all[i][j])
    new_book.save(out_path + 'na_' + path + '.xls')
c.stop()
