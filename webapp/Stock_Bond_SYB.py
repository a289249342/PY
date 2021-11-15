#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import re

cal_year = 10
in_path = r'E:/BC/data/SBsb/'
SYB = pd.read_csv(in_path + 'SYB.csv', index_col=0)
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
SYB = SYB.loc[:str(today.replace(year=today.year - cal_year)), :]

s = {
    "code": 1,
    "message": "success",
    "data": [
        {
            "date": "2020-04-01T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.562802873848659
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-31T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.579863421617274
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-30T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.660476219465249
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-27T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.747137090562909
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-26T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.731245018454842
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-25T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.808484186310405
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-24T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.644815998954972
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-23T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.399040575794418
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-20T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.632676083610539
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-19T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.465137450271566
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-18T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.65082766931738
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-17T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.818375004439051
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-16T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.850836527313922
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-13T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.100211159217988
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-12T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.231228179400881
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-11T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.344932578606512
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-10T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.42828974391038
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-09T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.287756792232322
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-06T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.54247092585958
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-05T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.69261155312067
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-04T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.487072306857208
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-03T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.429466167729066
            },
            "stockCode": "000016"
        },
        {
            "date": "2020-03-02T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 9.393348716478224
            },
            "stockCode": "000016"
        }
    ]
}
SYB = SYB.dropna(axis=0, how='any')
if s['code']==1:
    print(s['message'])
SYB['syb_50'] = 1 / SYB['pe_50'] / SYB['y_10']
SYB['syb_300'] = 1 / SYB['pe_300'] / SYB['y_10']
print(SYB)


def cal_temp(da, axr=0):  # 将估值数据百分位化
    dp = [0]
    count = 0
    result = []
    if 1:
        for k1 in range(len(da)):
            if da[k1] != 0:
                dp.append(da[k1])
            for n1 in range(len(dp)):
                if dp[n1] < da[k1]:
                    count += 1
            if axr == 0:
                result.append(round(count * 100 / len(dp), 5))
            if axr == 1:
                result.append(round(100 - count * 100 / len(dp), 5))
            count = 0
        return result[-1]


temp_50 = 100 - (cal_temp(list(SYB['syb_50'])[::-1]))  # 50股债收益比百分位
temp_300 = 100 - (cal_temp(list(SYB['syb_300'])[::-1]))  # 300股债收益比百分位
temp_500 = (cal_temp(list(SYB['pb_500'])[::-1]))  # 500PB百分位
print('十年国债收益率  50股债收益比  50百分位   300股债收益比  300百分位   500PB    500百分位')
print('%.3f          %.3f        %.2f      %.3f        %.2f      %.2f     %.2f' % (
    100 * SYB.iloc[0, 0], SYB.iloc[0, 5], temp_50, SYB.iloc[0, 6], temp_300, SYB.iloc[0, 3], temp_500))
st = s['data'][0]['date']
print(st.split('T')[0])
'''s = {
    "code": 1,
    "message": "success",
    "data": [
        {
            "date": "2020-04-01T00:00:00+08:00",
            "pe_ttm": {
                "mcw": 8.562802873848659
            },
            "stockCode": "000016"
        },'''