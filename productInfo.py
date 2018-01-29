import os
import io
import sys
import os.path
import array
import time
import string
#import xlwt
from xlwt import *
file = Workbook(encoding = 'utf-8')
#指定file以utf-8的格式打开
filename = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()));
table = file.add_sheet(filename)
#指定打开的文件名
rootdir = "E:/DX/PRODUCT"   # 指明被遍历的文件夹
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

fileType = 1#1:普通文本形式,2:表格形式
'''
for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    print(rootdir)
    for dirname in  dirnames:                       #输出文件夹信息
        print("parent is:" + parent)
        print("dirname is:" + dirname)

    for filename in filenames:                        #输出文件信息
        print("parent is:" + parent)
        print("filename is:" + filename)
        print("the full name of the file is:" + os.path.join(parent,filename)) #输出文件路径信息
'''
txtname = time.strftime('%Y%m%d',time.localtime(time.time()))+".txt";#源文件
fileHandle = open ( "E:/DX/PRODUCT/"+txtname,'r', encoding='UTF-8' )
fileList = fileHandle.readlines()

title = ("产品名称","账号","募集金额","风险比例金","操作周期","截止日期","固化","期内利息系数","募集金额系数")
for col in range(len(title)):
    table.write(0,col,title[col])
row = 1

if fileType == 1:
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
        table.write(row,0,A + G)
        table.write(row,1,B)
        table.write(row,2,C)
        table.write(row,3,D)
        table.write(row,4,E)
        table.write(row,5,F)
        table.write(row,6,G1)
        #table.write(row,7,float(G1)*int(E))
        #table.write(row,8,1-float(D))
        #table.write(row,7,string.atoi(G1)*string.atoi(E))
        #table.write(row,8,(1-string.atoi(D)))
        row = row + 1
elif fileType == 2:
    for fileLine in fileList[1:]:
        fileLine = fileLine.strip().replace(' ','').replace("，",",")#去空格及全角替换为半角
        proinof = fileLine.split(u"\t")
        #print(fileLine)
        print(proinof)
        #A,B,C,D,E,F,G,G1,G2
        A = proinof[1]
        B = proinof[2]
        C = proinof[3]
        D = proinof[4]
        E = proinof[5]
        Ff = proinof[6].split('/')
        if len(Ff) > 2:
            F = Ff[0]+'年'+Ff[1]+'月'+Ff[2]+'日'
        else:
            F = Ff[0]
        ghfd = proinof[7].split('+')
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
        table.write(row,0,A + G)
        table.write(row,1,B)
        table.write(row,2,C)
        table.write(row,3,D)
        table.write(row,4,E)
        table.write(row,5,F)
        table.write(row,6,G1)
        row = row + 1
fileHandle.close()

file.save('E:/DX/PRODUCT/'+filename+'.xls')
