#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
import time
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family'] = 'sans-serif'
in_path = r'E:/BC/data/G/'
out_path = r'templates/'
a = pd.read_excel(in_path + 'A_temp.xlsx', index_col=0, enconding='gbk')

g = pd.read_excel(in_path + 'G_temp.xlsx', index_col=0, encoding='gbk')
g = g['2000':]
a = a['2005':]
style = {'size': 18, 'color': 'indigo'}
g2 = g.loc['2003':, '全球温度']
a2 = a.loc['2008':, '中证温度']
# fig = plt.figure("fig01", figsize=[6, 4], dpi=300, constrained_layout=False)
# fig, ax = plt.subplots()
# ax.plot(d.index, d['估值温度'], label='估值温度')

# ax0 = ax.twinx()
# ax0.plot(d.index, d['中证全指价格指数'], 'r', label='中证全指价格指数')
# ax.legend()
# ax0.legend()
# d.legend(['估值温度'], ['中证全指价格指数'], borderaxespad=0.)
fig, ax = plt.subplots()
plt.figure(1, figsize=(2000, 1010))
ax.plot(g.index, g['全球温度'], 'steelblue', label='全球温度')
plt.grid(ls='--')
# plt.annotate('%f' % g['temp'][-1], (g.index[-1], g['temp'][-1]))
# plt.annotate('%.2f' % g2.max(), (g2.idxmax(), g2.max()), xytext=(-200, 5), textcoords='offset points'
plt.text(g.index[-1], g['全球温度'][-1], '%.2f' % g['全球温度'][-1], fontdict=style)
plt.annotate('%.2f' % g2.max(), (g2.idxmax(), g2.max()), xytext=(g2.idxmax(), g2.max() * 1.01 + 2),
             bbox=dict(boxstyle='round,pad=0.4', fc='red', ec='k', lw=1, alpha=0.8))
plt.annotate('%.2f' % (g2.min()), (g2.idxmin(), g2.min()), xytext=(g2.idxmin(), g2.min() * 0.9 - 3),
             bbox=dict(boxstyle='round,pad=0.4', fc='blue', ec='k', lw=1, alpha=0.2))
plt.title(str(g.index[-1].month)+'月'+str(g.index[-1].day)+'日全球温度计', fontsize=24)


# plt.text(g2.idxmax(), g2.max(), g2.max(), fontdict=style)
ax0 = ax.twinx()
ax0.plot(g.index, g['全球价格'], 'dimgray', label='加权资产净值')
fig.legend()
ax.set_xlabel('时间', size=18)
ax.set_ylabel('温度', size=18)
ax0.set_ylabel('价格', size=18)
# ax.set_yticks(np.arange(0, 110, 20))
# ax0.set_yticks(np.arange(0, 6, 1))

plt.savefig('G.png', figsize=(2, 1), dpi=2000)
plt.show()
fig2, ax2 = plt.subplots()
ax2.plot(a.index, a['中证温度'], 'steelblue', label='估值温度')
plt.grid(ls='--')
plt.text(a.index[-1], a['中证温度'][-1], '%.2f' % a['中证温度'][-1], fontdict=style)
plt.annotate('%.2f' % a2.max(), (a2.idxmax(), a2.max()), xytext=(a2.idxmax(), a2.max() * 1.01 + 2),
             bbox=dict(boxstyle='round,pad=0.4', fc='red', ec='k', lw=1, alpha=0.8))
plt.annotate('%.2f' % (a2.min()), (a2.idxmin(), a2.min()), xytext=(a2.idxmin(), a2.min() * 0.9 - 3),
             bbox=dict(boxstyle='round,pad=0.4', fc='blue', ec='k', lw=1, alpha=0.2))
plt.title('A股温度计', fontsize=24)
ax3 = ax2.twinx()
ax3.plot(a.index, a['中证全指'], 'peru', label='中证全指价格指数')
fig2.legend()
ax2.set_xlabel('时间', size=18)
ax2.set_ylabel('温度', size=18)
ax3.set_ylabel('价格', size=18)
plt.savefig('A.png', dpi=2000)
plt.show()
