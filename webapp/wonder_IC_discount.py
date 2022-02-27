#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import time
import requests
import datetime
import re
import calendar

in_path = r'E:/BC/data/IC/'


def third_friday(year, month):  # 计算每月第三个星期五
    return [day for week in calendar.Calendar(firstweekday=calendar.SUNDAY).monthdatescalendar(year, month) for day
            in week if day.weekday() == calendar.FRIDAY and day.month == month][2]


with open(in_path + 'Balance.txt', 'w') as f_file:
    pass
# 生成URL抓取合约价格↓↓↓↓↓↓↓↓
date_today = datetime.date.today()
y1 = str(date_today.year)[-2:]
y2 = str(date_today.year + 1)[-2:]
if date_today > third_friday(date_today.year, date_today.month):
    ic_contract = date_today.month + 1
else:
    ic_contract = date_today.month
url = 'http://hq.sinajs.cn/list='
for c in [ic_contract, ic_contract + 1, ic_contract + 4 - (ic_contract + 1) % 3,
          ic_contract + 7 - (ic_contract + 1) % 3]:
    if c <= 12:
        url = url + 'nf_IC' + y1 + '%02d' % c + ','
    else:
        url = url + 'nf_IC' + y2 + '%02d' % (c % 12) + ','
url = url[:-1]
headers = {'referer': 'https://finance.sina.com.cn/'}


def ic_update():
    try:
        r = requests.get('http://hq.sinajs.cn/list=s_sh000905', headers=headers).text
        ic_500 = re.split(',', r)[1]
        print('***********************************************************')
        # url = 'http://hq.sinajs.cn/list=nf_IC2109,nf_IC2110,nf_IC2112,nf_IC2203'
        ic = requests.get(url,headers=headers).text.split(';')
        if ic[-1] == '\n':
            ic.pop()
        ic_price, ic_date, ic_daily = [], [], []
        ic_output1, ic_output2 = '', ''
        ic_max = 0
        for i in ic:
            price = re.split(',', i)[3]
            name = re.search(r'IC\d+', i).group()
            t = third_friday(int('20' + name[2:4]), int(name[4:]))
            tt = t.__sub__(datetime.date.today()).days
            ic_price.append(float(price))
            ic_date.append(float(tt))
            if tt == 0:  # 交割日合约以最后两小时指数算术平均价计算
                time_today = datetime.datetime.now()
                time_start = datetime.time(13, 0, 0, 0)
                time_end = datetime.time(15, 0, 0, 0)
                if time_today.strftime('%H%M%S') > time_start.strftime('%H%M%S') and time_today.strftime(
                        '%H%M%S') < time_end.strftime('%H%M%S'):
                    with open(in_path + 'Balance.txt', 'r') as f:
                        f_read = f.read().split(',')
                    if len(f_read) == 1:
                        with open(in_path + 'Balance.txt', 'w') as f:
                            f.write(ic_500 + ',1')
                    elif len(f_read) == 2:
                        ic_total = float(ic_500) + float(f_read[0])
                        ic_num = float(f_read[1]) + 1
                        ic_daily.append(ic_total / ic_num - float(price))
                        with open(in_path + 'Balance.txt', 'w') as f:
                            f.write(str(ic_total) + ',' + str(ic_num))
                else:
                    ic_daily.append((float(ic_500) - float(price)))
            else:
                ic_daily.append((float(ic_500) - float(price)) / tt)
        for c0 in range(len(ic_daily)):  # 开始编写输出
            ic_output1 = ic_output1 + str(round(ic_daily[c0], 2)) + '   '
        for a in range(len(ic_price) - 1):
            for b in range(a + 1, 4):
                ic_month = (ic_price[a] - ic_price[b]) / (ic_date[b] - ic_date[a])
                if ic_month > ic_max:
                    ic_max = ic_month
                ic_output2 = ic_output2 + str(round(ic_month, 2)) + '   '
        ic_output2 = ic_output2 + 'max:%f' % ic_max
        print(ic_output1)
        print(ic_output2)
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError', e)
        time.sleep(100)
        return


ic_update()
while 1:
    time.sleep(2)
    n_time = time.strftime("%H:%M:%S", time.localtime())
    if "09:30:00" <= n_time <= "11:30:00" or "13:00:00" <= n_time <= "15:00:00":
        ic_update()
    elif n_time > "15:00:00":
        break
