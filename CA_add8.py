#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import datetime
import time
import os
import xlrd
import xlwt
from EmQuantAPI import *


def c_date(date_day):
    delta = datetime.timedelta(days=date_day)
    m_date = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta
    return m_date.strftime('%Y-%m-%d')
    return m_date


def get_data(code, day):
    time.sleep(0.18)

    day1 = "TradeDate=" + day + ",Type=1"  # Type=1 正股市盈率市净率取上年年报
    day2 = "TradeDate=" + day + ",Type=2"  # Type=2 意为全价表示收盘价
    # 2020-03-09 16:18:06
    # 债券 收盘价 转股价 转股价值 转股市净率 转股市盈率 转股溢价率
    # data = c.css(
    #     "110031.SH,110033.SH,110034.SH,110038.SH,110041.SH,110042.SH,110043.SH,110044.SH,110045.SH,110046.SH,110047.SH,110048.SH,110050.SH,110051.SH,110052.SH,110053.SH,110054.SH,110055.SH,110056.SH,110057.SH,110058.SH,110059.SH,110060.SH,110061.SH,110062.SH,110063.SH,110064.SH,110065.SH,110066.SH,113008.SH,113009.SH,113011.SH,113012.SH,113013.SH,113014.SH,113016.SH,113017.SH,113019.SH,113020.SH,113021.SH,113022.SH,113024.SH,113025.SH,113026.SH,113027.SH,113028.SH,113029.SH,113030.SH,113031.SH,113032.SH,113502.SH,113503.SH,113504.SH,113505.SH,113508.SH,113509.SH,113510.SH,113511.SH,113514.SH,113515.SH,113516.SH,113517.SH,113518.SH,113519.SH,113520.SH,113521.SH,113524.SH,113525.SH,113526.SH,113527.SH,113528.SH,113530.SH,113531.SH,113532.SH,113534.SH,113535.SH,113536.SH,113537.SH,113539.SH,113540.SH,113541.SH,113542.SH,113543.SH,113544.SH,113545.SH,113546.SH,113547.SH,113548.SH,113549.SH,113550.SH,113551.SH,113552.SH,113553.SH,113554.SH,113555.SH,113556.SH,113557.SH,113558.SH,113559.SH,113561.SH,113562.SH,113563.SH,113564.SH,113565.SH,113566.SH,113567.SH,113568.SH,113569.SH,113570.SH,145900.SH,117103.SZ,123002.SZ,123004.SZ,123007.SZ,123009.SZ,123010.SZ,123011.SZ,123012.SZ,123013.SZ,123014.SZ,123015.SZ,123016.SZ,123017.SZ,123018.SZ,123019.SZ,123020.SZ,123021.SZ,123022.SZ,123023.SZ,123024.SZ,123025.SZ,123026.SZ,123027.SZ,123028.SZ,123029.SZ,123030.SZ,123031.SZ,123032.SZ,123033.SZ,123034.SZ,123035.SZ,123036.SZ,123037.SZ,123038.SZ,123039.SZ,123040.SZ,123041.SZ,123042.SZ,123043.SZ,124001.SZ,124002.SZ,127003.SZ,127004.SZ,127005.SZ,127006.SZ,127007.SZ,127008.SZ,127011.SZ,127012.SZ,127013.SZ,127014.SZ,127015.SZ,128010.SZ,128012.SZ,128013.SZ,128014.SZ,128015.SZ,128016.SZ,128017.SZ,128018.SZ,128019.SZ,128021.SZ,128022.SZ,128023.SZ,128025.SZ,128026.SZ,128028.SZ,128029.SZ,128030.SZ,128032.SZ,128033.SZ,128034.SZ,128035.SZ,128036.SZ,128037.SZ,128038.SZ,128039.SZ,128040.SZ,128041.SZ,128042.SZ,128043.SZ,128044.SZ,128045.SZ,128046.SZ,128048.SZ,128049.SZ,128050.SZ,128051.SZ,128052.SZ,128053.SZ,128054.SZ,128055.SZ,128056.SZ,128057.SZ,128058.SZ,128059.SZ,128060.SZ,128061.SZ,128062.SZ,128063.SZ,128064.SZ,128065.SZ,128066.SZ,128067.SZ,128069.SZ,128070.SZ,128071.SZ,128072.SZ,128073.SZ,128074.SZ,128075.SZ,128076.SZ,128077.SZ,128078.SZ,128079.SZ,128080.SZ,128081.SZ,128082.SZ,128083.SZ,128084.SZ,128085.SZ,128086.SZ,128087.SZ,128088.SZ,128089.SZ,128090.SZ,128091.SZ,128092.SZ,128093.SZ,128094.SZ,128095.SZ,128096.SZ,128097.SZ,128098.SZ,128099.SZ",
    #     "CBCONVERSIONPRICE,CBCONVVALUE,CBCONVPB,CBCONVPE,CBCONVPREMIUMRATIO", "TradeDate=2020-03-09")
    data2 = list(c.css(code, "close", day2).Data.values())
    data1 = list(
        c.css(code, "CBCONVERSIONPRICE,CBCONVVALUE,CBCONVPB,CBCONVPE,CBCONVPREMIUMRATIO", day1).Data.values())
    day_data = data1[0]
    day_data.insert(0, data2[0][0])
    # 收盘价 转股价 转股价值 市净率 市盈率 转股溢价率
    return day_data


