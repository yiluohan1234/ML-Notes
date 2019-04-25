#coding=utf-8
'''
Created on 2017年7月31日

@author: cuiyufei

@description: 构造属性
'''
import pandas as pd

inputfile = '../data/4/electricity_data.xls'
outputfile = '../data/tmp/electricity_data.xls'

data = pd.read_excel(inputfile)
data[u'线损率'] = (data[u'供入电量'] - data[u'供出电量'])/data[u'供入电量']

data.to_excel(outputfile, index=False)
