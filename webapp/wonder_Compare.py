#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

in_path = r'E:/BC/data/wonder/'
new_stock = pd.read_csv(in_path + '4.csv')
old_stock = pd.read_csv(in_path + '3.csv')
new_add, old_drop = [], []
new_list = list(new_stock.iloc[:-1, 2])
old_list = list(old_stock.iloc[:-1, 2])
if old_stock.iloc[-2, 2] not in list(new_stock.iloc[:-1, 2]):
    print('111')
for i_new in new_stock.iloc[:-1, 2]:
    if i_new not in old_list:
        new_add.append(i_new)
for i_old in old_stock.iloc[:-1, 2]:
    if i_old not in new_list:
        old_drop.append(i_old)
print('调入', new_add)
print('调出', old_drop)
