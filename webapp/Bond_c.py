#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import json
import os

import pandas as pd
import requests
import datetime

# user-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53
in_path = r'E:/BC/data/bond_c/'
url = 'https://www.jisilu.cn/webapi/cb/list/'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
headers = {
    'user-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53'}
cookie = {
    'Cookie': 'kbz_newcookie=1; kbzw_r_uname=289249342; kbzw__Session=bs2kstmclmgshc64pqfv63jfe0; kbzw__user_login=7Obd08_P1ebax9aXqZqvk6uwpqyTkZyh6dbc7OPm1Nq_1KKoqJqpx9WtpqGw0quVqJnZqqaoxaSa2a3XmqzN3JasmZiyoO3K1L_RpKibrKStkpecpMy01r6bruPz3tXlzaaXpJGXn8rhz9TQ6-yVt82MqJKkkbKXyuHPppWvme2fraeX1Oybr6ehqIqQqNnc4NionqeTppGop6SYp9nT2d_k4aikp5Cm'}
ic = requests.get(url, cookies=cookie, headers=headers)
# ic = requests.get(url)
data = ic.content.decode("utf-8")
dat = json.loads(data)
d = dat['data']


# bond_list = pd.DataFrame(d)
# bond_list.set_index(['bond_id'], inplace=True)
# bond_list.to_excel(in_path + 'bond_date/' + str(datetime.date.today()) + '.xlsx')


def loop_back_test():
    date_path = os.listdir(in_path + 'bond_date/')
    bond_limit = 10
    initialization = 1
    date_path = ['2021-07-19.xlsx', '2021-07-22.xlsx', '2021-07-23.xlsx']
    for path in date_path:
        print(path)
        bond_list = pd.read_excel(in_path + 'bond_date/' + path, index_col=0)
        bond_list = bond_list[(bond_list.btype == 'C') & (bond_list.price != 100)]
        bond_list = bond_list.loc[:, ['bond_nm', 'premium_rt', 'price']]
        bond_list['value10'] = list(map(lambda x, y: 10 * x + y, bond_list['premium_rt'], bond_list['price']))
        bond_list['value08'] = list(map(lambda x, y: 8 * x + y, bond_list['premium_rt'], bond_list['price']))
        bond_list['value06'] = list(map(lambda x, y: 6 * x + y, bond_list['premium_rt'], bond_list['price']))
        bond_list['value04'] = list(map(lambda x, y: 4 * x + y, bond_list['premium_rt'], bond_list['price']))
        bond_list['value22'] = list(map(lambda x, y: x + y, bond_list['premium_rt'], bond_list['price']))

        def group_update(identifier):
            value_id = 'value' + identifier  # value10
            hold_id = 'hold' + identifier  # hold10
            value_group = pd.read_excel(in_path + value_id + '.xlsx', index_col=0)  # v,change,bs,buy,sell
            hold_10 = pd.read_excel(in_path + hold_id + '.xlsx', index_col=0)  # hold_list
            cash_out = 0
            candidate_list = bond_list.loc[:, ['bond_nm', 'premium_rt', 'price', value_id]].sort_values(
                by=value_id)[:bond_limit]
            if len(value_group) == 0 or initialization == 1:
                candidate_list.to_excel(in_path + hold_id + '.xlsx')
                value_initialization = pd.DataFrame(
                    [1, 0, 1, candidate_list['price'].sum(), candidate_list['price'].sum()]).T
                value_initialization.columns = ['Value', 'change', 'bs', 'buy', 'sell']
                value_initialization.to_excel(in_path + value_id + '.xlsx')
                print(candidate_list['price'].sum())
                print(value_initialization)
            else:
                print(hold_10.index)
                for i in hold_10.index:
                    print(str(i) in bond_list.index)
                    if str(i) in bond_list.index:
                        cash_out += bond_list.loc[str(i), 'price']
                        print(bond_list.loc[str(i), ['price', 'bond_nm']])
                    else:
                        cash_out += hold_10.loc[i, 'price']
                        print(hold_10.loc[i, ['price', 'bond_nm']])
                cash_into = candidate_list['price'].sum()
                value, change, bs, buy, sell = value_group.iloc[-1, :]
                new_10 = pd.DataFrame(
                    [cash_out / sell * value, cash_out / sell - 1, cash_out / buy, buy + cash_into - cash_out,
                     cash_out]).T
                new_10.columns = ['Value', 'change', 'bs', 'buy', 'sell']
                value_group = value_group.append(new_10, ignore_index=1)
                print(candidate_list)
                candidate_list.to_excel(in_path + hold_id + '.xlsx')
                value_group.to_excel(in_path + value_id + '.xlsx')

        # group_list = ['22', '04', '06', '08', '10']
        group_list = ['04']
        for group_id in group_list:
            group_update(group_id)
        if initialization == 1:
            initialization = 0


loop_back_test()
