#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from EmQuantAPI import *
import pandas as pd
import numpy as np
import datetime
import os
import xlrd
import xlwt

in_path = r'E:/BC/data/G/'


def t(t_data):
    td = []
    for t1 in t_data:
        for t2 in t1:
            td.append(t2)
    return td


code = "000002.SH"
# 000001.SH,399001.SZ,DJIA.GI,FCHI.GI,FTSE.GI,GDAXI.GI,HSI.HI,IXIC.GI,KS11.GI,N225.GI,RTS.GI,SENSEX.GI,SPX.GI
c.start()
gl = []
d = c.tradedates("1994-09-29", "2020-03-22").Data
print(d)
for i in d:
    gl1 = [i]
    value = c.csd(
        code,
        "PEMIDTTM,PEMIDLYR,PBMIDMRQ,PBMIDLYR", i, i,
        "DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=CNSESH").Data
    print(i, value[code])
    gl1.extend(t(value[code]))
    gl.append(gl1)
print(gl)
c.stop()
g = pd.DataFrame(gl)
g.columns = ['date', 'pe1', 'pe2', 'pb1', 'pb2']
g.to_csv(in_path + code + '.csv', index=0)
