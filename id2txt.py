#coding=utf-8
import sys

import xlrd
print (sys.getdefaultencoding())
#wb = xlrd.workbook('副本交易部—大象保收益产品情况.xlsx')
#xlwt.workbook(encoding='utf-8')
filename='D:/MYTEST/20180126.xlsx'
data = xlrd.open_workbook(filename)
#获取sheet
sheet = data.sheet_by_name("20151105")
file_object = open('D:/MYTEST/thefile.txt', 'w')
print("************start***********")
for i in range(sheet.nrows):
    if(i == 0):
        #print(sheet.row(i)[1].value)
        pass
    else:
        #print(sheet.row(i)[1].value)
        if(str(sheet.row(i)[1].value)!='' and isinstance(sheet.row(i)[1].value,float)):
            if(i != 1):
                file_object.write(" ,")
            file_object.write(str(int(sheet.row(i)[1].value)))
            count = i
print("************end!***********")
print("count:",count)
file_object.close( )
'''
# 打印每张表的最后一列
# 方法1
for s in data.sheets():
    #print ()"== The last column of sheet '%s' ==" % (s.name))
    for i in range(s.nrows):
        print(s.row(i)[1].value)

# 方法2
for i in range(wb.nsheets):
    s = wb.sheet_by_index(i)
    print "== The last column of sheet '%s' ==" % (s.name)
    for v in s.col_values(s.ncols - 1):
        print v

# 方法3
for name in wb.sheet_names():
    print "== The last column of sheet '%s' ==" % (name)
    s = wb.sheet_by_name(name)
    c = s.ncols - 1
    for r in range(s.nrows):
        print s.cell_value(r, c)
'''
