#coding=utf-8
'''
Created on 2017年8月1日

@author: cuiyufei

@description: 
'''
import pandas as pd
from apriori import *

inputfile = '../data/5/menu_orders.xls'
outputfle = '../data/tmp/apriori_rules.xls'

data = pd.read_excel(inputfile, header=None)

print u'\n转换原始数据至0-1矩阵'
ct = lambda x :pd.Series(1, index=x[pd.notnull(x)])
b = map(ct, data.as_matrix())
print b
data = pd.DataFrame(list(b)).fillna(0)
print u'转换完毕'
del b
print  data
support = 0.2
confidence = 0.5
ms = '---'
find_rule(data, support, confidence, ms).to_excel(outputfle)