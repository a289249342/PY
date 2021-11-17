#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import requests
import json

cal_year = 10
update = 1
in_path = r'E:/BC/data/SBsb/'
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
sd = str(today.replace(year=today.year - cal_year))
ed = str(today)
url1 = "https://open.lixinger.com/api/a/index/fundamental"
url2 = "https://open.lixinger.com/api/macro/national-debt"
data1 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd,
    "endDate": ed,
    "stockCodes": [
        "000016"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw"
    ]
}
data2 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd,
    "endDate": ed,
    "stockCodes": [
        "000300"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw"
    ]
}
data3 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd,
    "endDate": ed,
    "stockCodes": [
        "000905"
    ],
    "metricsList": [
        "pb.y10.mcw"
    ]
}
data4 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "areaCode": "cn",
    "startDate": sd,
    "endDate": ed,
    "metricsList": [
        "mir_y10"
    ]
}
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip,deflate, br, *"
}
if update == 1:
    s50 = json.loads(requests.post(url=url1, data=json.dumps(data1), headers=headers).text)
    s300 = json.loads(requests.post(url=url1, data=json.dumps(data2), headers=headers).text)
    s500 = json.loads(requests.post(url=url1, data=json.dumps(data3), headers=headers).text)
    sy = json.loads(requests.post(url=url2, data=json.dumps(data4), headers=headers).text)

# res = requests.post(url=url, data=json.dumps(data), headers=headers)
# print(res.text)

def add_one(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date() + datetime.timedelta(days=1)


def pick_data(r50, r300, r500, ry):
    if r50['code'] == 1:
        p1, p2, p3, p4, p5, p6, p7 = [], [], [], [], [], [], []
        for i in range(len(r50['data'])):
            p1.append(r50['data'][i]['date'].split('T')[0])
            p3.append(r50['data'][i]['pe_ttm']['y10']['mcw']['cv'])
            p4.append(r300['data'][i]['pe_ttm']['y10']['mcw']['cv'])
            p5.append(r500['data'][i]['pb']['y10']['mcw']['cv'])
            p6.append(r500['data'][i]['pb']['y10']['mcw']['cvpos'])
        for iy in range(len(ry['data'])):
            p7.append(ry['data'][iy]['date'].split('T')[0])
            p2.append(ry['data'][iy]['mir_y10'])
        print(add_one(ry['data'][0]['date'].split('T')[0]))  # X****************************************************
        print(len(p1), len(p2), len(p3), len(p4), len(p5), len(p6))
        d1 = pd.DataFrame(data={'pe_50': p3, 'pe_300': p4, 'pb_500': p5, 'pre_500': p6}, index=p1)
        d2 = pd.DataFrame(data={'y_10': p2}, index=map(add_one, p7))
        d1.index = pd.DatetimeIndex(d1.index)
        d1.index.name = 'time'
        d2.index = pd.DatetimeIndex(d2.index)
        d2.index.name = 'time'
        d3 = pd.merge(d2, d1, on='time', how='inner')
        return d3
    else:
        print(r50, r300, r500, sy)


SYB = pick_data(s50, s300, s500, sy)
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
print('十年国债收益率  50股债收益比  50百分位   300股债收益比  300百分位   500PB    500百分位   '+str(today))
print('%.3f          %.3f        %.2f     %.3f         %.2f      %.3f     %.2f' % (
    100 * SYB.iloc[0, 0], SYB.iloc[0, 5], temp_50, SYB.iloc[0, 6], temp_300, SYB.iloc[0, 3], temp_500))
