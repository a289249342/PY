#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import requests
import json

import pandas as pd
import datetime
import requests
import json

day_post = 1800  # 股票部分日期请求值,此值应在减去非交易日后仍大于设定值
day_set = 60  # 股票部分日期设定值，即选取的比较区间大小
threshold_value = 80
cal_year = 10  # 指数部分选取的时间长度
in_path = r'E:/BC/data/wonder/'
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
sd_stock = (datetime.date.today() + datetime.timedelta(days=-day_post)).strftime("%Y-%m-%d")
ed = str(today)
url1 = "https://open.lixinger.com/api/cn/index/fundamental"
url2 = "https://open.lixinger.com/api/macro/national-debt"
data1 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd_stock,
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
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd_stock,
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
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "startDate": sd_stock,
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
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "areaCode": "cn",
    "startDate": sd_stock,
    "endDate": ed,
    "metricsList": [
        "mir_y10"
    ]
}
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip,deflate, br, *"
}
# s50 = json.loads(requests.post(url=url1, data=json.dumps(data1), headers=headers).text)
# s300 = json.loads(requests.post(url=url1, data=json.dumps(data2), headers=headers).text)
s500 = json.loads(requests.post(url=url1, data=json.dumps(data3), headers=headers).text)
# sy = json.loads(requests.post(url=url2, data=json.dumps(data4), headers=headers).text)

stock_60ud = s500['data'][::-1]
stock = pd.DataFrame(stock_60ud)
stock.set_index(["date"], inplace=True)
stock.index = pd.DatetimeIndex(stock.index)
stock.index = stock.index.date
index_ud = stock.loc[:, 'cp']
index_all = []
for i in range(day_set, len(index_ud)):
    sim = index_ud[i - day_set:i]
    k = len(list(filter(lambda x: x <= index_ud[i], sim)))
    print(stock.index[i], index_ud[i], 10 * ' ' + str(k), min(sim), max(sim),'%.2f %.2f'%(100*(index_ud[i]/max(sim)-1),100*(index_ud[i]/min(sim)-1)))
print(100-100*index_ud[len(index_ud)-1]/max(index_ud[len(index_ud)-1-day_set:-1]))
index_all.append(len(list(filter(lambda x: x <= index_ud[-1], index_ud[len(index_ud) - 1 - day_set:-1]))))
