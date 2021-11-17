#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import os
import datetime
import calendar
import requests
import json

cal_year = 1
update = 0
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

s50 = json.loads(requests.post(url=url1, data=json.dumps(data1), headers=headers).text)
sy = json.loads(requests.post(url=url2, data=json.dumps(data4), headers=headers).text)
print(s50)

def add_one(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date() + datetime.timedelta(days=1)


def pick_data(r50, ry):
    if 1:
        p1, p2, p3, p4, p5, p6 = [], [], [], [], [], []
        for i in range(len(r50['data'])):
            p1.append(r50['data'][i]['date'].split('T')[0])
            p3.append(r50['data'][i]['pe_ttm']['y10']['mcw']['cv'])

        for iy in range(len(ry['data'])):
            p4.append(ry['data'][iy]['date'].split('T')[0])
            p5.append(ry['data'][iy]['mir_y10'])
            p6 = map(add_one, p4)
        print(p5)
        print(p6)
        d1 = pd.DataFrame(data={'pe_50': p3}, index=p1)
        d2 = pd.DataFrame(data={'y_10': p5}, index=p6)
        print(d1)
        print(d2)
        d1.index=pd.DatetimeIndex(d1.index)
        d1.index.name='time'
        d2.index=pd.DatetimeIndex(d2.index)
        d2.index.name = 'time'
        print(d1.index)
        print(d2.index)
        d3 = pd.merge(d1,d2,on='time',how='inner')
        print(d3)
        return d3


pick_data(s50, sy)
