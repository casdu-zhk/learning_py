import sys
import io
import pandas as pd
import copy
from collections import deque
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
def createData(file,symbol):
    #读取数据
    df = pd.read_excel(file)
    #根据日期排序
    #print(df)
    df = df.sort_values(by='OrderTime')
    #取需要的数据
    data0 = df[['Symbol','TradeDate','Buy/Sell','Quantity','Price','Amount']]
    #print(df1)
    #data0 = df1.sort_values(by='TradeDate')
    if(symbol == 'C'):
        symbol = 'C '
    flag = data0['Symbol'].str.startswith(symbol)
    #print(flag)
    a = data0['TradeDate'].astype(str).str[:8]
    #a1 = data0['Price'].astype(str)
    #print(b)
    data0.insert(6,'OrderDate',a)
    #data0.insert(7,'Price1',a1)
    #print(type(data0['Price1'][0]))
    #print(type(data0['OrderDate'][0]))

    data0 = data0[flag]
    #print(data0)
    df0 = data0.groupby(by=['OrderDate','Buy/Sell'],as_index = False)['Amount'].sum()
    df1 = data0.groupby(by=['OrderDate','Buy/Sell'],as_index = False)['Quantity'].sum()
    df2 = data0.groupby(by=['OrderDate','Buy/Sell'],as_index = False)['Price'].mean()#求平均
    data = pd.merge(df0, pd.merge(df1 , df2))
    #data['Amount'].astype()
    print(data)
    '''for i in data['Amount']:
        print(i)
    '''
    return data
#配对
def matchedPair(data):
    #定义一个零时的数LIST放每一组配对的数据tempList = ['symbol','buy/sell',0,'sell/buy',0]
    tempList = ['','',0,'',0]
    queue = deque([])
    List = []
    flag = False
    for indexs in data.index:
        tempList[0] = data.loc[indexs,'Buy/Sell']#.values['Buy/Sell']
        tempList[1] = float(data.loc[indexs,'Quantity'])
        tempList[2] = str(data.loc[indexs,'OrderDate'])#日期
        tempList[3] = float(data.loc[indexs,'Price'])#价格
        tempList[4] = float(data.loc[indexs,'Amount'])#市值
        if flag == False:
            #print('为空')
            queue.append(copy.deepcopy(tempList))
            flag = True
            #print('tempList:',tempList[0],tempList[1])
        else:
            #print(queue)
            if len(queue) > 0:
                if queue[0][0] == tempList[0]:#如果买卖方向相同
                    queue.append(copy.deepcopy(tempList))
                    #print('买卖方向相同' ,tempList, queue)
                else:
                    #print('方向不同')

                    p = queue.popleft()
                    #print('*****',queue,p)
                    if abs(p[1]) == abs(tempList[1]):#开仓数量等于平仓数量
                        #print("ok")
                        #print(p)
                        #print(tempList)
                        #print( p + tempList )
                        #print('end')
                        List.append(copy.deepcopy(p + tempList))#配对成功放入list
                    elif abs(p[1]) > abs(tempList[1]):#开仓数量大于平仓数量
                        #print('>',p)
                        List.append(copy.deepcopy(p + tempList))#配对成功部分放入list，剩余开仓单保留在数据中
                        tempList[0] = p[0]
                        tempList[1] = p[1] + tempList[1]
                        tempList[2] = p[2]
                        tempList[3] = p[3]
                        tempList[4] = p[4]
                        queue.insert(0,copy.deepcopy(tempList))
                    elif abs(p[1]) < abs(tempList[1]):#开仓数量小于平仓数量
                        #print('<ss',p)
                        digui(p,tempList,queue,List,flag)#进入递归
            if len(queue) < 1:
                flag = False
    return List

def digui(p,tempList,queue,List,flag):
    List.append(copy.deepcopy(p + tempList))#配对成功部分放入list，剩余平仓单继续配对
    #print('digui dayu',p + tempList)
    tempList[0] = p[0]
    tempList[1] = p[1] + tempList[1]
    tempList[2] = tempList[2]
    tempList[3] = tempList[3]
    tempList[4] = tempList[4]
    if len(queue) > 0:
        p = queue.popleft()
        if abs(p[1]) < abs(tempList[1]):
            digui(p,tempList,queue,List,flag)
        elif abs(p[1]) > abs(tempList[1]):
            List.append(copy.deepcopy(p + tempList))
            tempList[0] = p[0]
            tempList[1] = p[1] + tempList[1]
            tempList[2] = p[2]
            tempList[3] = p[3]
            tempList[4] = p[4]
            queue.append(copy.deepcopy(tempList))
        else:
            List.append(copy.deepcopy(p + tempList))
        if len(queue) < 1:
            flag = False
    else :
        queue.append(copy.deepcopy(tempList))
