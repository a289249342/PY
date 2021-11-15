#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import json
import pandas as pd
import requests
import datetime

# user-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
in_path = r'E:/BC/data/bond_c/'
url = 'https://www.jisilu.cn/web/data/cb/list'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
headers = {
    'user-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53'}
cookie = {
    'Cookie': 'kbz_newcookie=1; kbzw_r_uname=289249342; kbzw__Session=bs2kstmclmgshc64pqfv63jfe0; kbzw__user_login=7Obd08_P1ebax9aXqZqvk6uwpqyTkZyh6dbc7OPm1Nq_1KKoqJqpx9WtpqGw0quVqJnZqqaoxaSa2a3XmqzN3JasmZiyoO3K1L_RpKibrKStkpecpMy01r6bruPz3tXlzaaXpJGXn8rhz9TQ6-yVt82MqJKkkbKXyuHPppWvme2fraeX1Oybr6ehqIqQqNnc4NionqeTppGop6SYp9nT2d_k4aikp5Cm'}
ic = requests.get(url, cookies=cookie, headers=headers)
# ic = requests.get(url)
data = ic.content.decode("utf-8")


print(data)