#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import requests
import json

cal_year = 10  # 指数部分选取的时间长度
value_data = 5  # date,pe_ttm,cp,stockCode
day_set = 60  # 股票部分日期设定值，即选取的比较区间大小
in_path = r'E:/BC/data/wonder/'
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
# index_stock = str(today.replace(year=today.year - cal_year))
start_day = "2018-01-01"
ed = str(today)
url1 = "https://open.lixinger.com/api/cn/index/fundamental"  # 指数基本面
url2 = "https://open.lixinger.com/api/macro/national-debt"  # 国债
url_increase = "https://open.lixinger.com/api/cn/index/fs"  # 指数财务
token = "17871030-d55c-4562-b166-2ac0b5682a0f"
data1 = {
    "token": token,
    "startDate": start_day,
    "endDate": ed,
    "stockCodes": [
        "000016"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "pb.y10.mcw",
        "cp"
    ]
}
data2 = {
    "token": token,
    "startDate": start_day,
    "endDate": ed,
    "stockCodes": [
        "000300"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "pb.y10.mcw",
        "cp"
    ]
}
data3 = {
    "token": token,
    "startDate": start_day,
    "endDate": ed,
    "stockCodes": [
        "000905"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "pb.y10.mcw",
        "cp"
    ]
}
data4 = {
    "token": token,
    "startDate": start_day,
    "endDate": ed,
    "stockCodes": [
        "000852"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "pb.y10.mcw",
        "cp"
    ]
}
data5 = {
    "token": token,
    "startDate": start_day,
    "endDate": ed,
    "stockCodes": [
        "399303"
    ],
    "metricsList": [
        "pe_ttm.y10.mcw",
        "pb.y10.mcw",
        "cp"
    ]
}
data_y = {
    "token": token,
    "areaCode": "cn",
    "startDate": start_day,
    "endDate": ed,
    "metricsList": [
        "mir_y10"
    ]
}
data_i = {  # 三指数增长数据
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
s1000 = json.loads(requests.post(url=url1, data=json.dumps(data4), headers=headers).text)
s2000 = json.loads(requests.post(url=url1, data=json.dumps(data5), headers=headers).text)
sy = json.loads(requests.post(url=url2, data=json.dumps(data_y), headers=headers).text)
increase = json.loads(requests.post(url=url_increase, data=json.dumps(data_i), headers=headers).text)


def add_one(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date() + datetime.timedelta(days=1)


print("最新财报增长为：", increase['data'][0]["standardDate"])
for i_increase in range(0, 5):
    print(round(100 * increase['data'][i_increase]["q"]["ps"]["oi"]["c_y2y"], 2),
          round(100 * increase['data'][i_increase]["q"]["ps"]["np"]["c_y2y"], 2))

p_s_i, pe_50, pb_50, pe_300, pb_300, pe_500, pb_500, pre_500 = [], [], [], [], [], [], [], []
pe_1000, pb_1000, pe_2000, pb_2000, p_y, p_y_i, limit = [], [], [], [], [], [], []
for i in range(len(s50['data'])):
    if len(s50['data'][i]) == value_data:
        p_s_i.append(s50['data'][i]['date'].split('T')[0])
        pe_50.append(s50['data'][i]['pe_ttm']['y10']['mcw']['cv'])
        pb_50.append(s50['data'][i]['pb']['y10']['mcw']['cv'])
        pe_300.append(s300['data'][i]['pe_ttm']['y10']['mcw']['cv'])
        pb_300.append(s300['data'][i]['pb']['y10']['mcw']['cv'])
        pe_500.append(s500['data'][i]['pe_ttm']['y10']['mcw']['cv'])
        pb_500.append(s500['data'][i]['pb']['y10']['mcw']['cv'])
        pe_1000.append(s1000['data'][i]['pe_ttm']['y10']['mcw']['cv'])
        pb_1000.append(s1000['data'][i]['pb']['y10']['mcw']['cv'])
        pe_2000.append(s2000['data'][i]['pe_ttm']['y10']['mcw']['cv'])
        pb_2000.append(s2000['data'][i]['pb']['y10']['mcw']['cv'])
    else:
        print('数据缺失：', s50['data'][i])
for iy in range(len(sy['data'])):
    p_y_i.append(sy['data'][iy]['date'].split('T')[0])
    p_y.append(sy['data'][iy]['mir_y10'])
d1 = pd.DataFrame(
    data={'pe_50': pe_50, 'pb_50': pb_50, 'pe_300': pe_300, 'pb_300': pb_300, 'pe_500': pe_500, 'pb_500': pb_500,
          'pe_1000': pe_1000, 'pb_1000': pb_1000, 'pe_2000': pe_2000, 'pb_2000': pb_2000}, index=p_s_i)
# d2 = pd.DataFrame(data={'y_10': p2}, index=map(add_one, p7))
d2 = pd.DataFrame(data={'y_10': p_y}, index=p_y_i)
d1.index = pd.DatetimeIndex(d1.index)
d1.index.name = 'time'
d2.index = pd.DatetimeIndex(d2.index)
d2.index.name = 'time'

print('指数         当前PE       当前PB     最大PE     最小PE     最大PB     最小PB,')


def pe_pb(identifier, id_pe, id_pb, point):  # str
    def lim_map(x):
        return int(x * point)

    limit_pe = d1.loc[:'2018', id_pe][::-1]
    limit_pe.index = pd.to_datetime(limit_pe.index)
    limit_pb = d1.loc[:'2018', id_pb][::-1]
    limit_pb.index = pd.to_datetime(limit_pb.index)
    point_pe = limit_pe[-1]
    point_pb = limit_pb[-1]
    print('%s     %.2f     %.2f     %.2f     %.2f     %.2f     %.2f     %.2f' % (
        identifier, point, point_pe, point_pb, limit_pe['2019':].max(), limit_pe['2018':].min(),
        limit_pb['2019':].max(), limit_pb['2018':].min()))
    limit_high_pe = limit_pe['2019':].max() / point_pe
    limit_low_pe = limit_pe['2018':].min() / point_pe
    limit_high_pb = limit_pb['2019':].max() / point_pb
    limit_low_pb = limit_pb['2018':].min() / point_pb
    limit.append(
        [identifier, lim_map(limit_high_pe), lim_map(limit_high_pb), lim_map(limit_low_pe),
         lim_map(limit_low_pb),
         round(limit_high_pe / limit_high_pb, 3)])


pe_pb('上证50  ', 'pe_50', 'pb_50', s50['data'][0]['cp'])
pe_pb('沪深300 ', 'pe_300', 'pb_300', s300['data'][0]['cp'])
pe_pb('中证500 ', 'pe_500', 'pb_500', s500['data'][0]['cp'])
pe_pb('中证1000', 'pe_1000', 'pb_1000', s1000['data'][0]['cp'])
pe_pb('国证2000', 'pe_2000', 'pb_2000', s2000['data'][0]['cp'])
for lim in range(len(limit)):
    print(limit[lim])
print('券最新日期:', sy['data'][0]['date'].split('T')[0], len(p_s_i), len(p_y_i))  # 债券最新日期
SYB = pd.merge(d2, d1, on='time', how='inner')
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
    100 * SYB.iloc[0, 0], SYB.iloc[0, -2], temp_50, SYB.iloc[0, -1], temp_300, SYB.iloc[0, 6], temp_500))
# index_time | y_10,pe_50,pe_300,pb_500,pre_500,syb_50,syb_300

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