c.start()
log_error = []
log_txt = []
total_data = []
in_path = r'E:/BC/data/ts/'
out_path = r'E:/BC/data/nts/'
with open(in_path + 't_log.txt') as I_File:
    for i2 in I_File:
        log_txt.append(i2.strip('\n'))
for path in log_txt:
    workbook = xlrd.open_workbook(in_path + path + '.xls')
    names = workbook.sheet_names()
    worksheet = workbook.sheet_by_index(0)
    nrows = worksheet.nrows
    ncols = worksheet.ncols
    new_all = []
    new_close = ['收盘价格']
    new_cpr = ['转股价']
    new_cpv = ['转股价值']
    new_cpb = ['转股市净率']
    new_cpe = ['转股市盈率']
    new_cra = ['转股溢价率']
    new_vpb = ['价值市净率']
    new_vpe = ['价值市盈率']
    for i0 in worksheet.col_values(2):
        try:
            k = c_date(i0)
            if 1:
                val = get_data(path, k)
                new_close.append(val[0])
                new_cpr.append(val[1])
                new_cpv.append(val[2])
                new_cpb.append(val[3])
                new_cpe.append(val[4])
                new_cra.append(val[5])

                if val[3] is None or val[0] == 0:
                    new_vpb.append('')
                else:
                    new_vpb.append(val[3] / val[0] * 100 / val[1] * val[2])
                if val[4] is None or val[0] == 0:
                    new_vpe.append('')
                else:
                    new_vpe.append(val[4] / val[0] * 100 / val[1] * val[2])

        except TypeError as e:
            if i0 != '' and i0 != '日期':
                new_vpb.append('')
                new_vpe.append('')
                with open(out_path + 'log_error.txt', mode='a+') as f:
                    f.writelines(path + str(c_date(i0)))
                print(c_date(i0), e, '******************************************************************')
    for i1 in range(ncols):
        new_col = worksheet.col_values(i1)
        if worksheet.col_values(i1)[0] == '日期':
            for i4 in range(len(worksheet.col_values(i1))):
                try:
                    new_col[i4] = c_date(worksheet.col_values(i1)[i4])
                except TypeError:
                    pass
        for i2 in range(nrows):
            if new_col[nrows - 1 - i2] == '' or new_col[nrows - 1 - i2] == '数据来源：Wind':
                new_col.pop(nrows - 1 - i2)
        new_all.append(new_col)

    new_all.append(new_close)
    new_all.append(new_cpr)
    new_all.append(new_cpv)
    new_all.append(new_cpb)
    new_all.append(new_cpe)
    new_all.append(new_cra)
    new_all.append(new_vpb)
    new_all.append(new_vpe)
    print(new_all[1])
    new_book = xlwt.Workbook()
    new_sheet = new_book.add_sheet("file")
    for i in range(len(new_all)):
        for j in range(len(new_all[i])):
            new_sheet.write(j, i, new_all[i][j])
    new_book.save(out_path + 'n_' + path + '.xls')
c.stop()
