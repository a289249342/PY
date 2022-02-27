#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import pandas as pd
import datetime
import requests
import json

day_post = 120  # 股票部分日期请求值,此值应在减去非交易日后仍大于设定值
day_set = 60  # 股票部分日期设定值，即选取的比较区间大小
threshold_value = 2
cal_year = 10  # 指数部分选取的时间长度
in_path = r'E:/BC/data/wonder/'
# SYB.index = pd.DatetimeIndex(SYB.index)
today = datetime.date.today()
sd_stock = (datetime.date.today() + datetime.timedelta(days=-day_post)).strftime("%Y-%m-%d")
ed = str(today)
url_stock = "https://open.lixinger.com/api/cn/company/fundamental/non_financial"
token = "17871030-d55c-4562-b166-2ac0b5682a0f"
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip,deflate, br, *"
}
st, st1, st2 = {}, {}, {}


def stock_data_get(stock_codes):
    js_stock = json.loads(requests.post(url=url_stock, data=json.dumps(
        {"token": token, "startDate": sd_stock, "endDate": ed, "stockCodes": [stock_codes],
         "metricsList": ["fc_rights"]}), headers=headers).text)  # 前复权
    stock_60ud = js_stock['data'][::-1]
    stock = pd.DataFrame(stock_60ud)
    stock.set_index(["date"], inplace=True)
    stock.index = pd.DatetimeIndex(stock.index)
    stock.index = stock.index.date
    price_stock = (list(stock.iloc[:, 0]))
    for i in range(day_set, len(price_stock)):
        sim = price_stock[i - day_set:i]
        k = len(list(filter(lambda x: x <= price_stock[i], sim)))
        print(stock_codes, stock.index[i], price_stock[i], 10 * ' ' + str(k), min(sim), max(sim),
              '%.2f %.2f' % (100 * (price_stock[i] / max(sim) - 1), 100 * (price_stock[i] / min(sim) - 1)))
    st[stock_codes] = len(list(filter(lambda x: x <= price_stock[-1], price_stock[len(price_stock) - 1 - day_set:-1])))
    st1[stock_codes] = round(100*(price_stock[-1]/min(price_stock[len(price_stock)-day_set:])-1),2)
    st2[stock_codes] = round(100*(price_stock[-1]/max(price_stock[len(price_stock)-day_set:])-1),2)
    print(40 * '*')


d = pd.read_excel(in_path + 's28.xlsx')
for i0 in range(len(d)):
    stock_data_get((6 - len(str(d.iloc[i0, 0]))) * '0' + str(d.iloc[i0, 0]))

print(sorted(st.items(), key=lambda item: item[1]))
print(sorted(st1.items(), key=lambda item: item[1]))
print(sorted(st2.items(), key=lambda item: item[1]))
