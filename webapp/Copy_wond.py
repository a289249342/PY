#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import requests
import json

cal_year = 10  # 指数部分选取的时间长度
value_data = 4  # date,pe_ttm,cp,stockCode
day_set = 60  # 股票部分日期设定值，即选取的比较区间大小
in_path = r'E:/BC/data/wonder/'
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
index_stock = str(today.replace(year=today.year - cal_year))
ed = str(today)
url1 = "https://open.lixinger.com/api/cn/index/fundamental"  # 指数基本面
url2 = "https://open.lixinger.com/api/macro/national-debt"  # 国债
url_increase = "https://open.lixinger.com/api/cn/index/fs"  # 指数财务
token = "17871030-d55c-4562-b166-2ac0b5682a0f"
data1 = {
    "token": token,
    "startDate": index_stock,
    "endDate": ed,
    "stockCodes": [
        "000016"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "cp"
    ]
}
data2 = {
    "token": token,
    "startDate": index_stock,
    "endDate": ed,
    "stockCodes": [
        "000300"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "cp"
    ]
}
data3 = {
    "token": token,
    "startDate": index_stock,
    "endDate": ed,
    "stockCodes": [
        "000905"
    ],
    "metricsList": [
        "pb.y10.mcw",
        "cp"
    ]
}
data4 = {
    "token": token,
    "areaCode": "cn",
    "startDate": index_stock,
    "endDate": ed,
    "metricsList": [
        "mir_y10"
    ]
}
data5 = {  # 三指数增长数据
    "token": token,
    "date": "latest",
    "stockCodes": [
        "000016",
        "000300",
        "000905",
        "000852",
        "399303"
    ],
    "metricsList": [
        "q.ps.oi.c_y2y",
        "q.ps.np.c_y2y"
    ]
}
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip,deflate, br, *"
}
s50 = json.loads(requests.post(url=url1, data=json.dumps(data1), headers=headers).text)
s300 = json.loads(requests.post(url=url1, data=json.dumps(data2), headers=headers).text)
s500 = json.loads(requests.post(url=url1, data=json.dumps(data3), headers=headers).text)
sy = json.loads(requests.post(url=url2, data=json.dumps(data4), headers=headers).text)
increase = json.loads(requests.post(url=url_increase, data=json.dumps(data5), headers=headers).text)


def add_one(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date() + datetime.timedelta(days=1)


print("最新财报增长为：", increase['data'][0]["standardDate"])
for i_increase in range(0, 5):
    print(round(100 * increase['data'][i_increase]["q"]["ps"]["oi"]["c_y2y"], 2),
          round(100 * increase['data'][i_increase]["q"]["ps"]["np"]["c_y2y"], 2))


def pick_data(r50, r300, r500, ry):
    if r50['code'] == 1:
        p1, p2, p3, p4, p5, p6, p7 = [], [], [], [], [], [], []
        for i in range(len(r50['data'])):
            if len(r50['data'][i]) == value_data:
                p1.append(r50['data'][i]['date'].split('T')[0])
                p3.append(r50['data'][i]['pe_ttm']['y10']['mcw']['cv'])
                p4.append(r300['data'][i]['pe_ttm']['y10']['mcw']['cv'])
                p5.append(r500['data'][i]['pb']['y10']['mcw']['cv'])
                p6.append(r500['data'][i]['pb']['y10']['mcw']['cvpos'])
            elif len(r50['data'][i]) == 2:
                print('数据缺失：', r50['data'][i])
        for iy in range(len(ry['data'])):
            p7.append(ry['data'][iy]['date'].split('T')[0])
            p2.append(ry['data'][iy]['mir_y10'])
        print(add_one(ry['data'][0]['date'].split('T')[0]))  # 债券最新日期
        print(len(p1), len(p2), len(p3), len(p4), len(p5), len(p6))
        d1 = pd.DataFrame(data={'pe_50': p3, 'pe_300': p4, 'pb_500': p5, 'pre_500': p6}, index=p1)
        # d2 = pd.DataFrame(data={'y_10': p2}, index=map(add_one, p7))
        d2 = pd.DataFrame(data={'y_10': p2}, index=p7)
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
print(SYB.iloc[:2, :])


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
print('50|300:15高点2,1.5,19年初3.8,3.17,20疫情4.7,3.65')
print('十年国债收益率  50股债收益比  50百分位   300股债收益比  300百分位   500PB    500百分位   ' + str(today))
print('%.3f          %.3f        %.2f     %.3f         %.2f      %.3f     %.2f' % (
    100 * SYB.iloc[0, 0], SYB.iloc[0, 5], temp_50, SYB.iloc[0, 6], temp_300, SYB.iloc[0, 3], temp_500))

index_all = []
index_a_p = []


def index_60ud(index_data):
    stock_60ud = index_data['data'][::-1]
    stock = pd.DataFrame(stock_60ud)
    stock.set_index(["date"], inplace=True)
    stock.index = pd.DatetimeIndex(stock.index)
    stock.index = stock.index.date
    index_ud = stock.loc[:, 'cp']
    index_a_p.append(round(100 * index_ud[len(index_ud) - 1] / max(index_ud[len(index_ud) - 1 - day_set:-1]) - 100, 2))
    index_all.append(len(list(filter(lambda x: x <= index_ud[-1], index_ud[len(index_ud) - 1 - day_set:-1]))))


index_60ud(s50)
index_60ud(s300)
index_60ud(s500)
print(index_a_p)
print(index_all)
