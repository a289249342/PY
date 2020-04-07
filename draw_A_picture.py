#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
in_path = r'E:/BC/data/G/'
out_path=r'E:/BC/data/'
data = pd.read_excel(in_path + 'T_windQA.xls', index_col=0, enconding='gbk')
draw_data = data.loc['2005-01-01':, ['中证温度28', '中证全指价格指数']]
draw_data.rename(columns={'中证温度28': '估值温度'}, inplace=1)
print(draw_data)
d=draw_data.plot(secondary_y=['估值温度'])
d.get_figure().savefig(in_path+'temp.png')
plt.show()
