#-*- coding: utf-8 -*-
from WindPy import *
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pylab as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib.font_manager import FontProperties
import talib
import io
import sys
import matplotlib.ticker as ticker
'''
dates = dat.Times
close = fm['CLOSE'].values
sma5 = talib.SMA(close, timeperiod = 5)
ax1.plot(dates,sma5)
sma10 = talib.SMA(close, timeperiod = 10)
ax1.plot(dates,sma10)
'''
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
fm = pd.DataFrame()
#print("wewewe")
# 先设定一个日期转换方法
def format_date(x,pos=None):
    # 由于前面股票数据在 date 这个位置传入的都是int # 因此 x=0,1,2,... # date_tickers 是所有日期的字符串形式列表
    print(fm.index)
    if x < 0 or x > len(fm.index)-1:
        return ''
    return fm.index[int(x)]
#macd
def get_MACD(close, fastperiod, slowperiod, signalperiod) :
    macdDIFF, macdDEA, macd = talib.MACDEXT(close, fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1, signalperiod=signalperiod, signalmatype=1)
    macd = macd * 2
    return macdDIFF, macdDEA, macd

def createSPAN(symbol1, symbol2, period, title):

    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #有中文出现的情况，需要u'内容'
    w.start()
    #dat= w.wsd("ifi.wi", "open,high,low,close,volume,amt", "2017-05-10", "2018-01-07", "TradingCalendar=SZSE;Fill=Previous")
    '''
    dat = w.wsd("ifi.wi", "open,high,low,close,volume,amt","ED-1Y" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")
    fm=pd.DataFrame(dat.Data,index=dat.Fields,columns=dat.Times)#pandas timeseries type
    fm=fm.T
    dat2 = w.wsd("ifi.wi", "open,high,low,close,volume,amt","ED-14M" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")
    fm2 = pd.DataFrame(dat2.Data,index=dat2.Fields,columns=dat2.Times)#pandas timeseries type
    fm2 = fm2.T
    '''
    #w.wsd("AUFI.WI", "open,high,low,close,volume", "ED-200W", "2018-01-09", "Period=W")
    #w.wsd("AUFI.WI", "open,high,low,close,volume", "ED-200D", "2018-01-09", "")
    #w.wsd("AUFI.WI", "open,high,low,close,volume", "ED-200M", "2018-01-09", "Period=M")
    global fm
    #dat1 ,dat2
    if period == '1':#日线
        dat1 = w.wsd(symbol1, "open,high,low,close,volume","ED-1Y" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")
        dat2 = w.wsd(symbol2, "open,high,low,close,volume","ED-1Y" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")
    elif period == '2':#周线
        dat1 = w.wsd(symbol1, "open,high,low,close,volume", "ED-200M", datetime.today().strftime('%Y-%m-%d'), "Period=M")
        dat2 = w.wsd(symbol2, "open,high,low,close,volume", "ED-200M", datetime.today().strftime('%Y-%m-%d'), "Period=M")
    elif period == '3':#月线
        dat1 = w.wsd(symbol1, "open,high,low,close,volume", "ED-200M", datetime.today().strftime('%Y-%m-%d'), "Period=M")
        dat2 = w.wsd(symbol2, "open,high,low,close,volume", "ED-200M", datetime.today().strftime('%Y-%m-%d'), "Period=M")
    else:
        dat1 = w.wsd(symbol1, "open,high,low,close,volume","ED-1Y" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")
        dat2 = w.wsd(symbol2, "open,high,low,close,volume","ED-1Y" ,(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'), "Fill=Previous")

    fm1 = pd.DataFrame(dat1.Data,index=dat1.Fields,columns=dat1.Times)#pandas timeseries type
    fm1 = fm1.T
    fm2 = pd.DataFrame(dat2.Data,index=dat2.Fields,columns=dat2.Times)#pandas timeseries type
    fm2 = fm2.T
    fm = fm1/fm2
    #print(fm)
    #type(fm['OPEN'])
    w.close()
    fig = plt.figure(figsize=[18,8])#图片尺寸
    fig.suptitle(title, fontsize = 16, fontweight='bold')
    ax1 = plt.subplot2grid((3,12),(0,0),rowspan=2,colspan=12)
    #ax1 = plt.subplot(211)
    lt = []
    for i in range(len(fm['CLOSE'])):
        lt.append(i)
    #print(l)
    ohlc = zip(lt,fm['OPEN'],fm['HIGH'],fm['LOW'],fm['CLOSE'])
    #mondayFormatter = DateFormatter('%Y-%m-%d') # 如：2015-02-29
    #ax1.xaxis.set_major_formatter(mondayFormatter)
    candlestick_ohlc(ax1,ohlc,width =0.45,colorup='red',colordown='limegreen',alpha=1)
    close = [float(x) for x in fm['CLOSE']]
    # 调用talib计算10日移动平均线的值
    ma5 = talib.MA(np.array(close), timeperiod=5)
    ma10 = talib.MA(np.array(close), timeperiod=10)
    ma20 = talib.MA(np.array(close), timeperiod=20)
    ma40 = talib.MA(np.array(close), timeperiod=40)
    ma60 = talib.MA(np.array(close), timeperiod=60)
    ax1.plot(lt,ma5, label='MA5', linewidth=1 , color='cornflowerblue',alpha=0.7)
    ax1.plot(lt,ma10, label='MA10', linewidth=1 , color='gold',alpha=0.7)
    ax1.plot(lt,ma20, label='MA20', linewidth=1 , color='fuchsia',alpha=0.7)
    ax1.plot(lt,ma40, label='MA40', linewidth=1 , color='lawngreen',alpha=0.7)
    ax1.plot(lt,ma60, label='MA60', linewidth=1 , color='darkgray',alpha=0.7)
    #print(fm.index.map(date2num))
    #print(ax1.xaxis)
    #ax1.set_xticks(range(len(fm.index.map(date2num))))
    #ax1.set_xticklabels(fm.index.map(date2num))
    ax1.legend(loc='upper left')
    #用 set_major_formatter() 方法来修改主刻度的文字格式化方式
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(30))

    plt.grid(True)
    '''
    ax2 = plt.subplot2grid((8,12),(4,0),rowspan=1,colspan=12)
    ax2 = plt.subplot(312, sharex=ax1)
    ax2.bar(l,fm['VOLUME'],width=0.5,align='center')
    plt.grid(True)

    #ax2.set_xticklabels(fm.index,rotation=10)#rotation=10旋转角度
    plt.setp(ax1.get_xticklabels(),visible=True)
    #plt.setp(ax1.yaxis.get_ticklabels()[0],visible=True)
    #mondayFormatter = DateFormatter('%Y-%m-%d') # 如：2015-02-29
    #ax2.xaxis.set_major_formatter(mondayFormatter)
    '''
    ax2 = plt.subplot2grid((3,12),(2,0),rowspan=1,colspan=12,sharex=ax1)

    #macd, signal, hist = talib.MACD(df['CLOSE'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    macd, signal, hist = get_MACD(fm['CLOSE'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    #ax2 = plt.subplot(212, sharex=ax1)
    plt.plot(lt,macd,label='macd dif')#fm.index.map(date2num)
    plt.plot(lt,signal,label='signal dea')
    #plt.bar(1,2,width = 0.35,facecolor = 'lightskyblue',edgecolor = 'white')
    color = []
    for i in hist:
        if i >= 0:
            color.append('red')
        else:
            color.append('green')
    #print(color)
    plt.bar(lt,hist,width=0.35,align='center',color=color)
    plt.legend(loc='best')#显示图例
    # True 显示网格
    # linestyle 设置线显示的类型(一共四种)
    # color 设置网格的颜色
    # linewidth 设置网格的宽度
    #plt.grid(True, linestyle = "-.", color = "r", linewidth = "1")
    plt.grid(True)

    #mondayFormatter = DateFormatter('%Y-%m-%d') # 如：2015-02-29
    #ax3.xaxis.set_major_formatter(mondayFormatter)

    plt.show()

createSPAN("zcfi.wi", "rbfi.wi", '1', u'郑煤螺纹')
