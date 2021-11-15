#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

from WindPy import *
from numpy import datetime64
import pandas as pd
import datetime
import time
import webbrowser
from io import BytesIO
from lxml import etree
import base64
import matplotlib.pyplot as plt
import matplotlib
import requests
import traceback
import configparser

try:
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    in_path = r'E:/Temp/'
    conf = configparser.ConfigParser()
    conf.read(in_path + 'config.ini')
    # G：global 全球温度计  A ：A股温度计
    G_data = pd.read_excel(in_path + 'G_data.xlsx', header=0, index_col=0, encoding='gbk')
    A_data = pd.read_excel(in_path + 'A_data.xlsx', header=0, index_col=0, encoding='gbk')
    G_data = G_data['2000':]
    A_data = A_data['2005':]
    # G_data.index = G_data.index.date
    # A_data.index = A_data.index.date
    # G_data.index.name = '时间'
    # A_data.index.name = '时间'
    update_temp = 1
    back_day = conf.getint('conf', 'back')  # back默认-5，意为重新读取前5日的数据，防止源数据更新不及时带来的错误
    end_day = datetime.date.today()
    # end_day = datetime.date(2020, 5, 26)
    if update_temp == 1:
        w.start()
        d_g = w.tdays(G_data.index.date[back_day], end_day, "TradingCalendar=AMEX")
        d_a = w.tdays(A_data.index.date[back_day], end_day)
        day_g = d_g.Times
        day_a = d_a.Times
        if len(day_g) > 1:
            day_g.pop(-1)
            for dd_g in day_g:
                # priceAdj=F;  前复权
                dg_to_list = []
                s = "tradeDate=" + dd_g.strftime("%Y%m%d") + ";cycle=D;ShowBlank=0"
                data = w.wss("DJI.GI,IXIC.GI,SPX.GI,FTSE.GI,FCHI.GI,GDAXI.GI,N225.GI,HSI.HI,000985.CSI,881003.WI",
                             "pb_lf,pe_ttm,close", s)
                for d2 in data.Data:
                    for d3 in d2:
                        dg_to_list.append(d3)
                G_data.loc[datetime64(dd_g)] = dg_to_list
        if day_a:
            for dd_a in day_a:
                da_to_list = []
                s = "tradeDate=" + dd_a.strftime("%Y%m%d") + ";cycle=D;ShowBlank=0"
                data = w.wss("000985.CSI,881003.WI", "pb_lf,pe_ttm,close", s)
                for d4 in data.Data:
                    for d5 in d4:
                        da_to_list.append(d5)
                A_data.loc[datetime64(dd_a)] = da_to_list


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
            print(result)
            return result


    g_list = []
    a_list = []
    for i0 in range(20):  # 计算温度并组装为list
        g_list.append(cal_temp(list(G_data.iloc[:, i0])))
    for i5 in range(4):
        a_list.append(cal_temp(list(A_data.iloc[:, i5])))
    g_std = []
    a_std = []
    for i1 in range(10):  # 计算第一个非零值并作为基准
        l1 = list(G_data.iloc[:, i1])
        l2 = list(G_data.iloc[:, i1 + 10])
        for i2 in range(len(l1)):
            if l1[i2] != 0 or l2[i2] != 0:
                g_std.append(G_data.iloc[i2, i1 + 20])
                break
    for i6 in range(2):
        l3 = list(A_data.iloc[:, i6])
        l4 = list(A_data.iloc[:, i6 + 2])
        for i7 in range(len(l3)):
            if l3[i7] != 0 or l4[i7] != 0:
                a_std.append(A_data.iloc[i7, i6 + 4])
                break

    g = pd.DataFrame(g_list).T
    g.index = G_data.index
    a = pd.DataFrame(a_list).T
    a.index = A_data.index
    for i4 in range(len(g_std)):  # 将各指数点位除以其基准值以便统一计算
        g[i4 + 20] = G_data.iloc[:, i4 + 20].apply(lambda x: x / g_std[i4])
    for i8 in range(len(a_std)):
        a[i8 + 4] = A_data.iloc[:, i8 + 4].apply(lambda x: x / a_std[i8])
    g.columns = G_data.columns
    a.columns = A_data.columns
    tem = [0] * 10
    tem2 = [0] * 10


    def cal_g_temp(x):  # 计算全球加权温度，权重为A股30%，美股（道琼斯、纳斯达克、标普）共30%，港股20%，欧洲（英、法、德）共15%，日经5%
        global tem  # 默认计算价格，带2后缀的为计算温度
        global tem2
        ca = []
        ta = []
        count = 0  # 除数计数器，无估值数据的指数不纳入计算
        r = 0.8  # 此为市净率与市盈率估值的权重，默认为0.8:0.2
        for i3 in range(10):  # 若估值数据异常为0，则使用上一交易日数据
            if x[i3] != 0 and x[i3 + 10] != 0:
                ca.append(x[i3] * r + x[i3 + 10] * (1 - r))
                ta.append(x[i3 + 20])
            else:
                ca.append(tem[i3])
                ta.append(tem2[i3])
        tem = ca
        tem2 = ta
        if ca[0] == 0:
            count += 0.1
            ta[0] = 0
        if ca[1] == 0:
            count += 0.1
            ta[1] = 0
        if ca[2] == 0:
            count += 0.1
            ta[2] = 0
        if ca[3] == 0:
            count += 0.05
            ta[3] = 0
        if ca[4] == 0:
            count += 0.05
            ta[4] = 0
        if ca[5] == 0:
            count += 0.05
            ta[5] = 0
        if ca[6] == 0:
            count += 0.05
            ta[6] = 0
        if ca[7] == 0:
            count += 0.2
            ta[7] = 0
        if ca[8] == 0:
            count += 0.3
            ta[8] = 0
        t = (ca[0] + ca[1] + ca[2]) / 3 * 0.3 + (ca[3] + ca[4] + ca[5] + ca[6]) / 4 * 0.2 + ca[7] * 0.2 + ca[8] * 0.3
        t2 = (ta[0] + ta[1] + ta[2]) / 3 * 0.3 + (ta[3] + ta[4] + ta[5] + ta[6]) / 4 * 0.2 + ta[7] * 0.2 + ta[8] * 0.3
        return t / (1 - count), t2 / (1 - count)


    g['全球温度'], g['全球价格'] = zip(*g.apply(cal_g_temp, axis=1))
    a['中证温度'] = a.apply(lambda x: x[0] * 0.8 + x[2] * 0.2, axis=1)
    a['全A温度'] = a.apply(lambda x: x[1] * 0.8 + x[3] * 0.2, axis=1)

    c1 = 'tomato'
    c2 = 'steelblue'
    c3 = 'g'
    a.rename(columns={'中证温度': 'A股温度'}, inplace=True)
    p = [.1, .2, .3, .4, .5, .6, .7, .8, .9]
    des = pd.DataFrame([a['A股温度'].describe(percentiles=p), g['全球温度'].describe(percentiles=p)])
    des = des.drop(['count', 'std'], axis=1)
    des.rename(columns={'mean': '平均值', 'min': '最小值', 'max': '最大值'}, inplace=1)
    des = """<h1>温度分布</h1>""" + des.to_html(float_format=lambda x: format(x, '.2f'))
    style = {'size': 18, 'color': 'red'}
    # indigo dimgray steelblue peru
    a2 = a.loc['2008':, 'A股温度']  # 此处为计算近期温度高点低点所用
    g2 = g.loc['2005':, '全球温度']
    fig, ax0 = plt.subplots()
    ax0.plot(g.index, g['全球价格'], c2, label='全球资产加权净值')

    ax = ax0.twinx()
    ax.plot(g.index, g['全球温度'], c1, label='全球温度')

    plt.grid(ls='--')
    # plt.annotate('%f' % g['temp'][-1], (g.index[-1], g['temp'][-1]))
    # plt.annotate('%.2f' % g2.max(), (g2.idxmax(), g2.max()), xytext=(-200, 5), textcoords='offset points'
    plt.text(g.index[-1], g['全球温度'][-1], '%.2f°' % g['全球温度'][-1], fontdict=style)
    # 上为标注当前温度，下为标注高低点
    plt.annotate('%.2f°' % g2.max(), (g2.idxmax(), g2.max()), xytext=(g2.idxmax(), g2.max() * 1.01 + 2),
                 bbox=dict(boxstyle='round,pad=0.4', fc='red', ec='k', lw=1, alpha=0.8))
    plt.annotate('%.2f°' % (g2.min()), (g2.idxmin(), g2.min()), xytext=(g2.idxmin(), g2.min() * 0.9 - 4),
                 bbox=dict(boxstyle='round,pad=0.4', fc='blue', ec='k', lw=1, alpha=0.2))
    plt.title(str(g.index[-1].month) + '月' + str(g.index[-1].day) + '日全球温度计', fontsize=24)
    fig.legend()
    ax0.set_xlabel('时间', size=18)
    ax.set_ylabel('温度', size=18)
    ax0.set_ylabel('价格', size=18)
    ax.set_yticks([g['全球温度'][-1]], minor=True)
    # ax2.yaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='minor', c=c3)
    buffer = BytesIO()
    plt.savefig(buffer, dpi=100)
    plot_data = buffer.getvalue()
    d = a['2006':]
    d = d[d.index != '2009-06-30']

    # **********************************************************************************************************************
    fig2, ax3 = plt.subplots()
    ax3.plot(a.index, a['中证全指'], c2, label='中证全指价格指数')

    ax2 = ax3.twinx()
    ax2.plot(a.index, a['A股温度'], c1, label='A股温度')
    plt.grid(ls='--')
    plt.text(a.index[-1], a['A股温度'][-1], '%.2f°' % a['A股温度'][-1], fontdict=style)
    plt.annotate('%.2f°' % a2.max(), (a2.idxmax(), a2.max()), xytext=(a2.idxmax(), a2.max() * 1.01 + 2),
                 bbox=dict(boxstyle='round,pad=0.4', fc='red', ec='k', lw=1, alpha=0.8))
    plt.annotate('%.2f°' % (a2.min()), (a2.idxmin(), a2.min()), xytext=(a2.idxmin(), a2.min() * 0.9 - 3),
                 bbox=dict(boxstyle='round,pad=0.4', fc='blue', ec='k', lw=1, alpha=0.2))
    plt.title(str(a.index[-1].month) + '月' + str(a.index[-1].day) + '日A股温度计', fontsize=24)
    fig2.legend()
    # ax2.set_yticks([0,20, 40, 60,80,100], minor=False)
    ax2.set_yticks([a['A股温度'][-1]], minor=True)
    # ax2.yaxis.grid(True, which='major')
    ax2.yaxis.grid(True, which='minor', c=c3)
    ax3.set_xlabel('时间', size=18)
    ax2.set_ylabel('温度', size=18)
    ax3.set_ylabel('价格', size=18)
    # plt.subplots_adjust(wspace=0)
    # figure 保存为二进制文件
    buffer = BytesIO()
    plt.savefig(buffer, dpi=100)
    plot_data2 = buffer.getvalue()
    # 图像数据转化为 HTML 格式
    a_temp = a.iloc[-1, -2]
    g_temp = g.iloc[-1, -2]
    ims = base64.b64encode(plot_data).decode()
    ims2 = base64.b64encode(plot_data2).decode()
    # ims3 = base64.b64decode(plot_data3).decode()

    with open(in_path + 'jzfx.jpg', 'rb') as f:
        ims3 = base64.b64encode(f.read()).decode()

    imd = "data:image/png;base64," + ims
    imd2 = "data:image/png;base64," + ims2
    imd3 = "data:image/png;base64," + ims3
    im_a = """<h1>微信公众号：价值发现者  独家发布全球估值温度计 </h1><h2>最新温度为%.4s度（A股）, %.4s度（全球）</h2>  """ % (
        a_temp, g_temp) + """<img style="width:100%" """ + """ src="%s">""" % imd2
    im_g = """<img style="width:100%" """ + """src="%s">""" % imd
    im3 = """<img src="%s">""" % imd3

    root = "<title>估值温度计</title>"  # 标签页名
    s = """<div>
            <div>说明：</div>
            <ul style="font-size:14px">
                <li>1、温度计是将当前估值在所有历史数据中取百分位，取值为0-100，历史数据越丰富，其表示的温度越准确。</li>
                <li>2、温度越高说明估值越贵，温度越低越具有投资价值，温度综合参考了市净率和市盈率估值，权重为0.8:0.2。</li>
                <li>3、图中上方红标表示温度高点，下方蓝标表示温度低点，最右方标注当前温度。将首日指数点位作为基准值，记为1.0。</li>
                <li>4、A股使用中证全指，全球指数权重为A股30%，美股（道琼斯、纳斯达克、标普）共30%，港股20%，欧洲（英、法、德）共15%，日经5%。</li>
                <li>5、全球温度计以美国证券交易所日历为准，A股以上交所交易日历为准。</li>
                <li>6、全球温度涉及多个指数，在其指数收盘后才能得到估值数据，因此更新会晚一天。</li></ul>
            <div style="margin-top: 10px;">更多资讯，请关注微信公众号：价值发现者</div>
        </div>"""
    root = root + im_a + im_g + s + im3  # 将多个 html 格式的字符串连接起来
    # lxml 库的 etree 解析字符串为 html 代码，并写入文件
    html = etree.HTML(root)
    tree = etree.ElementTree(html)
    tree.write('temp.html')
    files = {'file': open('temp.html', 'rb')}
    user_info = {'password': '884443'}
    r = requests.post("http://111.229.61.127:80/upload", data=user_info, files=files)
    # g['时间'] = g['时间'].dt.date
    G_data.index = G_data.index.date
    A_data.index = A_data.index.date
    g.index = g.index.date
    a.index = a.index.date
    G_data.to_excel(in_path + 'G_data.xlsx')
    A_data.to_excel(in_path + 'A_data.xlsx')
    g.to_excel(in_path + 'G_temp.xlsx', index=1)
    a.to_excel(in_path + 'A_temp.xlsx', index=1)
    time.sleep(15)
    webbrowser.open("http://111.229.61.127:80")
except Exception as e:
    with open(in_path + 'log.txt', 'w') as f:
        f.write(str(datetime.datetime.now()))
        f.write(traceback.format_exc())
