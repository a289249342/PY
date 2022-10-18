#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import requests
import re
import time

in_path = r'E:/BC/data/book/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
u1 = "http://m.nbian.com/wapbook/10_10931_"
u2 = ".html"
s = ''


def r_quest(url):
    response = requests.post(url=url, headers=headers)
    responses = response.text
    book = re.split(r'</center>', responses)[1]
    book = book.replace('<u>', '')
    book = book.replace('</u>', '')
    book = book.replace('&nbsp;', '')
    c = re.split(r'<br/><br/>', book)
    # print(c)
    return c


def nov(a1, a2=2):
    url = u1 + str(a1) + u2
    b = r_quest(url)
    for w1 in range(0, len(b), 5):
        b[w1] = b[w1] + '\n'
    f.writelines(b[3]+'\n')
    f.writelines(b[3]+'\n')
    for i in range(4, len(b) - 1):
        f.writelines(b[i])
    f.writelin(re.split(r'<', b[-1])[0])
    r = int(re.findall('[0-9]+', b[-1])[1])
    time.sleep(1)
    while a2 <= r:
        url = u1 + str(a1) + '-' + str(a2) + u2
        b = r_quest(url)
        for w1 in range(0, len(b), 5):
            b[w1] = b[w1] + '\n'
        f.write(re.split(r'\n\t\t\t', b[0])[1])
        for i in range(1, len(b) - 1):
            f.writelines(b[i])
        f.write(re.split(r'<', b[-1])[0])
        a2 += 1
        time.sleep(1)


# 193331-193365
# 470638-470639

with open(in_path + '11.txt', 'w') as f:
    for j in range(193331, 193366):
        nov(j)
    nov(470638)
    nov(470639)
