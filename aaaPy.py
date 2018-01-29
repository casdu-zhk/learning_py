from WindPy import *
from WindPy import w
import sys
import io
import xlrd
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
w.start();
def dealData():
    dicData = {}
    filename='E:/pythonWORK/targetData.xlsx'
    data = xlrd.open_workbook(filename)
    #获取sheet
    sheet = data.sheet_by_name("Sheet1")
    for i in range(sheet.nrows):
        dicData[sheet.row(i)[1].value] = sheet.row(i)[2].value
    print(dicData)
    return dicData
def getData( symbol ,beginDate):

    #data=w.wsd("600000.SH","close,amt","2017-12-07", datetime.today()-timedelta(10))#取浦发银行收盘价等信息
    data=w.wsd( symbol ,"open,close",beginDate ,datetime.today()-timedelta(1))#取开盘价，收盘价
    #date = w.wset("futurecc","wind_code=jm1805.dce")
    #aaa = w.wset("futurecc","wind_code=JMFI.WI")
    #print(aaa)
    #print(data.Times)
    print(data)
    #l = data.Data[0]
    #list = []
    str = ''
    for i in range(len(data.Data[0])):
        #日内收盘价-开盘价
        if data.Data[1][i] - data.Data[0][i] >= 0:
            str = str + '1'
            #list.append('1')
        else:
            str = str + '0'
            #list.append('0')
    print("时间区间:%s--%s"%(beginDate ,"昨天"))
    print(str)
    #print(list)
    #print(date)

    return str

def frequency( dataStr , flagStr ):
    if( flagStr == '1'):
        tempFlagStr = '0'
    else:
        tempFlagStr = '1'
    #获取最大连涨天数
    maxDay = 1
    count = 0
    for i in range( len(dataStr)-1 ):
        if dataStr[i:i+1] == dataStr[i+1:i+2] and dataStr[i:i+1] == flagStr:
            count = count + 1
            if maxDay < count:
                maxDay = count
        else:
            count = 1
    print( "最多连续涨（跌） %d 天"%(maxDay) )

    resultList = []
    for i in range( 1, maxDay+1 ):
        #拼接子字符串
        temp = tempFlagStr
        times = 0
        for m in range( i ):
            temp = temp + flagStr
        temp = temp + tempFlagStr
        for j in range( len(dataStr)-i-2 ):
            if dataStr[ j : j+i+2 ] == temp:
                times = times + 1
        #比较开头和结尾
        if( dataStr[:i+1] == temp[1:] ):
            times = times + 1
        if( dataStr[-i-1:] == temp[:-1] ):
            times = times + 1
        #将统计结果记录列表中
        resultList.append(times)
    for i in range(maxDay):
        if(flagStr == '1'):
            print("连涨 %d 天次数：%d次" %(i+1 , resultList[i]))
        else:
            print("连跌 %d 天次数：%d次" %(i+1 , resultList[i]))
#target='CUFI.WI,ALFI.WI,ZNFI.WI,PBFI.WI,NIFI.WI,AUFI.WI,AGFI.WI,JFI.WI,JMFI.WI,ZCFI.WI,IFI.WI,RBFI.WI,HCFI.WI,FGFI.WI,RUFI.WI,LFI.WI,TAFI.WI,VFI.WI,PPFI.WI,MAFI.WI,BUFI.WI,AFI.WI,CFI.WI,MFI.WI,RMFI.WI,YFI.WI,OIFI.WI,PFI.WI,CFFI.WI,SRFI.WI,CSFI.WI'
targetList = dealData()
for key,value in targetList.items():
    #print('key is %s,value is %s'%(key,value))
    dataStr = getData( key , value)#获取涨跌序列JMFI.WI JM.dce
    frequency( dataStr ,'1')#获取统计频率 第二个参数'0':跌，'1'：涨
#dealData()
w.stop()