if __name__ == '__main__':
    file = 'C:/Users/admin/Downloads/data2017.xlsx'
    symbol = 'EUR.USD'#ZM,
    data = createData(file,symbol)#交易数据
    pairList = matchedPair(data)#数据配对
    #print(pairList)
    print('交易笔数：',len(pairList))
    lirun =0
    #生成指标语句
    for i in range(len(pairList)):
        openDate = pairList[i][2]#开仓日期
        closeDate = pairList[i][7]#平仓仓日期
        openPrice = round(pairList[i][3],4)#开仓价格
        closePrice = round(pairList[i][8],4)#平仓价格
        openAmount = pairList[i][4]#开仓市值
        closeAmount = pairList[i][9]#平仓市值

    '''
    #生成指标语句
    for i in range(len(pairList)):
        openDate = pairList[i][2]#开仓日期
        closeDate = pairList[i][7]#平仓仓日期
        openPrice = round(pairList[i][3],4)#开仓价格
        closePrice = round(pairList[i][8],4)#平仓价格
        openAmount = pairList[i][4]#开仓市值
        closeAmount = pairList[i][9]#平仓市值

        #print(openPrice*100)
        if False:
            #print(openPrice ,"   ", closePrice," ",openAmount)

            #以k线均价为开平仓点标记（有指数与开平仓点误差）
            #print('DRAWICON(REF(DATE,1)<>DATE &&DATE=',openDate[2:],',AVPRICE,\'ICO109\');')#标记开仓点
            if openAmount < 0:
                print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',HIGH,\'买\'),FONTSIZE20,COLORBLACK;')#开仓市值注释
            else:
                print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',HIGH,\'卖\'),FONTSIZE20,COLORBLACK;')#开仓市值注释
            #print('KTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',0,AVPRICE,1,COLORYELLOW,\'开仓',openAmount,'\');')#开仓市值注释
            #print('DRAWICON(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',AVPRICE,\'ICO5\');')#标记平仓点
            #print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',AVPRICE,\'平仓',closeAmount,'\'),FONTSIZE15;')#平仓市值注释
            print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',HIGH,\'平\'),FONTSIZE20,COLORRED;')#平仓市值注释
            if openAmount > 0:
                if openPrice < closePrice:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORRED,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORRED,LINETHICK2;')#划线
                else:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORGREEN,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORGREEN,LINETHICK2;')#划线
            else:
                if openPrice > closePrice:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORRED,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORRED,LINETHICK2;')#划线
                else:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORGREEN,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',AVPRICE, DATE=',closeDate[2:],',AVPRICE,0),COLORGREEN,LINETHICK2;')#划线
            print('//' + openDate[2:] + ':' +str(openAmount))
            print('//' + closeDate[2:] + ':' +str(closeAmount))
        else:
            #以开平仓价格为开平仓点标记（有指数与合约误差）
            #print('DRAWICON(REF(DATE,1)<>DATE &&DATE=',openDate[2:],',',openPrice,',\'ICO109\');')#标记开仓点
            if openAmount < 0:
                print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',HIGH,\'买\'),FONTSIZE20,COLORBLACK;')#开仓市值注释
            else:
                print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',HIGH,\'卖\'),FONTSIZE20,COLORBLACK;')#开仓市值注释
            #print('DRAWICON(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',',closePrice,',\'ICO5\');')#标记平仓点
            print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',HIGH,\'平\'),FONTSIZE20,COLORRED;')#平仓市值注释
            print('//'+openDate[2:] + ':' +str(openAmount))
            print('//'+closeDate[2:] + ':' +str(closeAmount))
            if openAmount < 0:
                #print(openPrice ,"   ", closePrice)
                if openPrice < closePrice:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
                else:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线
            else:
                if openPrice > closePrice:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
                else:
                    if openDate[2:] == closeDate[2:]:
                        print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线
                    else:
                        print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线

        print()


        #以开平仓价格为开平仓点标记（有指数与合约误差）
        print('DRAWICON(REF(DATE,1)<>DATE &&DATE=',openDate[2:],',',openPrice,',\'ICO109\');')#标记开仓点
        print('KTEXT(REF(DATE,1)<>DATE&&DATE=',openDate[2:],',0,',openPrice,',1,COLORYELLOW,\'开',openAmount,'\');')#开仓市值注释
        print('DRAWICON(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',',closePrice,',\'ICO5\');')#标记平仓点
        print('DRAWTEXT(REF(DATE,1)<>DATE&&DATE=',closeDate[2:],',',closePrice,',\'平',closeAmount,'\'),FONTSIZE15;')#平仓市值注释
        if openPrice < closePrice:
            if openDate[2:] == closeDate[2:]:
                print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
            else:
                print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORRED,LINETHICK2;')#划线
        else:
            if openDate[2:] == closeDate[2:]:
                print('DRAWLINE(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线
            else:
                print('DRAWLINE1(DATE=',openDate[2:],',',openPrice,', DATE=',closeDate[2:],',',closePrice,',0),COLORGREEN,LINETHICK2;')#划线
        '''
