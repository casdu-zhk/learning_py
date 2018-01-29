# -*- coding:utf-8 -*-
from pymongo import MongoClient
import xlrd
import time
import io
import os
import sys
from xlwt import *
import csv
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
def gci(filepath):
#遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    ls = []
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:
            temp = os.path.join(filepath,fi_d)
            print(temp)
            ls.append(temp)
    return ls
#递归遍历/root目录下所有文件
#gci('/root')
product = {
    "ClientAccountID" : "",
    "TradeDate" : "",
    "Symbol" : "",
    "Description" : "",
    "AssetClass" : "",
    "SettleDate" : "",
    "Buy/Sell" : "",
    "Quantity" : 0,
    "Price" : 0.0,
    "Proceeds" : "",
    "Amount" : "",
    "Commission" : 0.0,
    "Strategy" : "",
    "FundManager" : "",
    "ExecutionStrategy" : ""
}
#建立MongoDB数据库连接
client = MongoClient('localhost',27017)

#连接所需数据库,test为数据库名
db=client.redhorse

#连接所用集合，也就是我们通常所说的表，test为表名
col = db.dao_fund_info

list_dir =  gci('C:/Users/admin/Desktop/zhk/道基金日结单')
print(list_dir)
csvfile = ''

def insert2daofundtradeinfo(csvfile):
    count = col.count()
    csv_readers = csv.reader(open(csvfile, encoding='utf-8'))
    rows= [row for row in csv_readers]
    print(rows[1:])
    for s in rows[1:]:
        print(s)
        product["ClientAccountID"] = s[0]
        product["TradeDate"] = s[1]
        product["Symbol"] = s[2]
        product["Description"] = s[3]
        product["AssetClass"] = s[4]
        product["SettleDate"] = s[5]
        product["Buy/Sell"] = s[6]
        product["Quantity"] = s[7]
        product["Price"] = s[8]
        product["Proceeds"] = s[9]
        product["Amount"] = s[10]
        product["Commission"] = s[11]
        product["Strategy"] = s[13]
        product["FundManager"] = s[14]
        product["ExecutionStrategy"] = s[15]
        count = count+1
        product["_id"] = count
        print(product)
        print(count)
        print( col.insert_one( product ))

'''
for d in list_dir:
    insert2daofundtradeinfo(d)
'''
d='C:/Users/admin/Desktop/zhk/道基金日结单/道基金日结单20180110.csv'
insert2daofundtradeinfo(d)
