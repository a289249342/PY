#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import json
import requests

data1 = {
    "token": "17871030-d55c-4562-b166-2ac0b5682a0f",
    "date": "latest",
    "stockCodes": [
        "000016",
        "000300",
        "000905",
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
url1 = "https://open.lixinger.com/api/cn/index/fs"
increase = json.loads(requests.post(url=url1, data=json.dumps(data1), headers=headers).text)
print(increase['data'][0]["standardDate"])

for ss in range(0, 4):
    print(round(100 * increase['data'][ss]["q"]["ps"]["oi"]["c_y2y"], 2),
          round(100 * increase['data'][ss]["q"]["ps"]["np"]["c_y2y"], 2))
