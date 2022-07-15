#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd

in_path = r'E:/BC/data/'
limit = []


def pe_pb(identifier):  # str
    limit_pe = pd.read_csv(in_path + identifier + '_pe.csv', index_col=0)
    point = limit_pe.iloc[0, 0]

    def lim_map(x):
        return int(x * point)

    limit_pe = limit_pe.iloc[:-1, 4][::-1]
    limit_pe.index = pd.to_datetime(limit_pe.index)
    limit_pb = pd.read_csv(in_path + identifier + '_pb.csv', index_col=0)
    limit_pb = limit_pb.iloc[:-1, 4][::-1]
    limit_pb.index = pd.to_datetime(limit_pb.index)
    point_pe = limit_pe.iloc[-1]
    point_pb = limit_pb.iloc[-1]
    print(identifier, point, point_pe, point_pb, limit_pe['2019':].max(), limit_pe['2018':].min(),
          limit_pb['2019':].max(), limit_pb['2018':].min())
    limit_high_pe = limit_pe['2019':].max() / point_pe
    limit_low_pe = limit_pe['2018':].min() / point_pe
    limit_high_pb = limit_pb['2019':].max() / point_pb
    limit_low_pb = limit_pb['2018':].min() / point_pb
    limit.append(
        [identifier, lim_map(limit_high_pe), lim_map(limit_high_pb), lim_map(limit_low_pe), lim_map(limit_low_pb),
         round(limit_high_pe / limit_high_pb, 3)])


pe_pb('Hu50')
pe_pb('Hs300')
pe_pb('Zz500')
pe_pb('Zz1000')
pe_pb('Gz2000')
for l in range(len(limit)):
    print(limit[l])
