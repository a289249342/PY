#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ARASHI'

from EmQuantAPI import *
from WindPy import w
import datetime
import os
import xlrd
import xlwt
import pandas as pd
import numpy as np

out_path = r'E:/11.csv'
in_path = r'E:/BC/data/da/'
total_data = pd.read_excel(in_path + '2715.xls', header=0, encoding='gbk')
t=total_data.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
t.to_excel(in_path+'d.xls')