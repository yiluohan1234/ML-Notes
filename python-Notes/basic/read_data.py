#!/usr/bin/env python
# coding=utf-8
#######################################################################
#       > File Name: read_data.py
#       > Author: cyf
#       > Mail: XXX@qq.com
#       > Created Time: Mon 22 Apr 2019 01:59:19 AM UTC
#######################################################################
import xlrd
import MySQLdb as mdb
from pymongo import MongoClient
import urllib2
import json
#logging
import time
import os
import logging
#时间格式
timeFormat = '%Y%m%d%H'
curTime = time.strftime(timeFormat, time.localtime())

#设置log路径
logPath = "./log"
if not os.path.exists(logPath):
    os.mkdir(logPath)
logFile = '%s/%s.log' %(logPath, curTime)

logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] %(asctime)s %(filename)s [line:%(lineno)d] [%(message)s]',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logFile,
                filemode='a+')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(filename)s: %(lineno)d %(levelname)-4s  %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
def read_txt(file_path):
    """read_txt（通过最基本的方式读取文件的数据）
        Args:
            file_path excel文件位置
        Returns:
            None
    """
    f = open(file_path)
    
    for lines in f.readlines():
        line = lines.strip('\n').split(',')
        name = line[0]
        sex = line[1]
        age = line[2]
        print name, sex, age
def read_excel_into_MySQL(file_path, sheet_name):
    """read_excel_into_MySQL（通过xlrd读取excel文件并插入mysql数据库）
        Args:
            file_path excel文件位置
            sheet_name 读取excel的sheet的名字
        Returns:
            None
    """
    #读取xlsx文件
    xlsx_data = xlrd.open_workbook(file_path)
    print 'All sheets: %s' %xlsx_data.sheet_names()
    
    sheet_data = xlsx_data.sheet_by_name(sheet_name)
    rows = sheet_data.nrows
    
    
    ret = []
    for i in xrange(rows):
        # 过滤标题行
        if i < 1:
            continue
        row_data = sheet_data.row_values(i)

        id = row_data[0]
        item_1 = row_data[1]
        item_2 = row_data[2]
        item_3 = row_data[3]

        values = (id, item_1, item_2, item_3)
        
        
        ret.append(values)
    logging.info(ret)
    try:
        db=mdb.connect(host='localhost',user='root',passwd='199037', port=3306, db='test',charset='utf8')
        
        cursor = db.cursor() 
         
        cursor.executemany('insert into test_xlsx (id, item_1, item_2, item_3) values (%s, %s, %s, %s)', ret)  
    except mdb.DatabaseError, e:
        logging.info(str(e))
        return 
    finally:
        db.commit()
        db.close()
    logging.info("序号 %s:共%s数据导入成功", id, len(ret))
def read_data_from_mongodb():
    """read_data_from_mongodb（读取mongodb的数据）
        Args:
            file_path excel文件位置
            sheet_name 读取excel的sheet的名字
        Returns:
            None
    """
    client = MongoClient() # 建立连接
    client = MongoClient('127.0.0.1', 27017) # 环境变量初始化
    db = client.test_py # 选择test_py库
    orders = db.ordersets # 选择orders集合
    terms = [{"user":
    "tony", "id": "31020", "age":
    "30", "products": ["215120", "245101",
    "128410"], "date": "2017-04-06"},
    {"user": "lucy", "id": "32210",
    "age": "29", "products": ["541001",
    "340740", "450111"],
    "date": "2017-04-06"}] # 定义一条数据集合用于插入
    #orders.insert_many(terms) # 插入数据
    print orders.find_one() # 获取一文档数据
    print '======================================='
    for i in orders.find(): # 获取所有文档数据并展示
        print i
    print '======================================='
    print orders.find()[0:2] # 查询特定范围内的数据记录
    print '======================================='
    print orders.find({"user": "lucy"}) # 所有数据，注意使用迭代方法查看数据
    print '======================================='
    orders.find_one({"user": "lucy"}) # 单条数据
def read_data_from_API():
    """read_data_from_API（读取API的数据）
        Args:
            file_path excel文件位置
            sheet_name 读取excel的sheet的名字
        Returns:
            None
    """
    add = '北京市中关村软件园' # 定义地址
    ak ='qcADbDw2rYAe9np8k#############' # 创建访问应用时获得的AK
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' # 请求URL
    req = urllib2.Request(url % (add, ak)) # 获得返回请求
    response = urllib2.urlopen(req)
    content = response.read()
    json_data = json.loads(content) #加载Json字符串对象
    
    print json.dumps(json_data, sort_keys=True, indent=2)# 打印输出
if __name__ == '__main__':
#     file_path = './data/test_xlsx.xlsx'
#     read_excel_into_MySQL(file_path, 'Sheet1')
    #read_data_from_API()
    read_txt('./data/names/yob1880.txt')
