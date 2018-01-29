#coding=utf-8
from pymongo import MongoClient
import os
import io
import sys
import os.path
import array
import time
import string
#import xlwt
from xlwt import *
#建立MongoDB数据库连接
client = MongoClient('localhost',27017)

#连接所需数据库,test为数据库名
db=client.redhorse

#连接所用集合，也就是我们通常所说的表，test为表名
col = db.dx_product_info
file = Workbook(encoding = 'utf-8')
#指定file以utf-8的格式打开
#filename = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()));
#table = file.add_sheet(filename)
#指定打开的文件名
rootdir = "E:/DX/PRODUCT"   # 指明被遍历的文件夹
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

txtname = time.strftime('%Y%m%d',time.localtime(time.time()))+".txt";#源文件
fileHandle = open ( "E:/DX/PRODUCT/"+txtname,'r', encoding='UTF-8' )
fileList = fileHandle.readlines()
title = ("产品名称","账号","募集金额","风险比例金","操作周期","截止日期","固化","期内利息系数","募集金额系数")
product1 = {
    "account" : "8017468",
    "amount" : "560万",
    "Riskratio" : "10%",
    "operatingperiod" : 43,
    "enddate" : "2018年1月15日"
}
count = col.count()
print(count)
row = 1
for fileLine in fileList:
    fileLine = fileLine.strip().replace(' ','').replace("，",",")#去空格及全角替换为半角
    proinof = fileLine.split(u",")
    #A,B,C,D,E,F,G,G1,G2
    for i in range(len(proinof)):
        #print(proinof[i])
        if( i == 0 ):
            A = proinof[i][proinof[i].find("=")+1:]
        elif( i == 1 ):
            B = proinof[i][proinof[i].find("帐号:")+3:]
        elif( i == 2 ):
            C = proinof[i][proinof[i].find("募集金额")+4:]
        elif( i == 3 ):
            D = proinof[i][proinof[i].find("风险金比例")+5:]
        elif( i == 4 ):
            E = proinof[i][proinof[i].find("操作周期")+4:proinof[i].find("天")]
        elif( i == 5 ):
            F = proinof[i][proinof[i].find("截止日期")+4:]
        elif( i == 6 ):
            ghfd = proinof[i].split('+')
            if( len(ghfd) > 1 ):
                G1 = ghfd[0][ghfd[0].find("固化")+2:]
                G2 = ghfd[1][ghfd[1].find("浮动")+2:]
                G = "(" + G1 + "+" + G2 + ")"
            else:
                if(ghfd[0].find("固化") != -1):
                    G1 = ghfd[0][ghfd[0].find("固化")+2:]
                else:
                    G1 = "0%"
                if(ghfd[0].find("浮动") != -1):
                    G2 = ghfd[0][ghfd[0].find("浮动")+2:]
                G = "(" + G1 + ")"
    print(A,B,C,D,E,F,G)
    product1["_id"] = count + row
    product1["acctName"] = A + G
    product1["account"] = B
    product1["amount"] = C
    product1["Riskratio"] = D
    product1["operatingperiod"] = E
    product1["enddate"] = F
    product1["yield"] = G1
    product1["createDate"] = time.strftime('%Y%m%d',time.localtime(time.time()))
    # 打印集合第1条记录
    print( col.insert_one( product1 ))
    #table.write(row,7,float(G1)*int(E))
    #table.write(row,8,1-float(D))
    #table.write(row,7,string.atoi(G1)*string.atoi(E))
    #table.write(row,8,(1-string.atoi(D)))
    row = row + 1

fileHandle.close()
