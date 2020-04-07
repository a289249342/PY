#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from WindPy import w
import numpy as np

from collections import Iterable
import xlrd
import datetime
from scipy import optimize
from EmQuantAPI import *

import time
import datetime


def t_msg():
    d = []
    f_rate = -1 * 0.5
    z_rate = 0.5
    data = c.csqsnapshot("002271.SZ,128016.SZ", "BuyPrice1,SellPrice1", "Ispandas=0")
    if not isinstance(data, c.EmQuantData):
        print(data)
    else:
        if data.ErrorCode != 0:
            print("request csqsnapshot Error, ", data.ErrorMsg)
        else:
            for key, value in data.Data.items():
                d.append(value[0])
                d.append(value[1])
    yhb1 = d[0]
    yhs1 = d[1]
    zzb1 = d[2]
    zzs1 = d[3]
    fu = (zzs1 - yhb1 * 100 / 22.4) / (yhb1 * 100 / 22.4) * 100
    ze = (zzb1 - yhs1 * 100 / 22.4) / (yhs1 * 100 / 22.4) * 100
    if fu < f_rate:
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(fu, "卖出正股，买入转债")

    elif ze > z_rate:
        print('----------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------')
        print(ze, "卖出转债，买入正股")
    else:
        print(fu, ze)
    time.sleep(3)
    # for key, value in data.Data.items():
    #     print(key, ">>> ", end="")
    #     for v in value:
    #         print(v, " ", end="")
    #     print()


c.start()
while 1:
    t_msg()

c.stop()
