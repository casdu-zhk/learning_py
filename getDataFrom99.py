# -*- coding:utf-8 -*-
from xlwt import *
import urllib.request
import os
import time
import io
import sys
import requests
from bs4 import BeautifulSoup
import pandas
from WindPy import *
import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
# 打开URL，返回HTML信息
def open_url(url):
    # 根据当前URL创建请求包
    req = urllib.request.Request(url)
    # 添加头信息，伪装成浏览器访问
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    # 发起请求
    response = urllib.request.urlopen(req)
    # 返回请求到的HTML信息
    return response.read()

# 查找URL中的下一页页码
def get_page(url):
    # 请求网页，并解码
    html=open_url(url).decode('utf-8')
    # 在html页面中找页码
    a=html.find('current-comment-page')+23
    b=html.find(']',a)
    # 返回页码
    return html[a:b]

# 查找当前页面所有图片的URL
def find_imgs(url):
    # 请求网页
    html=open_url(url).decode('utf-8')
    img_addrs=[]
    # 找图片
    a = html.find('img src=')
    #不带停，如果没找到则退出循环
    while a != -1:
        # 以a的位置为起点，找以jpg结尾的图片
        b = html.find('.jpg',a, a+255)
        # 如果找到就添加到图片列表中
        if b != -1:
            img_addrs.append(html[a+9:b+4])
        # 否则偏移下标
        else:
            b=a+9
        # 继续找
        a=html.find('img src=',b)
    return img_addrs

# 保存图片
def save_imgs(img_addrs):
    for each in img_addrs:
        print('download image:%s'%each)
        filename=each.split('/')[-1]
        with open(filename,'wb') as f:
            img=open_url("http:"+each)
            f.write(img)

# 下载图片
# folder 文件夹前缀名
# pages 爬多少页的资源，默认只爬10页
def download_mm(folder='woman',pages=10):
    folder+= str(time.time())
    # 创建文件夹
    os.mkdir(folder)
    # 将脚本的工作环境移动到创建的文件夹下
    os.chdir(folder)

    # 本次脚本要爬的网站
    url='http://jandan.net/ooxx/'
    # 获得当前页面的页码
    page_num=int(get_page(url))
    for i in range(pages):
        page_num -= i
        # 建立新的爬虫页
        page_url=url+'page-'+str(page_num-1)+'#comments'
        # 爬完当前页面下所有图片
        img_addrs=find_imgs(page_url)
        # 将爬到的页面保存起来
        save_imgs(img_addrs)

if __name__ == '__main__':
    w.start()
    l = w.tdays("2017-01-01","2017-12-24")
    #print(l)

    w.stop()
    file = Workbook(encoding = 'utf-8')
    #指定file以utf-8的格式打开
    filename = '99期货'#time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()));
    table = file.add_sheet(filename)
    table.write(0,0, '品种')
    table.write(0,1, '多头持仓')
    table.write(0,2, '空头持仓')
    table.write(0,3, '净头寸')
    table.write(0,4, '占交易所总持仓比例')
    table.write(0,5, '换手率')
    for mem in mems:
        count = 1
        for i in l.Times :
            date = i.strftime("%Y-%m-%d")
            target = 'http://service.99qh.com/hold2/MemberGoodsHold/GetTableHtml.aspx?date='+date+'&mem='+ mem +'&user=99qh&script=no'
            req = requests.get(url = target)
            html = req.text
            bf = BeautifulSoup(html,'html.parser')
            data = pandas.read_html(req.text)[0]
            r = 0
            tempdata = data[[0,1,2,3,4,5]][(data[0]=='铁矿石')]
            table.write(count,0, tempdata.values[0][0])
            table.write(count,1, tempdata.values[0][1])
            table.write(count,2, tempdata.values[0][2])
            table.write(count,3, tempdata.values[0][3])
            table.write(count,4, tempdata.values[0][4])
            table.write(count,5, tempdata.values[0][5])
            table.write(count,6, '2017-12-22')
            count += 1
    file.save('C:/Users/admin/Desktop/'+filename+'.xls')

'''
    for index,row in data[[0]].iterrows():
        #print(index) #获取行的索引
        #print (row.a) #根据列名获取字段
        sym = row[0]
        #print(sym)#根据列的序号（从0开始）获取字段
        if sym == '铁矿石':
            r = index
            break
'''
    #print(r)
    #print(data)
    #print(type(data))
